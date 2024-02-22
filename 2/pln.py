from pypdf import PdfReader
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

# Lendo o arquivo PDF
reader = PdfReader("artigos/web/Strategies_for_web_application_development_methodologies.pdf")
number_of_pages = len(reader.pages)
page = reader.pages[0]
text = page.extract_text()
# print(text)

# Tokenização
tokens = word_tokenize(text)
# print(tokens)

# Remoção de stopwords
stop_words = set(stopwords.words('english'))
tokens = [word for word in tokens if word.lower() not in stop_words]
# print(tokens)

# Stemming
stemmer = SnowballStemmer('english')
tokens = [stemmer.stem(word) for word in tokens]
# print(tokens)

# Lematização
lemmatizer = WordNetLemmatizer()
tokens = [lemmatizer.lemmatize(word) for word in tokens]
# print(tokens)

# Frequência

freq = nltk.FreqDist(tokens)
print('Frequência de palavras')
print(freq.most_common(10))
print('-------------------------------------')
# freq.plot(10, cumulative=False)

# # Bigramas
bigrams = list(nltk.bigrams(tokens))
# print(bigrams)
freq_bigrams = nltk.FreqDist(bigrams)
print('Frequência de bigramas')
print(freq_bigrams.most_common(10))
print('-------------------------------------')
# freq_bigrams.plot(10, cumulative=False)

# # Trigramas
trigrams = list(nltk.trigrams(tokens))
# print(trigrams)
freq_trigrams = nltk.FreqDist(trigrams)
print('Frequência de trigramas')
print(freq_trigrams.most_common(10))
print('-------------------------------------')
# freq_trigrams.plot(10, cumulative=False)

