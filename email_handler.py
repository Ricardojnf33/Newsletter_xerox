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
