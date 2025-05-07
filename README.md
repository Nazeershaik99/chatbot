# AI Chatbot with Dashboard

A sophisticated AI chatbot application built with Flask, MongoDB, and Google's Gemini AI. This project features user authentication, real-time chat functionality, file uploads, and an analytics dashboard.

## 🌟 Features

- **AI-Powered Chat Interface**
  - Real-time conversation with Gemini AI
  - Message history tracking
  - Category-based response classification
  - Response time monitoring

- **User Authentication System**
  - Secure registration and login
  - Password encryption using bcrypt
  - Session management
  - User profile tracking

- **Interactive Dashboard**
  - Chat analytics and statistics
  - Category distribution visualization
  - Daily activity tracking
  - Response time analysis
  - Recent interactions display

- **File Management**
  - Secure file upload system
  - Support for multiple file types
  - Upload history tracking
  - File access management

## 🛠️ Technologies Used

- **Backend**
  - Flask (Python web framework)
  - MongoDB (Database)
  - Google Gemini AI API
  - bcrypt (Password hashing)

- **Frontend**
  - HTML5
  - CSS3
  - JavaScript
  - Chart.js (for dashboard visualizations)

- **Security**
  - Session-based authentication
  - Secure file handling
  - Password encryption
  - Input validation

## 📋 Prerequisites

- Python 3.8+
- MongoDB
- Google Gemini AI API key

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-chatbot.git
cd ai-chatbot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up MongoDB:
```bash
# Start MongoDB service
# On Windows:
net start MongoDB
# On Linux:
sudo systemctl start mongod
```

4. Configure environment variables:
```bash
# Create a .env file in the project root
GOOGLE_API_KEY=your_gemini_api_key
FLASK_SECRET_KEY=your_secret_key
MONGODB_URI=mongodb://localhost:27017/
```

5. Create required directories:
```bash
mkdir static/uploads
```

## 💻 Usage

1. Start the application:
```bash
python app.py
```

2. Access the application:
   - Open your browser and navigate to `http://localhost:5000`
   - Register a new account or login with existing credentials

## 📊 Dashboard Features

- **Analytics Overview**
  - Total questions asked
  - Average response time
  - Most active categories
  - Daily interaction count

- **Visualization Types**
  - Category distribution pie chart
  - Daily activity line graph
  - Response time analysis
  - Recent interactions list

## 🔐 Security Features

- Password hashing using bcrypt
- Secure file upload handling
- Session-based authentication
- Input validation and sanitization
- Secure MongoDB connection

## 📁 Project Structure

```
ai-chatbot/
├── app.py                 # Main application file
├── static/               
│   ├── uploads/          # File upload directory
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript files
├── templates/
│   ├── chat.html        # Chat interface
│   ├── dashboard.html   # Analytics dashboard
│   ├── login.html      # Login page
│   └── register.html   # Registration page
├── requirements.txt     # Python dependencies
└── README.md           # Project documentation
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Nazeer Shaik** - *Initial work* - [Nazeershaik99](https://github.com/Nazeershaik99)

## 🙏 Acknowledgments

- Google Gemini AI for providing the chat API
- MongoDB for database support
- Flask community for the excellent web framework
- Chart.js for dashboard visualizations

## 📞 Support

For support, email nazeershaik@example.com or create an issue in the repository.

## 🔄 Version History

- 0.1.0
  - Initial Release
  - Basic chat functionality
  - User authentication
  - Simple dashboard

- 0.2.0
  - Added file upload functionality
  - Enhanced dashboard analytics
  - Improved error handling
  - UI/UX improvements

 You can access it here : https://chatbot-pigf.onrender.com/login
