# Função principal    
def main():

  # Credenciais do Gmail
  sender = "ricardo.jnf1@gmail.com" 
  password = "wsdaoztnleortmvj"

  # Email destinatário 
  recipient = "cheetahdatascience@gmail.com"

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
