"""
Smart Study Assistant
Core logic for extracting study-relevant concepts and generating exam questions
based on meaning and context rather than keyword frequency.
"""

import random
import re
from collections import Counter
from typing import List, Dict, Optional

import spacy
import logging


# Basic runtime setup
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
random.seed(42)

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("spaCy model not found. Install with: python -m spacy download en_core_web_sm")


# Generic terms that are too broad to be useful study concepts
GENERIC_PHRASES = {
    "system", "systems", "task", "tasks",
    "study", "field", "building",
    "applications", "models", "model",
    "approach", "method", "process",
}

# Domain hints used to identify technical concepts
DOMAIN_HINTS = {
    "learning", "network", "networks",
    "intelligence", "data", "model",
    "algorithm", "neural",
}


# Identify concepts that are explicitly defined and contextually important
def extract_defined_concepts_with_context(text: str) -> set:
    """
    Identifies concepts that are explicitly defined and carry semantic weight
    within the lecture context.
    """
    doc = nlp(text)
    defined = []

    for sent in doc.sents:
        sentence = sent.text.strip().lower()
        match = re.match(r"^([a-z\s]{3,50})\s+(is|are|refers to|means)\b", sentence)

        if match:
            concept = re.sub(r"[^a-z\s]", "", match.group(1).strip())
            if 1 <= len(concept.split()) <= 3:
                defined.append(concept)

    concepts = set()
    for concept in defined:
        score = 0

        # Multi-word concepts are more likely to be meaningful
        if len(concept.split()) > 1:
            score += 1

        # Repeated usage suggests importance
        if len(re.findall(rf"\b{re.escape(concept)}\b", text.lower())) > 1:
            score += 1

        # Relationship language indicates conceptual relevance
        if re.search(
            rf"{re.escape(concept)}.*(subset|within|part of|used in|based on)",
            text.lower()
        ):
            score += 1

        # Domain-specific vocabulary boost
        if any(word in concept for word in DOMAIN_HINTS):
            score += 1

        if score >= 1:
            concepts.add(concept)

    return concepts


# Extract core study concepts using noun phrases and contextual validation
def extract_keywords(text: str, max_keywords: int = 8) -> List[str]:
    """
    Extracts study-worthy concepts by combining noun phrase analysis
    with definition-aware filtering.
    """
    if not text or len(text.split()) < 50:
        return []

    doc = nlp(text)
    candidates = []
    defined_concepts = extract_defined_concepts_with_context(text)

    for chunk in doc.noun_chunks:
        phrase = re.sub(r"[^a-z\s]", "", chunk.text.lower().strip())

        if phrase == "datum":
            phrase = "data"

        if (
            len(phrase.split()) <= 3
            and len(phrase) > 4
            and phrase not in GENERIC_PHRASES
            and not phrase.startswith(("a ", "the "))
        ):
            candidates.append(phrase)

    freq = Counter(candidates)
    keywords = []

    for kw, count in freq.most_common(max_keywords):
        if count > 1 or len(kw.split()) > 1 or kw in defined_concepts:
            keywords.append(kw)

    logging.info(f"Extracted keywords: {keywords}")
    return keywords


# Extract strict conceptual definitions (not usage descriptions)
def extract_definitions(text: str, keywords: List[str]) -> Dict[str, str]:
    """
    Extracts explicit conceptual definitions while excluding usage-based sentences.
    """
    doc = nlp(text)
    definitions = {}

    excluded_terms = {"system", "systems", "application", "applications"}
    excluded_phrases = {"used in", "widely used", "applied in", "used for"}

    for sent in doc.sents:
        sentence = sent.text.strip()
        lower = sentence.lower()

        if len(sentence.split()) < 6:
            continue

        match = re.match(r"^([a-z\s]{3,50})\s+(is|are|refers to|means)\b", lower)
        if not match:
            continue

        concept = re.sub(r"[^a-z\s]", "", match.group(1).strip())

        if concept.split()[-1] in excluded_terms:
            continue

        if any(p in lower for p in excluded_phrases):
            continue

        if 1 <= len(concept.split()) <= 3:
            definitions[concept] = sentence

    return definitions


