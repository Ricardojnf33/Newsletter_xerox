import imaplib
import email
from bs4 import BeautifulSoup

# Função de Web Scraping do Gmail
def scrape_gmail(user, password):
    # Faz conexão segura com servidor IMAP do Gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com") 
    
    # Efetua login com as credenciais fornecidas
    imap.login(user, password)

    # Seleciona inbox
    imap.select("INBOX") 

    # Montando o comando de pesquisa corretamente
    search_query = '(UNSEEN TAG "newsletter")'

    # Faz a pesquisa
    typ, data = imap.search(None, search_query)
    ids = data[0].split()

    # Inicializa lista para armazenar conteúdo dos emails
    all_email_text = []

    # Itera sobre os IDs
    for id in ids:
        # Busca o dado bruto do email pelo ID
        typ, data = imap.fetch(id, "(RFC822)") 

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

