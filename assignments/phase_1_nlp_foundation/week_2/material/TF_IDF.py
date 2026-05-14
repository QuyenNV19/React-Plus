from sklearn.feature_extraction.text import TfidfVectorizer

text = ['NLP has changed the world', 'I love NLP', 'NLP is cool', 'NLP is future']

tf = TfidfVectorizer()
txt_fit = tf.fit(text)

txt_transform = txt_fit.transform(text)

idf = tf.idf_

print(dict(zip(txt_fit.get_feature_names_out(), idf)))

