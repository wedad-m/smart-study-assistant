import re
import random
from collections import Counter 

STOP_WORDS = {
    "the", "is", "and", "a", "an", "of", "to", "in", "that", "this",
    "for", "with", "on", "as", "are", "was", "by", "be", "or", "it",
    "from", "at", "which"
}

QUESTION_TEMPLATES = [
    "Which of the following best defines the term '{word}'?",
    "What is the correct definition of '{word}'?",
    "Choose the best description for '{word}'.",
    "Which option correctly explains the concept of '{word}'?",
    "What does the term '{word}' refer to?"
]

def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    words = text.split()
    return [w for w in words if w not in STOP_WORDS and len(w) > 3]

def extract_keywords(text, max_keywords=6):
    words = clean_text(text)
    freqWords = Counter(words)

    available = len(freqWords)
    n = min(max_keywords, available)

    return [w for w, _ in freqWords.most_common(n)]

def generate_mcq(keywords):
    questions = []
    for word in keywords[:3]:
        options = [w for w in keywords if w != word]
        options = options[:3] + [word]

        template = random.choice(QUESTION_TEMPLATES)

        questions.append({
            "question": template.format(word=word),
            "answer": word,
            "options": sorted(options)
        })
    return questions

def extract_sentences(text):
    sentences = re.split(r'[.!?]', text)
    return [s.strip() for s in sentences if len(s.split()) > 5]

def generate_true_false(text, keywords):
    sentences = extract_sentences(text)
    statements = []

    if not sentences:
        return statements

    for word in keywords[3:5]:
        related = [s for s in sentences if word.lower() in s.lower()]

        if related:
            statement = random.choice(related)
            statements.append({
                "statement": statement,
                "answer": "True"
            })

    return statements

def generate_short_answer(keywords):
    return [f"Explain the role of {word}." for word in keywords[5:]]
