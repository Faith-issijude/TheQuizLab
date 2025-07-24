# 📚 TheQuizLab – AI-Powered Quiz Generator

**TheQuizLab** is an interactive Streamlit web app that generates intelligent quiz questions from your documents using natural language processing. Ideal for educators, students, and trainers, it can turn lecture notes, reports, and articles into quizzes with just a few clicks.

---

## 🚀 Features

- 📁 Upload support for `.docx`, `.pdf`, `.txt`, `.csv`, and `.ipynb` files  
- 🎯 Customize quiz difficulty: Easy, Medium, or Hard  
- ❓ Choose question types: Multiple Choice (MCQ) or Fill-in-the-Blank  
- 🧠 Generate quiz questions using `sentence-transformers`  
- 📥 Export generated quizzes as a downloadable `.docx` file  
- ⚙️ Progress bar and retry logic for robust question generation  
- 💡 Tips section for better document preparation

---

## 🖼️ Screenshot
<img width="1355" height="611" alt="image" src="https://github.com/user-attachments/assets/dca362fb-4915-4fa3-9d5b-222964f6d338" />

---

## 🛠️ Tech Stack

- Python 3.10+
- [Streamlit](https://streamlit.io/) – UI Framework
- [sentence-transformers](https://www.sbert.net/) – Semantic embedding model
- `pdfminer.six` – PDF text extraction  
- `pypandoc` – File format conversion  
- `python-docx` – Word document handling  
- `dotenv` – For managing API keys (if applicable)

---

## 📂 Folder Structure

TheQuizLab/
│

├── main.py # Main Streamlit app

├── quiz_engine.py # Handles question generation logic

├── doc_processor.py # Handles file reading & conversion

├── requirements.txt

└── README.md


---

## 🧪 How to Run

1. **Clone this repository**

git clone https://github.com/your-username/TheQuizLab.git
cd TheQuizLab

2. **Install dependencies** 

pip install -r requirements.txt

**3. Run the app**

streamlit run main.py
📝 Note: For PDF, CSV, and notebook file uploads, Pandoc must be installed on your system.

---
## 🧠 **How it Works**

The user uploads a document.
The app extracts clean text and uses a pre-trained SentenceTransformer model to understand and generate quiz-style questions.
You choose difficulty level and type (MCQ or Fill-in-the-blank).
The app returns a list of questions with answers, and you can download it as a Word document.

🧾**License**
MIT License. Feel free to modify and use for educational or personal projects.

🙌 **Contributing**
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

👨‍💻 **Author**
Faithfulness Issijude and Toochi Uduma 
