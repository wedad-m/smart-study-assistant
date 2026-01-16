# Smart Study Assistant – Exam Question Generator

An intelligent study assistant that automatically generates exam-style questions from lecture text using Natural Language Processing (NLP).

This tool is designed to help students move beyond memorization by generating questions that test understanding, reasoning, and conceptual clarity.

---

## Why this project?

Students often rely on rereading notes or memorizing definitions when preparing for exams.  
However, effective studying requires **active recall** and **conceptual understanding**.

This project addresses that problem by transforming raw lecture text into meaningful practice questions, encouraging deeper thinking rather than rote memorization.

---

## What does it generate?

The assistant analyzes lecture text and generates different types of questions:

- **Definition-based questions**  
  Generated only when a concept is explicitly defined in the text.

- **Contextual multiple-choice questions (MCQs)**  
  Focused on understanding concepts within real sentences, not isolated keywords.

- **True / False questions**  
  Designed to test reasoning by subtly modifying factual statements.

- **Short-answer questions**  
  Encourage explanation and reflection rather than one-word answers.

---

## What makes it intelligent?

- Filters out generic terms such as *system*, *application*, and *process*
- Extracts only meaningful, domain-relevant concepts
- Detects explicit definitions using linguistic patterns
- Generates questions based on **context**, not keyword matching
- Avoids definition questions when no valid definition exists
- Uses NLP analysis (spaCy) instead of hardcoded rules

---

## Example

### Input
```text
Artificial intelligence is a field of study that focuses on building systems capable of performing tasks that normally require human intelligence.
```

### Generated Question (Easy Mode)

```text
Which concept best fits the following statement?

"Artificial intelligence is a field of study that focuses on building systems capable of performing tasks that normally require human intelligence."

Options:
- Machine learning
- Artificial intelligence
- Decision making
- Neural networks
```

### Generated Questions (Hard Mode)

```text
True / False:
Machine learning is a subset of artificial intelligence. (True)

Short Answer:
Explain the role of neural networks in artificial intelligence systems.
```

---

## How it works

1. The input lecture text is processed using spaCy NLP
2. Key concepts are extracted using linguistic and contextual rules
3. Explicit definitions are detected using strict patterns
4. Question types are generated based on the selected difficulty level
5. Output is displayed through a command-line interface

---

## How to run

### Requirements

* Python 3.9+
* spaCy
* spaCy English model (`en_core_web_sm`)

### Installation

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Run the program

```bash
python main.py
```

---

## Difficulty modes

* **Easy**
  Generates contextual multiple-choice questions focused on understanding.

* **Hard**
  Generates True/False questions and short-answer questions that require reasoning and explanation.

---

## Tech Stack

* Python
* spaCy (Natural Language Processing)
* Rule-based linguistic analysis
* Command-line interface (CLI)

---

## Future Improvements

* Medium difficulty level
* Question quality scoring
* Web-based interface
* Export questions to PDF or quiz platforms
* Support for additional academic domains

---

## Author

Developed as an academic NLP project focused on improving study effectiveness through intelligent question generation.

