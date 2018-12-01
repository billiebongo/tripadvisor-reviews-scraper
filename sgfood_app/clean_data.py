#clean the restaurant names and reviews before indexing
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
#import from the database
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
stop_words = stopwords.words('english')


#create the json and post

def clean_review(review):
	wordnet_lemmatizer = WordNetLemmatizer()
	#tokenize\
	tokens = word_tokenize(review) #by whitespace
	#print(tokens)
	words = [word for word in tokens if word.isalpha()] #remove punctuation
	#lower
	words = [word.lower() for word in words]
	#stopw words: https://www.ranks.nl/stopwords
	words = [w for w in words if not w in stop_words]
	#porterstem
	#print(words)
	#stemmer2 = SnowballStemmer("english", ignore_stopwords=True)

	words = [wordnet_lemmatizer.lemmatize(w) for w in words]


	return words



