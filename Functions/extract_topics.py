# Importações
import sklearn
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Função para extrair tópicos com LDA
def extract_topics_lda(processed_text, num_topics=5):
  
  # Cria bag of words
  cv = CountVectorizer() 
  X = cv.fit_transform(processed_text)

  # Treina modelo LDA
  lda = LatentDirichletAllocation(n_components=num_topics)
  lda.fit(X)

  # Extrai tópicos principais
  topic_keywords = []
  for topic_idx, topic in enumerate(lda.components_):
    topic_keywords.append([cv.get_feature_names_out()[i] for i in topic.argsort()[:-5 - 1:-1]])
  
  # Retorna tópicos encontrados
  return topic_keywords
