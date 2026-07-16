import random
from difflib import get_close_matches

import pandas as pd
import streamlit as st

from database import (
    authenticate_user,
    create_tables,
    create_user,
    delete_quiz_history,
    get_quiz_history,
    get_user_statistics,
    save_quiz_result,
)


create_tables()

# -----------------------------
# PAGE CONFIGURATION
# -----------------------------
st.set_page_config(
    page_title="IntelliLearn",
    page_icon="🤖",
    layout="centered"
)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = None

if "language" not in st.session_state:
    st.session_state.language = "English"

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# -----------------------------
# SESSION MEMORY
# -----------------------------
if "questions_asked" not in st.session_state:
    st.session_state.questions_asked = 0

if "quiz_attempts" not in st.session_state:
    st.session_state.quiz_attempts = []

if "highest_score" not in st.session_state:
    st.session_state.highest_score = 0

# -----------------------------
# LOGIN AND SIGN-UP
# -----------------------------
if not st.session_state.logged_in:

    st.title("🤖 IntelliLearn")

    st.write(
        "Sign in or create an account to track your learning progress."
    )

    login_tab, signup_tab = st.tabs(
        ["Sign In", "Create Account"]
    )

    with login_tab:

        with st.form("login_form"):

            login_username = st.text_input(
                "Username",
                key="login_username",
            )

            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password",
            )

            login_submitted = st.form_submit_button(
                "Sign In",
                type="primary",
            )

        if login_submitted:

            if authenticate_user(
                login_username,
                login_password,
            ):
                st.session_state.logged_in = True
                st.session_state.username = login_username.strip()

                st.success("Signed in successfully.")
                st.rerun()

            else:
                st.error(
                    "Incorrect username or password."
                )

    with signup_tab:

        with st.form("signup_form"):

            new_username = st.text_input(
                "Choose a username",
                key="new_username",
            )

            new_password = st.text_input(
                "Choose a password",
                type="password",
                key="new_password",
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password",
            )

            signup_submitted = st.form_submit_button(
                "Create Account"
            )

        if signup_submitted:

            if new_password != confirm_password:
                st.error("The passwords do not match.")

            else:
                success, message = create_user(
                    new_username,
                    new_password,
                )

                if success:
                    st.success(
                        f"{message} You can now sign in."
                    )

                else:
                    st.error(message)

    st.stop()
# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("📚 Navigation")

st.sidebar.write(
    f"Signed in as **{st.session_state.username}**"
)

if st.sidebar.button("Log Out"):

    st.session_state.logged_in = False
    st.session_state.username = None

    st.rerun()

page = st.sidebar.radio(
    "Choose a page",
    [
        "Home",
        "Dashboard",
        "Ask the Assistant",
        "Topic Library",
        "Study Tips",
        "Quiz",
        "About"
    ]
)


# -----------------------------
# HOME PAGE
# -----------------------------
if page == "Home":

    st.title("🤖 IntelliLearn")

    st.write("""
Welcome to **IntelliLearn**!

This application was created for students studying
**Intelligent Systems Engineering**.

Use the navigation menu on the left to:

- 💬 Ask questions
- 📚 Explore important topics
- 💡 Receive study tips
- 📝 Test yourself with a quiz
- 📊 Track your progress
""")

    st.subheader("Topics You Can Learn")

    st.markdown("""
- Artificial Intelligence
- Machine Learning
- Python
- Robotics
- Computer Vision
- Data Science
- Deep Learning
- Natural Language Processing
- Internet of Things
- Sensors
""")


