from sklearn.feature_extraction.text import CountVectorizer
document = ["NLP has changed the world. I love NLP. NLP is cool"]

vectorizer = CountVectorizer()

# tokenize and build vocabulary
vectorizer.fit(document)
print(vectorizer.vocabulary_)

# encode document
vector = vectorizer.transform(document)

# summarize encoded vector
print(vector.toarray())