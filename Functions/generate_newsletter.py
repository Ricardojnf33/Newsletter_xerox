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