# -----------------------------
# DASHBOARD
# -----------------------------
elif page == "Dashboard":

    st.title("📊 Learning Dashboard")

    username = st.session_state.username
    statistics = get_user_statistics(username)
    history = get_quiz_history(username)

    attempts = statistics["attempts"]
    highest_score = statistics["highest_score"]
    average_percentage = statistics["average_percentage"]

    if average_percentage >= 80:
        level = "Advanced Beginner"
        level_icon = "🏆"

    elif average_percentage >= 60:
        level = "Developing"
        level_icon = "📈"

    elif attempts > 0:
        level = "Getting Started"
        level_icon = "🌱"

    else:
        level = "New Learner"
        level_icon = "✨"

    column1, column2, column3, column4 = st.columns(4)

    column1.metric(
        "Quiz Attempts",
        attempts
    )

    column2.metric(
        "Highest Score",
        f"{highest_score}/5"
    )

    column3.metric(
        "Average Score",
        f"{average_percentage:.0f}%"
    )

    column4.metric(
        "Current Level",
        f"{level_icon} {level}"
    )

    st.divider()

    if not history:

        st.info(
            "Complete your first quiz to unlock progress charts "
            "and achievements."
        )

    else:

        chart_rows = []

        for attempt_number, result in enumerate(
            history,
            start=1
        ):
            chart_rows.append(
                {
                    "Attempt": attempt_number,
                    "Percentage": result[3],
                    "Difficulty": result[0]
                }
            )

        progress_dataframe = pd.DataFrame(chart_rows)

        st.subheader("Progress Over Time")

        st.line_chart(
            progress_dataframe,
            x="Attempt",
            y="Percentage"
        )

        st.subheader("Performance by Difficulty")

        difficulty_summary = (
            progress_dataframe
            .groupby("Difficulty")["Percentage"]
            .mean()
            .reset_index()
        )

        st.bar_chart(
            difficulty_summary,
            x="Difficulty",
            y="Percentage"
        )

        st.subheader("Achievements")

        achievements = []

        if attempts >= 1:
            achievements.append(
                "🎯 First Quiz Completed"
            )

        if attempts >= 3:
            achievements.append(
                "🔥 Consistent Learner — 3 Quiz Attempts"
            )

        if attempts >= 5:
            achievements.append(
                "📚 Dedicated Student — 5 Quiz Attempts"
            )

        if highest_score == 5:
            achievements.append(
                "🏆 Perfect Score"
            )

        if average_percentage >= 80:
            achievements.append(
                "⭐ Strong Performance"
            )

        if achievements:
            for achievement in achievements:
                st.success(achievement)

        else:
            st.info(
                "Keep completing quizzes to unlock achievements."
            )

        st.subheader("Quiz History")

        history_rows = []

        for attempt_number, result in enumerate(
            history,
            start=1
        ):
            history_rows.append(
                {
                    "Attempt": attempt_number,
                    "Difficulty": result[0],
                    "Score": f"{result[1]}/{result[2]}",
                    "Percentage": f"{result[3]:.0f}%",
                    "Date": result[4].replace("T", " ")
                }
            )

        history_dataframe = pd.DataFrame(history_rows)

        st.dataframe(
            history_dataframe,
            use_container_width=True,
            hide_index=True
        )

        csv_data = history_dataframe.to_csv(
            index=False
        ).encode("utf-8")

        st.download_button(
            label="⬇️ Download Progress Report",
            data=csv_data,
            file_name=f"{username}_quiz_progress.csv",
            mime="text/csv"
        )

        with st.expander("⚠️ Reset Progress"):

            st.warning(
             "This will permanently delete all of your quiz history."
            )

            confirm_reset = st.checkbox(
              "I understand that this cannot be undone."
            )

            if st.button(
             "Delete My Quiz History",
             disabled=not confirm_reset
            ):
                delete_quiz_history(username)

                st.success("Your quiz history has been deleted.")

                st.rerun()
