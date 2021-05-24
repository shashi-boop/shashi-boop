from similarity import Similarity

headline = "Obama speaks to the media in Illinois"

news = ["Obama speaks to the media in Illinois",
        "The president greets the press in Chicago",
        "Having a tough time finding an orange juice press machine?"]

a = Similarity().make_document(headline, news)
print(a)