# Generate definition-based multiple choice questions
def generate_definition_mcq(definitions: Dict[str, str]) -> List[Dict]:
    """
    Generates MCQs only for concepts with valid, explicit definitions.
    """
    questions = []

    for concept, definition in definitions.items():
        distractors = [d for k, d in definitions.items() if k != concept]
        if len(distractors) < 3:
            continue

        options = random.sample(distractors, 3) + [definition]
        random.shuffle(options)

        questions.append({
            "question": f"Which of the following best defines '{concept}'?",
            "answer": definition,
            "options": options
        })

    return questions


# Collect sentences that provide meaningful context for each concept
def extract_concept_sentences(text: str, keywords: List[str]) -> Dict[str, List[str]]:
    """
    Maps concepts to sentences where they appear in explanatory contexts.
    """
    doc = nlp(text)
    concept_sentences = {}

    for sent in doc.sents:
        sentence = sent.text.strip()
        lower = sentence.lower()

        if len(sentence.split()) < 8:
            continue

        for kw in keywords:
            if re.search(rf"\b{re.escape(kw)}\b", lower):
                concept_sentences.setdefault(kw, []).append(sentence)

    return concept_sentences


# Generate reasoning-based conceptual MCQs
def generate_contextual_mcq(
    text: str,
    keywords: List[str],
    max_questions: int = 4
) -> List[Dict]:
    """
    Generates MCQs that test conceptual understanding rather than memorization.
    """
    concept_sentences = extract_concept_sentences(text, keywords)
    used = set()
    questions = []

    for concept, sentences in concept_sentences.items():
        sentence = random.choice(sentences)
        if sentence in used:
            continue

        used.add(sentence)

        distractors = [
            k for k in keywords
            if k != concept and len(k.split()) == len(concept.split())
        ]

        if len(distractors) < 3:
            distractors = [k for k in keywords if k != concept][:3]

        if len(distractors) < 3:
            continue

        options = random.sample(distractors, 3) + [concept]
        random.shuffle(options)

        questions.append({
            "question": "Which concept best fits the following statement?",
            "context": sentence,
            "answer": concept,
            "options": options
        })

        if len(questions) >= max_questions:
            break

    return questions


# Extract sufficiently informative sentences for reasoning tasks
def extract_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"[.!?]", text) if len(s.split()) > 7]


# Create minimally altered false statements for T/F questions
def create_false_statement(sentence: str, keywords: List[str]) -> Optional[str]:
    doc = nlp(sentence)
    nouns = [t for t in doc if t.pos_ == "NOUN"]
    if not nouns:
        return None

    target = random.choice(nouns)
    alternatives = [k for k in keywords if k != target.lemma_.lower()]
    if not alternatives:
        return None

    return sentence.replace(target.text, random.choice(alternatives), 1)


# Generate true/false questions based on sentence reasoning
def generate_true_false(
    text: str,
    keywords: List[str],
    max_questions: int = 4
) -> List[Dict]:
    """
    Generates reasoning-based true/false questions.
    """
    sentences = extract_sentences(text)
    results = []

    for s in random.sample(sentences, min(len(sentences), max_questions // 2)):
        results.append({"statement": s, "answer": "True"})
        false_s = create_false_statement(s, keywords)
        if false_s:
            results.append({"statement": false_s, "answer": "False"})

    return results


# Generate short-answer questions that encourage explanation and reasoning
def generate_short_answer(
    keywords: List[str],
    max_questions: int = 3
) -> List[str]:
    """
    Generates open-ended questions focused on explanation and reasoning.
    """
    templates = [
        "Explain the role of {kw} in artificial intelligence systems.",
        "Why is {kw} important in modern AI applications?",
        "How does {kw} contribute to intelligent behavior in machines?",
    ]

    return [
        random.choice(templates).format(kw=kw)
        for kw in random.sample(keywords, min(len(keywords), max_questions))
    ]