# -----------------------------
# ASK THE ASSISTANT
# -----------------------------
elif page == "Ask the Assistant":

    st.title("💬 IntelliLearn Assistant")

    st.write(
        "Ask about artificial intelligence, machine learning, "
        "robotics, programming, sensors, and related topics."
    )

    # Knowledge used by the rule-based assistant
    assistant_topics = {
        "artificial intelligence": {
            "definition": (
                "Artificial Intelligence, or AI, is the field of creating "
                "computer systems that can perform tasks that normally "
                "require human intelligence."
            ),
            "example": (
                "Examples include voice assistants, recommendation systems, "
                "image recognition, and autonomous vehicles."
            ),
            "related": [
                "Machine Learning",
                "Computer Vision",
                "Natural Language Processing"
            ]
        },

        "machine learning": {
            "definition": (
                "Machine Learning is a branch of AI where computers learn "
                "patterns from data and use those patterns to make predictions."
            ),
            "example": (
                "An email spam filter can learn from labelled emails and "
                "predict whether a new email is spam."
            ),
            "related": [
                "Supervised Learning",
                "Training Data",
                "Deep Learning"
            ]
        },

        "deep learning": {
            "definition": (
                "Deep Learning is a type of machine learning that uses neural "
                "networks with many layers to learn complex patterns."
            ),
            "example": (
                "Deep learning can be used to recognize objects in images "
                "or convert speech into text."
            ),
            "related": [
                "Neural Networks",
                "Machine Learning",
                "Computer Vision"
            ]
        },

        "neural network": {
            "definition": (
                "A neural network is a computational model inspired loosely "
                "by the way biological neurons process information."
            ),
            "example": (
                "A neural network can learn to classify handwritten numbers "
                "by studying many labelled examples."
            ),
            "related": [
                "Deep Learning",
                "Training Data",
                "Artificial Intelligence"
            ]
        },

        "computer vision": {
            "definition": (
                "Computer Vision helps computers analyze and understand "
                "images and videos."
            ),
            "example": (
                "A smart parking system can use computer vision to determine "
                "whether parking spaces are empty or occupied."
            ),
            "related": [
                "Image Recognition",
                "Deep Learning",
                "Smart Parking"
            ]
        },

        "natural language processing": {
            "definition": (
                "Natural Language Processing, or NLP, helps computers "
                "understand, analyze, and generate human language."
            ),
            "example": (
                "Chatbots, translation systems, and sentiment analysis "
                "applications use NLP."
            ),
            "related": [
                "Artificial Intelligence",
                "Chatbots",
                "Machine Learning"
            ]
        },

        "robotics": {
            "definition": (
                "Robotics combines programming, electronics, sensors, "
                "control systems, and mechanical engineering."
            ),
            "example": (
                "A warehouse robot may use sensors to detect obstacles "
                "and software to choose a safe route."
            ),
            "related": [
                "Sensors",
                "Automation",
                "Control Systems"
            ]
        },

        "sensor": {
            "definition": (
                "A sensor is a device that measures information from "
                "the physical environment."
            ),
            "example": (
                "Examples include temperature, motion, light, pressure, "
                "ultrasonic, and proximity sensors."
            ),
            "related": [
                "Internet of Things",
                "Robotics",
                "Embedded Systems"
            ]
        },

        "internet of things": {
            "definition": (
                "The Internet of Things, or IoT, connects physical devices "
                "so they can collect, exchange, and respond to data."
            ),
            "example": (
                "A smart thermostat can measure room temperature and allow "
                "the user to control it through a mobile application."
            ),
            "related": [
                "Sensors",
                "Networking",
                "Embedded Systems"
            ]
        },

        "python": {
            "definition": (
                "Python is a general-purpose programming language known "
                "for its readable syntax and large collection of libraries."
            ),
            "example": (
                "Python is commonly used for data analysis, automation, "
                "web applications, and machine-learning projects."
            ),
            "related": [
                "Programming",
                "Streamlit",
                "Machine Learning"
            ]
        },

        "algorithm": {
            "definition": (
                "An algorithm is an ordered set of steps used to solve "
                "a problem or complete a task."
            ),
            "example": (
                "A sorting algorithm arranges a collection of values "
                "from smallest to largest."
            ),
            "related": [
                "Programming",
                "Problem Solving",
                "Machine Learning"
            ]
        },

        "training data": {
            "definition": (
                "Training data is the information used to teach a "
                "machine-learning model to recognize patterns."
            ),
            "example": (
                "To train a cat-image classifier, the training data may "
                "contain many labelled images of cats and other animals."
            ),
            "related": [
                "Testing Data",
                "Machine Learning",
                "Model Accuracy"
            ]
        },

        "supervised learning": {
            "definition": (
                "Supervised Learning is a machine-learning approach that "
                "uses labelled examples containing both inputs and answers."
            ),
            "example": (
                "A model can learn to predict house prices using properties "
                "whose selling prices are already known."
            ),
            "related": [
                "Machine Learning",
                "Classification",
                "Regression"
            ]
        },

        "unsupervised learning": {
            "definition": (
                "Unsupervised Learning finds patterns or groups in data "
                "that does not contain labelled answers."
            ),
            "example": (
                "A business may use clustering to group customers according "
                "to similar purchasing behaviour."
            ),
            "related": [
                "Clustering",
                "Machine Learning",
                "Data Analysis"
            ]
        },

        "overfitting": {
            "definition": (
                "Overfitting happens when a model learns the training data "
                "too closely and performs poorly on new, unseen data."
            ),
            "example": (
                "A model may achieve excellent training accuracy but low "
                "testing accuracy because it memorized the training examples."
            ),
            "related": [
                "Training Data",
                "Testing Data",
                "Model Evaluation"
            ]
        }
    }

    topic_aliases = {
        "ai": "artificial intelligence",
        "ml": "machine learning",
        "nlp": "natural language processing",
        "iot": "internet of things",
        "neural networks": "neural network",
        "sensors": "sensor"
    }

    # Separate chat history for each signed-in account
    chat_key = f"assistant_history_{st.session_state.username}"

    if chat_key not in st.session_state:
        st.session_state[chat_key] = [
            {
                "role": "assistant",
                "content": (
                    "Hello! Ask me about AI, machine learning, robotics, "
                    "computer vision, Python, sensors, or other supported topics."
                )
            }
        ]

    def find_assistant_topic(user_message):
        """Find the closest supported topic in the user's message."""
        cleaned_message = user_message.lower().strip()

        # Check abbreviations and aliases first
        for alias, full_topic in topic_aliases.items():
            if alias == cleaned_message or alias in cleaned_message.split():
                return full_topic

        # Check whether a complete topic appears in the message
        for topic_name in assistant_topics:
            if topic_name in cleaned_message:
                return topic_name

        # Compare individual words and short phrases for spelling errors
        possible_phrases = [cleaned_message]
        words = cleaned_message.split()

        possible_phrases.extend(words)

        for index in range(len(words) - 1):
            possible_phrases.append(
                f"{words[index]} {words[index + 1]}"
            )

        for phrase in possible_phrases:
            close_match = get_close_matches(
                phrase,
                assistant_topics.keys(),
                n=1,
                cutoff=0.72
            )

            if close_match:
                return close_match[0]

        return None

    def create_rule_based_answer(user_message):
        """Generate a structured response from the topic library."""
        cleaned_message = user_message.lower().strip()
        words = cleaned_message.split()

        if any(
          greeting in words
         for greeting in ["hello", "hi", "hey"]
        ):
            return (
              "Hello! What Intelligent Systems topic would you "
             "like to learn about?"
         )

        if "what can you answer" in cleaned_message or cleaned_message == "help":
            supported = ", ".join(
                topic.title() for topic in assistant_topics
            )

            return (
                "I can currently explain these topics:\n\n"
                f"{supported}."
            )

        matched_topic = find_assistant_topic(user_message)

        if matched_topic is None:
            suggestions = get_close_matches(
                cleaned_message,
                assistant_topics.keys(),
                n=3,
                cutoff=0.35
            )

            if suggestions:
                formatted_suggestions = ", ".join(
                    topic.title() for topic in suggestions
                )

                return (
                    "I could not identify that topic clearly. "
                    "You may be looking for:\n\n"
                    f"**{formatted_suggestions}**"
                )

            return (
                "I do not have information about that topic yet. "
                "Try asking about AI, machine learning, deep learning, "
                "robotics, computer vision, NLP, IoT, sensors, Python, "
                "algorithms, training data, or overfitting."
            )

        topic_information = assistant_topics[matched_topic]

        related_topics = ", ".join(
            topic_information["related"]
        )

        return (
            f"### {matched_topic.title()}\n\n"
            f"**Definition:** {topic_information['definition']}\n\n"
            f"**Example:** {topic_information['example']}\n\n"
            f"**Related topics:** {related_topics}"
        )

    # Display previous conversation
    for message in st.session_state[chat_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Suggested questions
    st.write("**Try asking:**")

    suggestion_columns = st.columns(3)

    suggestions = [
        "What is machine learning?",
        "Explain computer vision",
        "What is overfitting?"
    ]

    selected_suggestion = None

    for column, suggestion in zip(
        suggestion_columns,
        suggestions
    ):
        if column.button(
            suggestion,
            use_container_width=True
        ):
            selected_suggestion = suggestion

    typed_question = st.chat_input(
        "Ask an Intelligent Systems question..."
    )

    question = selected_suggestion or typed_question

    if question:
        st.session_state.questions_asked += 1

        st.session_state[chat_key].append(
            {
                "role": "user",
                "content": question
            }
        )

        answer = create_rule_based_answer(question)

        st.session_state[chat_key].append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()

    if st.button("Clear Conversation"):
        st.session_state[chat_key] = [
            {
                "role": "assistant",
                "content": (
                    "Conversation cleared. What would you "
                    "like to learn about?"
                )
            }
        ]

        st.rerun()

# -----------------------------
# TOPIC LIBRARY
# -----------------------------
elif page == "Topic Library":

    st.title("📚 Topic Library")

    topics = {
        "Artificial Intelligence": (
            "Artificial Intelligence enables computers to perform "
            "tasks that normally require human intelligence, such as "
            "learning, reasoning, and decision-making."
        ),

        "Machine Learning": (
            "Machine Learning allows computers to learn patterns "
            "from data and use those patterns to make predictions."
        ),

        "Deep Learning": (
            "Deep Learning is a type of machine learning that uses "
            "neural networks with multiple layers."
        ),

        "Computer Vision": (
            "Computer Vision helps computers understand and analyze "
            "images and videos."
        ),

        "Robotics": (
            "Robotics combines programming, sensors, electronics, "
            "and mechanical systems to create intelligent machines."
        ),

        "Natural Language Processing": (
            "Natural Language Processing helps computers understand "
            "and generate human language."
        ),

        "Internet of Things": (
            "The Internet of Things connects physical devices so "
            "they can collect and exchange information."
        ),

        "Sensors": (
            "Sensors collect information from the environment, such "
            "as temperature, motion, distance, or light."
        ),

        "Data Science": (
            "Data Science combines programming, statistics, and data "
            "analysis to discover patterns and support decision-making."
        ),

        "Python": (
            "Python is a popular programming language used in AI, "
            "automation, data science, and web development."
        )
    }

    search = st.text_input(
        "Search the topic library",
        placeholder="Example: robotics"
    ).lower().strip()

    matching_topics = 0

    for topic, explanation in topics.items():

        if search == "" or search in topic.lower():

            matching_topics += 1

            with st.expander(topic):
                st.write(explanation)

    if matching_topics == 0:
        st.warning("No matching topic was found.")


# -----------------------------
# STUDY TIPS
# -----------------------------
elif page == "Study Tips":

    st.title("💡 Study Tips")

    tips = [
        "Study for 25 minutes, then take a 5-minute break.",
        "Practice coding every day, even for 20 minutes.",
        "Teach someone else what you learned.",
        "Build small projects instead of only watching tutorials.",
        "Review difficult topics before sleeping.",
        "Use flashcards for important definitions.",
        "Take handwritten notes while learning.",
        "Test yourself instead of only rereading your notes.",
        "Break large topics into smaller sections.",
        "Explain programming concepts out loud in your own words."
    ]

    st.write(
        "Press the button to receive a random study tip."
    )

    if st.button("Generate Study Tip"):
        st.success(random.choice(tips))


# -----------------------------
# QUIZ
# -----------------------------
elif page == "Quiz":

    st.title("📝 Intelligent Systems Quiz")

    difficulty = st.selectbox(
        "Choose difficulty",
        ["Beginner", "Intermediate"]
    )

    beginner_questions = [
        {
            "question": "Which field allows computers to learn from data?",
            "options": [
                "Web Design",
                "Machine Learning",
                "Graphic Design",
                "Networking"
            ],
            "answer": "Machine Learning"
        },
        {
            "question": "Which technology helps computers understand images?",
            "options": [
                "Computer Vision",
                "Cybersecurity",
                "Cloud Storage",
                "Web Development"
            ],
            "answer": "Computer Vision"
        },
        {
            "question": "Which programming language is commonly used in AI?",
            "options": [
                "HTML",
                "Python",
                "CSS",
                "XML"
            ],
            "answer": "Python"
        },
        {
            "question": "Which device collects information from the environment?",
            "options": [
                "Sensor",
                "Printer",
                "Speaker",
                "Screen"
            ],
            "answer": "Sensor"
        },
        {
            "question": "Which field combines machines, sensors, and programming?",
            "options": [
                "Marketing",
                "Robotics",
                "Accounting",
                "Graphic Design"
            ],
            "answer": "Robotics"
        },
        {
            "question": "What does AI stand for?",
            "options": [
                "Artificial Intelligence",
                "Automated Internet",
                "Advanced Interface",
                "Artificial Integration"
            ],
            "answer": "Artificial Intelligence"
        },
        {
            "question": "What does IoT stand for?",
            "options": [
                "Internet of Things",
                "Intelligence of Technology",
                "Input of Tools",
                "Internet of Testing"
            ],
            "answer": "Internet of Things"
        }
    ]

    intermediate_questions = [
        {
            "question": "Which model is inspired by biological neurons?",
            "options": [
                "Neural Network",
                "Database",
                "Web Browser",
                "Spreadsheet"
            ],
            "answer": "Neural Network"
        },
        {
            "question": "Which type of learning uses labelled data?",
            "options": [
                "Supervised Learning",
                "Unsupervised Learning",
                "Random Learning",
                "Manual Learning"
            ],
            "answer": "Supervised Learning"
        },
        {
            "question": "What is overfitting?",
            "options": [
                "Performing well on training data but poorly on new data",
                "Using too little storage",
                "Training without data",
                "Removing all model features"
            ],
            "answer": "Performing well on training data but poorly on new data"
        },
        {
            "question": "Which field processes human language?",
            "options": [
                "Natural Language Processing",
                "Computer Graphics",
                "Networking",
                "Embedded Design"
            ],
            "answer": "Natural Language Processing"
        },
        {
            "question": "Which sensor can measure distance?",
            "options": [
                "Ultrasonic Sensor",
                "LED",
                "Speaker",
                "Motor"
            ],
            "answer": "Ultrasonic Sensor"
        },
        {
            "question": "What is training data used for?",
            "options": [
                "Teaching a model to recognize patterns",
                "Changing screen brightness",
                "Creating folders",
                "Connecting to Wi-Fi"
            ],
            "answer": "Teaching a model to recognize patterns"
        },
        {
            "question": "What is an algorithm?",
            "options": [
                "A set of steps used to solve a problem",
                "A computer screen",
                "A type of sensor",
                "A storage device"
            ],
            "answer": "A set of steps used to solve a problem"
        }
    ]

    if difficulty == "Beginner":
        question_bank = beginner_questions
    else:
        question_bank = intermediate_questions

    quiz_key = f"quiz_questions_{difficulty}"
    submitted_key = f"quiz_submitted_{difficulty}"
    score_key = f"quiz_score_{difficulty}"
    answers_key = f"quiz_answers_{difficulty}"

    if quiz_key not in st.session_state:
        st.session_state[quiz_key] = random.sample(
            question_bank,
            5
        )

    if submitted_key not in st.session_state:
        st.session_state[submitted_key] = False

    # Reset old quiz data created before answers were saved
    if (
        st.session_state[submitted_key]
        and answers_key not in st.session_state
    ):
        st.session_state[submitted_key] = False

        if score_key in st.session_state:
            del st.session_state[score_key]

    questions = st.session_state[quiz_key]
    user_answers = []

    for number, question in enumerate(
        questions,
        start=1
    ):

        st.subheader(f"Question {number}")

        answer = st.radio(
            question["question"],
            question["options"],
            key=f"{difficulty}_question_{number}"
        )

        user_answers.append(answer)

    if st.button(
        "Submit Quiz",
        disabled=st.session_state[submitted_key]
    ):

        score = 0

        for index, question in enumerate(questions):
            if user_answers[index] == question["answer"]:
                score += 1

        save_quiz_result(
            username=st.session_state.username,
            difficulty=difficulty,
            score=score,
            total_questions=len(questions)
        )

        st.session_state[submitted_key] = True
        st.session_state[score_key] = score
        st.session_state[answers_key] = user_answers.copy()

        st.rerun()

    if st.session_state[submitted_key]:

        score = st.session_state[score_key]
        saved_answers = st.session_state[answers_key]
        percentage = score / len(questions) * 100

        st.divider()
        st.subheader("Your Result")

        column1, column2 = st.columns(2)

        column1.metric(
            "Score",
            f"{score}/{len(questions)}"
        )

        column2.metric(
            "Percentage",
            f"{percentage:.0f}%"
        )

        st.progress(score / len(questions))

        if score == len(questions):
            st.success(
                "Excellent! You answered everything correctly."
            )
            st.balloons()

        elif score >= 3:
            st.success(
                "Good job! You understand the main concepts."
            )

        else:
            st.warning(
                "Keep learning and try another quiz."
            )

        with st.expander("Review Your Answers"):

            for number, question in enumerate(
                questions,
                start=1
            ):

                user_answer = saved_answers[number - 1]
                correct_answer = question["answer"]

                st.write(
                    f"**{number}. {question['question']}**"
                )

                st.write(
                    f"Your answer: {user_answer}"
                )

                st.write(
                    f"Correct answer: {correct_answer}"
                )

                if user_answer == correct_answer:
                    st.success("Correct")
                else:
                    st.error("Incorrect")

                st.divider()

    if st.button("Start New Quiz"):

        keys_to_delete = [
            quiz_key,
            submitted_key,
            score_key,
            answers_key
        ]

        for key in keys_to_delete:
            if key in st.session_state:
                del st.session_state[key]

        for number in range(1, 6):

            answer_key = f"{difficulty}_question_{number}"

            if answer_key in st.session_state:
                del st.session_state[answer_key]

        st.rerun()


# -----------------------------
# ABOUT
# -----------------------------
elif page == "About":

    st.title("ℹ️ About IntelliLearn")

    st.write("""
**IntelliLearn** is a beginner-friendly educational assistant
built using Python and Streamlit.

### Technologies Used

- Python
- Streamlit
- Git
- GitHub
- Visual Studio Code

### Skills Demonstrated

- Python Programming
- Conditional Statements
- Dictionaries
- Loops
- Session State
- User Interaction
- Streamlit Development
- Problem Solving

### Current Features

- Multi-page navigation
- Learning dashboard
- Question counter
- Topic library
- Study-tip generator
- Five-question quiz
- Quiz score history
- Highest-score tracking

### Future Improvements

- Add quiz difficulty levels
- Randomize quiz questions
- Add an OpenAI-powered assistant
- Save progress permanently
- Add Arabic language support
- Deploy the app online
""")


# -----------------------------
# FOOTER
# -----------------------------
st.divider()

st.caption(
    "Created by Latifa Albalooshi • "
    "Intelligent Systems Engineering Student"
)