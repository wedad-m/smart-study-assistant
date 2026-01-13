# 🧠 Exam Question Generator

An AI-powered tool that automatically generates **exam-style questions** from lecture text using Natural Language Processing (NLP).

This project is part of the **Smart Study Assistant** system — a collection of intelligent tools designed to help students study more effectively.

---

## ✨ Features

✔ Extracts **important keywords** from lecture text  
✔ Generates **Multiple Choice Questions (MCQ)** with varied templates  
✔ Creates **True / False** questions directly from real sentences in the text  
✔ Produces **Short Answer** questions for deeper understanding  
✔ Handles both **short and long** lecture content gracefully  

---

## 🧠 How It Works

1. Cleans and processes the input text  
2. Removes common stop-words  
3. Extracts the most frequent and meaningful keywords  
4. Generates:
   - MCQ questions  
   - True / False questions based on actual lecture sentences  
   - Short Answer questions  

This design ensures the questions are **context-aware**, educational, and realistic.

---

## 🧪 Example Output

> **Input Lecture Text**
> ```
> Machine learning is a branch of artificial intelligence that focuses on building systems that learn from data.
> ```

> **Generated Output**
> - Keywords  
> - MCQ Questions  
> - True / False Questions  
> - Short Answer Prompts  

---

## 🛠 Technologies Used

- Python  
- Regular Expressions (`re`)  
- Natural Language Processing Fundamentals  
- Frequency Analysis (`Counter`)  

---

## 🚀 How to Run

```bash
python main.py
