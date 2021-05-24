from nltk.corpus import stopwords
from gensim import corpora
import gensim.downloader as api
from gensim.models import WordEmbeddingSimilarityIndex
from gensim.similarities import SparseTermSimilarityMatrix

class Similarity:
    def __init__(self):
        self.stop_words = stopwords.words('english')
        self.w2v_model = api.load("glove-wiki-gigaword-50")
        self.similarity_index = WordEmbeddingSimilarityIndex(self.w2v_model)

    def make_document(self, headline, articles):
        temp = []
        headline = [w for w in headline.lower().split() if w not in self.stop_words]
        for article in articles:
            article = [w for w in article.lower().split() if w not in self.stop_words]
            temp.append(article)
        self.documents = [headline] + temp
        dictionary = corpora.Dictionary(self.documents)
        self.similarity_matrix = SparseTermSimilarityMatrix(self.similarity_index, dictionary)
        headline = dictionary.doc2bow(headline)
        articles = [dictionary.doc2bow(i) for i in temp]
        similarities = []
        for i in articles:
            similarities.append(self.get_similarity(headline, i))
        return similarities
    
    def get_similarity(self, s1, s2):
        return self.similarity_matrix.inner_product(s1, s2, normalized=True)
    