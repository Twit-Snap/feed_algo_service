import string
import re

import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from typing import List, Tuple

class TopicExtractor:
    def __init__(self):
        self.__english_stopwords = set(stopwords.words('english'))
        self.__word_frequency = {}
        self.__frequency_sorted = False

    def __clean_tweet_content(self, tweet_content : str):
        # Remove punctiation
        cleaned_content = "".join([char if char not in string.punctuation else ' ' for char in tweet_content])

        # Remove multiple spaces
        cleaned_content = re.sub('\\s+', ' ', cleaned_content)

        # Lowercase the text
        cleaned_content = cleaned_content.lower()

        # Split the twit into words
        words = word_tokenize(cleaned_content)

        # Remove Stopwords in the twit
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        # Remove leftover non-alphabetic words from stopword removal
        words = [word for word in words if word.isalpha()]

        cleaned_text = ' '.join(words)
        return cleaned_text

    def load_twit_content(self, tweets_data: List[Tuple[str, str]]):
        cleaned_twits = [self.__clean_tweet_content(tweet_content) for _, tweet_content in tweets_data]
        for twit in cleaned_twits:
            for word in twit.split():
                if word in self.__word_frequency:
                    self.__word_frequency[word] += 1
                else:
                    self.__word_frequency[word] = 1
        self.__frequency_sorted = False

    def extract_topics(self, n_topics: int = 5):
        if len(self.__word_frequency) < n_topics:
            return list(self.__word_frequency.keys())

        # Sort the words by frequency if not already sorted
        if not self.__frequency_sorted:
            self.__word_frequency = {k: v for k, v in sorted(self.__word_frequency.items(), key=lambda item: item[1], reverse=True)}
            self.__frequency_sorted = True

        return list(self.__word_frequency.keys())[:n_topics]

topic_extractor = TopicExtractor()