import os

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from pymongo import MongoClient
from datetime import datetime, UTC, timedelta
import time
import bcrypt
import google.generativeai as genai


app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Gemini API Configuration
GOOGLE_API_KEY = 'AIzaSyA-PzmGEx1-HRPQwbMQFBQrh3Y6O0hdktA'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash')

# MongoDB Connection with error handling
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client['chatbot_db']
    users = db['users']
    user_interactions = db['user_interactions']
    print("Successfully connected to MongoDB")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def categorize_message(message):
    message = message.lower()
    if any(word in message for word in ['learn', 'study', 'course', 'teach', 'education', 'training']):
        return 'Education'
    elif any(word in message for word in ['code', 'programming', 'software', 'develop', 'tech', 'computer']):
        return 'Technology'
    elif any(word in message for word in ['science', 'research', 'experiment', 'physics', 'chemistry', 'biology']):
        return 'Science'
    elif any(word in message for word in ['art', 'music', 'paint', 'draw', 'creative', 'design']):
        return 'Arts'
    return 'General'


@app.route('/')
@login_required
def home():
    current_time = datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')
    return render_template('chat.html',
                           username=session.get('username'),
                           current_datetime=current_time)


@app.route('/chat', methods=['POST'])
@login_required
def chat():
    try:
        data = request.json
        message = data['message']
        start_time = time.time()

        try:
            # Generate response
            response = model.generate_content(message)
            ai_response = response.text
        except Exception as model_error:
            print(f"Model Error: {str(model_error)}")
            ai_response = "I apologize, but I encountered an error generating the response."

        # Calculate response time and category
        response_time = time.time() - start_time
        category = categorize_message(message)

        # Store in MongoDB
        interaction_data = {
            "user_id": session['user_id'],
            "username": session.get('username'),
            "query": message,
            "response": ai_response,
            "category": category,
            "response_time": response_time,
            "timestamp": datetime.now(UTC)
        }

        try:
            user_interactions.insert_one(interaction_data)
            print(f"Stored interaction for user: {session.get('username')}")
        except Exception as db_error:
            print(f"Database Error: {str(db_error)}")

        return jsonify({'reply': ai_response})

    except Exception as e:
        print(f"Chat Error: {str(e)}")
        return jsonify({'reply': 'Sorry, I encountered an error processing your request.'})


@app.route('/dashboard')
@login_required
def dashboard():
    try:
        user_id = session['user_id']

        # Get basic stats
        total_questions = user_interactions.count_documents({"user_id": user_id})

        # Get category distribution
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": "$category",
                "count": {"$sum": 1}
            }},
            {"$sort": {"count": -1}}
        ]
        categories = list(user_interactions.aggregate(pipeline))

        category_labels = ['Education', 'Technology', 'Science', 'Arts', 'General']
        category_data = []
        for label in category_labels:
            count = next((cat['count'] for cat in categories if cat['_id'] == label), 0)
            category_data.append(count)

        today_start = datetime.now(UTC).replace(hour=0, minute=0, second=0, microsecond=0)
        today_interactions = user_interactions.count_documents({
            "user_id": user_id,
            "timestamp": {"$gte": today_start}
        })

        # Calculate average response time
        pipeline = [
            {"$match": {"user_id": user_id}},
            {"$group": {
                "_id": None,
                "avg_response_time": {"$avg": "$response_time"}
            }}
        ]
        avg_response = list(user_interactions.aggregate(pipeline))
        avg_response_time = round(avg_response[0]['avg_response_time'], 2) if avg_response else 0

        # Get recent activities
        recent_activities = list(user_interactions.find(
            {"user_id": user_id},
            {"query": 1, "category": 1, "response": 1, "timestamp": 1, "_id": 0}
        ).sort("timestamp", -1).limit(5))

        # Format timestamps for recent activities
        for activity in recent_activities:
            if 'timestamp' in activity:
                activity['timestamp'] = activity['timestamp'].strftime('%Y-%m-%d %H:%M:%S')

        # Prepare daily activity data
        days = 7
        activity_labels = [(datetime.now(UTC) - timedelta(days=i)).strftime('%Y-%m-%d')
                           for i in range(days - 1, -1, -1)]
        activity_data = []

        for day in activity_labels:
            day_start = datetime.strptime(day, '%Y-%m-%d').replace(tzinfo=UTC)
            day_end = (day_start + timedelta(days=1))
            count = user_interactions.count_documents({
                "user_id": user_id,
                "timestamp": {
                    "$gte": day_start,
                    "$lt": day_end
                }
            })
            activity_data.append(count)

        stats = {
            'total_questions': total_questions,
            'avg_response_time': avg_response_time,
            'top_category': categories[0]['_id'] if categories else 'N/A',
            'today_interactions': today_interactions
        }

        return render_template(
            'dashboard.html',
            username=session.get('username'),
            stats=stats,
            recent_activities=recent_activities,
            category_labels=category_labels,
            category_data=category_data,
            activity_labels=activity_labels,
            activity_data=activity_data
        )
    except Exception as e:
        print(f"Dashboard error: {str(e)}")
        return "Error loading dashboard", 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']

            if users.find_one({'username': username}):
                return 'Username already exists'

            if users.find_one({'email': email}):
                return 'Email already registered'

            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user_data = {
                'username': username,
                'password': hashed,
                'email': email,
                'created_at': datetime.now(UTC),
                'last_login': None,
                'account_status': 'active',
                'profile': {
                    'total_interactions': 0,
                    'favorite_categories': [],
                    'last_active': None
                }
            }

            result = users.insert_one(user_data)

            if result.inserted_id:
                print(f"User registered successfully: {username}")
                return redirect(url_for('login'))
            else:
                return 'Registration failed'

        except Exception as e:
            print(f"Registration error: {str(e)}")
            return 'An error occurred during registration'

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = users.find_one({'username': username})
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            # Update last login time
            users.update_one(
                {'_id': user['_id']},
                {
                    '$set': {
                        'last_login': datetime.now(UTC),
                        'profile.last_active': datetime.now(UTC)
                    }
                }
            )

            session['username'] = username
            session['user_id'] = str(user['_id'])
            return redirect(url_for('home'))

        return 'Invalid username/password combination'

    return render_template('login.html')


@app.route('/check_user/<username>')
@login_required
def check_user(username):
    if session.get('username') != username:
        return jsonify({'error': 'Unauthorized'}), 403

    user = users.find_one({'username': username}, {'password': 0})
    if user:
        user['_id'] = str(user['_id'])
        return jsonify(user)
    return jsonify({'error': 'User not found'}), 404


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)