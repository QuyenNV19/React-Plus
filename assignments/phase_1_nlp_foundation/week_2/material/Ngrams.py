from sklearn.feature_extraction.text import CountVectorizer

text = ['NLP has changed the world', 'I love NLP', 'NLP is cool', 'NLP is future']

vectorizer = CountVectorizer(ngram_range=(2,2))

X = vectorizer.fit_transform(text)

print(vectorizer.get_feature_names_out())
print(X.toarray())