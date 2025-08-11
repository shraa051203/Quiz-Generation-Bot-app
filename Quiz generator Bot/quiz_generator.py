import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import random

nltk.download('punkt')
nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

def generate_fill_in_blanks(text):
    questions = []
    sentences = sent_tokenize(text)

    for sentence in sentences:
        words = word_tokenize(sentence)
        content_words = [w for w in words if w.isalnum() and w.lower() not in stop_words]
        if not content_words:
            continue
        blank_word = random.choice(content_words)
        question = sentence.replace(blank_word, "_____")
        questions.append((question, blank_word))
    return questions

def generate_mcqs(text):
    questions = []
    sentences = sent_tokenize(text)

    for sentence in sentences:
        words = word_tokenize(sentence)
        content_words = [w for w in words if w.isalnum() and w.lower() not in stop_words]
        if len(set(content_words)) < 4:
            continue
        correct = random.choice(content_words)
        options = [correct]
        while len(options) < 4:
            fake = random.choice(content_words)
            if fake not in options:
                options.append(fake)
        random.shuffle(options)
        labeled_options = {chr(65 + i): opt for i, opt in enumerate(options)}  # A, B, C, D
        question = sentence.replace(correct, "_____")
        questions.append((question, correct, labeled_options))
    return questions
