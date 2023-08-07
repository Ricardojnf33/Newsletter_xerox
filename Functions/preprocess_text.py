# Importações
import re 
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Função para pré-processar texto 
def preprocess_text(text):
  
  # Converte para lowercase
  text = text.lower()

  # Remove pontuações e numerais
  text = re.sub(r'[^\w\s]', '', text)

  # Tokeniza o texto
  tokens = word_tokenize(text)

  # Remove stopwords
  stop_words = set(stopwords.words("english"))
  tokens = [token for token in tokens if token not in stop_words]

  # Aplica lematização nos tokens
  lemmatizer = WordNetLemmatizer()
  tokens = [lemmatizer.lemmatize(token) for token in tokens]

  # Retorna texto pré-processado
  return " ".join(tokens)
