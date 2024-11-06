import string
import re
import os

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

        # Open the file of filtered adjectives and nouns and add them to the stopwords
        with open(os.path.join(os.path.dirname(__file__), 'filters/filtered_adjectives.txt')) as f:
            adjectives = [line.strip() for line in f]
            self.__english_stopwords.update(adjectives)

        with open(os.path.join(os.path.dirname(__file__), 'filters/filtered_nouns.txt')) as f:
            nouns = [line.strip() for line in f]
            self.__english_stopwords.update(nouns)

        self.__word_frequency = {}
        self.__frequency_sorted = False

    def __clean_tweet_content(self, tweet_content : str):
        # Remove punctiation
        cleaned_content = "".join([char if char not in string.punctuation else ' ' for char in tweet_content])

        # Remove multiple spaces
        cleaned_content = re.sub('\\s+', ' ', cleaned_content)

        # Remove # from the twit content so that hashtags can be treated as normal words
        cleaned_content = cleaned_content.replace('#', '')

        # Lowercase the text
        cleaned_content = cleaned_content.lower()

        # Split the twit into words
        words = word_tokenize(cleaned_content)

        # Remove Stopwords in the twit
        words = [w for w in words if not w in self.__english_stopwords]

        # Remove leftover non-alphabetic words from stopword removal
        words = [word for word in words if word.isalpha()]

        cleaned_text = ' '.join(words)
        return cleaned_text

    def load_twit_content(self, tweets_data: List[Tuple[str, str]]):
        cleaned_twits = [self.__clean_tweet_content(tweet_content) for _, tweet_content in tweets_data]

        self.__word_frequency = {}
        self.__frequency_sorted = False

        for twit in cleaned_twits:
            # Make a set out of the filtered twit to ensure that each twit can only add to the frequency of a word once
            for word in set(twit.split()):
                if word in self.__word_frequency:
                    self.__word_frequency[word] += 1
                else:
                    self.__word_frequency[word] = 1
        self.__frequency_sorted = False

    def extract_topics(self, n_topics: int = 5):
        if len(self.__word_frequency) < n_topics:
            return [{word: freq} for word, freq in self.__word_frequency.items()]

        # Sort the words by frequency if not already sorted
        if not self.__frequency_sorted:
            self.__word_frequency = {k: v for k, v in sorted(self.__word_frequency.items(), key=lambda item: item[1], reverse=True)}
            self.__frequency_sorted = True

        return [{word: freq} for word, freq in list(self.__word_frequency.items())[:n_topics]]

topic_extractor = TopicExtractor()