import sys
import string
import re

from keras.models import load_model
from keras.preprocessing import sequence
from preprocessor.preprocess_text import clean

from models.cnn import ConvolutionalNet

import os

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

MATCH_MULTIPLE_SPACES = re.compile("\ {2,}")
SEQUENCE_LENGTH = 20
EMBEDDING_DIMENSION = 30

UNK = "<UNK>"
PAD = "<PAD>"

vocabulary = open("data/vocabulary.txt").read().split("\n")
inverse_vocabulary = dict((word, i) for i, word in enumerate(vocabulary))


def words_to_indices(inverse_vocabulary, words):
    return [inverse_vocabulary.get(word, inverse_vocabulary[UNK]) for word in words]


class Predictor (object):
    def __init__(self, model_path):
        model = ConvolutionalNet(vocabulary_size=len(
            vocabulary), embedding_dimension=EMBEDDING_DIMENSION, input_length=SEQUENCE_LENGTH)
        model.load_weights(model_path)
        self.model = model

    def predict(self, headline):
        headline = headline.encode("ascii", "ignore")
        inputs = sequence.pad_sequences([words_to_indices(
            inverse_vocabulary, clean(headline).lower().split())], maxlen=SEQUENCE_LENGTH)
        clickbait_value = self.model.predict(inputs)[0, 0]
        return round(clickbait_value * 100, 2)


predictor = Predictor("models/detector.h5")
predictor.predict("hello")
# if __name__ == "__main__":
#     print(
#         round(predictor.predict(sys.argv[1]) * 100, 2))
#     print(
#         round(predictor.predict(sys.argv[1]) * 100, 2))
#     print(
#         round(predictor.predict(sys.argv[1]) * 100, 2))
