import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import random

nltk.download('punkt')
nltk.download('stopwords')

def generate_fill_in_blank(sentence):
    words = word_tokenize(sentence)
    words = [w for w in words if w.isalnum()]
    if not words:
        return None

    blank_word = random.choice(words)
    return sentence.replace(blank_word, "_____"), blank_word

def generate_mcq(sentence):
    words = word_tokenize(sentence)
    words = [w for w in words if w.isalnum()]
    correct = random.choice(words)
    options = [correct]
    while len(options) < 4:
        fake = random.choice(words)
        if fake not in options:
            options.append(fake)
    random.shuffle(options)
    return sentence.replace(correct, "_____"), correct, options
