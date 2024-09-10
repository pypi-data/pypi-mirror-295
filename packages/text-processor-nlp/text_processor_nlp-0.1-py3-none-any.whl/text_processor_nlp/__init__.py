import re
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.tokens import Doc, Token

class TextPreprocessor:
    def __init__(self):
        # Load spaCy model
        self.nlp = spacy.load("en_core_web_sm")

    def text_cleaning(self, text: str) -> str:
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        # Remove special characters and extra whitespaces
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def lowercasing(self, text: str) -> str:
        return text.lower()

    def tokenization(self, text: str):
        doc = self.nlp(text)
        # Word Tokenization
        word_tokens = [token.text for token in doc]
        # Sentence Tokenization
        sentence_tokens = [sent.text for sent in doc.sents]
        return word_tokens, sentence_tokens

    def remove_stop_words(self, tokens):
        return [token for token in tokens if token.lower() not in STOP_WORDS]

    def normalization(self, tokens):
        doc = self.nlp(' '.join(tokens))
        # Lemmatization
        lemmatized_tokens = [token.lemma_ for token in doc]
        return lemmatized_tokens

    def handle_punctuation(self, text: str) -> str:
        return re.sub(r'[^\w\s]', '', text)

    def remove_numbers(self, text: str) -> str:
        return re.sub(r'\d+', '', text)


    def preprocess(self, text: str):
        # Apply all preprocessing steps
        text = self.text_cleaning(text)
        text = self.lowercasing(text)
        word_tokens, sentence_tokens = self.tokenization(text)
        word_tokens = self.remove_stop_words(word_tokens)
        word_tokens = self.normalization(word_tokens)
        text = ' '.join(word_tokens)
        text = self.handle_punctuation(text)
        text = self.remove_numbers(text)
        return text, word_tokens, sentence_tokens
