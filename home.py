# Importações
import imaplib
import email
from bs4 import BeautifulSoup
import re  
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import pinecone
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#Função de Web Scraping do Gmail
def scrape_gmail(user, password):
  
  # Faz conexão segura com servidor IMAP do Gmail
  imap = imaplib.IMAP4_SSL("imap.gmail.com") 
  
  # Efetua login com as credenciais fornecidas
  imap.login(user, password)

  # Seleciona inbox
  imap.select("INBOX") 

  # Procura por emails não lidos com tag "newsletter" na data de hoje
  search = imap.search(None, '(UNSEEN TAG "newsletter") ON "05-Aug-2023"')

  # Busca IDs das mensagens encontradas
  ids = search[1][0].decode("utf-8").split()

  # Inicializa lista para armazenar conteúdo dos emails
  all_email_text = []

  # Itera sobre os IDs
  for id in ids:
      
    # Busca o dado bruto do email pelo ID
    _, data = imap.fetch(id, "(RFC822)") 

    # Converte dados brutos em objeto email    
    email_data = data[0][1]
    email_message = email.message_from_bytes(email_data)

    # Extrai o corpo do email
    body = email_message.get_payload()
    soup = BeautifulSoup(body, "html.parser")
    text = soup.get_text()

    # Adiciona à lista de conteúdos 
    all_email_text.append(text)

  # Desconecta do servidor
  imap.close()
  imap.logout()

  # Retorna conteúdo concatenado
  return ". ".join(all_email_text)

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

# Função para gerar texto da newsletter   
def generate_newsletter(topics):

  # Cria estrutura da newsletter 
  newsletter = f"""
  <h1>Newsletter diária sobre tecnologia</h1>

  <h3>Tópicos de hoje</h3>

  <h4>Tópico 1</h4>

  Conteúdo sobre tópico 1

  <h4>Tópico 2</h4>

  Conteúdo sobre tópico 2  

  <h4>Tópico 3</h4>

  Conteúdo sobre tópico 3

  <h5>Esperamos que tenha gostado!</h5> 
  """

  # Preenche tópicos na estrutura
  for i, topic in enumerate(topics):
    title = f"Tópico {i+1}"
    keywords = " ".join(topic)
    paragraph = f"Esse tópico é sobre {keywords}"
    newsletter = newsletter.replace(title, f"<h4>{title}</h4>{paragraph}", 1)

  # Retorna texto da newsletter
  return newsletter
  
# Função para enviar newsletter por email  
def send_newsletter(newsletter_html, sender, password, recipient):

  # Cria mensagem
  message = MIMEMultipart()
  message["From"] = sender
  message["To"] =  recipient
  message["Subject"] = "Sua newsletter diária"  

  # Adiciona corpo da newsletter em HTML
  part = MIMEText(newsletter_html, "html")
  message.attach(part)

  # Cria conexão SMTP segura e envia mensagem
  with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender, password)  
    server.sendmail(
      sender, recipient, message.as_string()
    )

# Função principal    
def main():

  # Credenciais do Gmail
  sender = "sender@email.com" 
  password = "senha123"

  # Email destinatário 
  recipient = "recipient@email.com"

  # Extração de conteúdo dos emails
  raw_text = scrape_gmail(sender, password)

  # Pré-processamento do texto
  processed_text = preprocess_text(raw_text)

  # Extração de tópicos
  topics = extract_topics_lda(processed_text)

  # Geração da newsletter
  newsletter_html = generate_newsletter(topics)
  
  # Envio da newsletter
  send_newsletter(newsletter_html, sender, password, recipient)

  print("Newsletter gerada e enviada com sucesso!")

if __name__ == "__main__":
  main()
