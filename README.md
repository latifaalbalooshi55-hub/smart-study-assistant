# 🤖 IntelliLearn

[![Streamlit App](https://intellilearn-study-assistant.streamlit.app/)]

**IntelliLearn** is an interactive learning platform designed for beginner students exploring Artificial Intelligence and Intelligent Systems Engineering.

The application combines a structured rule-based assistant, topic library, quizzes, progress tracking, user accounts, and downloadable learning reports in one Streamlit web application.

## 🌐 Live Application

Try IntelliLearn online:

**(https://intellilearn-study-assistant.streamlit.app/)**

## ✨ Features

- User registration, sign-in, and logout
- Password hashing for demonstration accounts
- Rule-based Intelligent Systems study assistant
- Conversation history and suggested questions
- Approximate topic matching for minor spelling mistakes
- Searchable topic library
- Beginner and intermediate quizzes
- Randomized quiz questions
- Answer review with feedback
- Persistent local quiz history using SQLite
- Personal learning dashboard
- Progress and difficulty-performance charts
- Achievement system
- Downloadable quiz-progress report in CSV format
- Progress reset option

## 📚 Supported Topics

IntelliLearn currently includes explanations and examples for topics such as:

- Artificial Intelligence
- Machine Learning
- Deep Learning
- Neural Networks
- Computer Vision
- Natural Language Processing
- Robotics
- Sensors
- Internet of Things
- Python
- Algorithms
- Training Data
- Supervised Learning
- Unsupervised Learning
- Overfitting

## 🛠️ Technologies Used

- Python
- Streamlit
- SQLite
- Pandas
- Git
- GitHub
- Visual Studio Code

## 🧠 How the Assistant Works

The assistant is fully rule-based and does not rely on a paid AI API.

It uses:

- A structured topic knowledge base
- Text normalization
- Topic aliases such as `AI`, `ML`, `NLP`, and `IoT`
- Approximate string matching for small spelling mistakes
- Conversation history through Streamlit Session State
- Structured responses containing definitions, examples, and related topics

## 📊 Learning Dashboard

Each account can view:

- Number of quiz attempts
- Highest score
- Average percentage
- Current learning level
- Progress over time
- Performance by difficulty
- Unlocked achievements
- Complete quiz-attempt history

Users can also download their progress as a CSV report.

## 📁 Project Structure

```text
smart-study-assistant/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
└── screenshots/
```

## ▶️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/latifaalbalooshi55-hub/smart-study-assistant.git
```

### 2. Open the project folder

```bash
cd smart-study-assistant
```

### 3. Install the dependencies

```bash
python3 -m pip install -r requirements.txt
```

### 4. Run the application

```bash
python3 -m streamlit run app.py
```

The application should open in your browser.

## 🗄️ Database

IntelliLearn uses SQLite for local account and quiz-history storage.

The database file is excluded from the public repository to prevent test accounts and locally generated records from being uploaded.

> **Deployment note:** The hosted portfolio version uses temporary local storage. Account and quiz-history data may reset when the Streamlit Community Cloud application restarts or redeploys.

## 🔐 Security Note

Passwords are hashed rather than stored as plain text.

This authentication system was created for educational and portfolio purposes. It should not be treated as production-level authentication for sensitive personal information.

## 🚀 Future Improvements

- Move account and quiz data to a hosted database
- Add password reset functionality
- Expand the assistant knowledge base
- Add more quiz difficulty levels
- Add topic-based quiz selection
- Add automated testing
- Improve mobile responsiveness
- Add optional Arabic support
- Add administrator tools for managing questions

## 👩‍💻 Author

**Latifa Albalooshi**  
Intelligent Systems Engineering Student

- GitHub: https://github.com/latifaalbalooshi55-hub
- LinkedIn: www.linkedin.com/in/latifaalbalooshi

## 📄 License

This project was created for educational and portfolio purposes.
