from langchain_community.llms import Ollama

llm = Ollama(model="mistral")

query = """Hva er meningen med livet? Svar på norsk. 
Vær litt spøkefull, og få inn noen referanser til Monty Python, samt Hitchhiker's Guide to the Galaxy.
Formater det som et mermaid diagram."""
  
for chunk in llm.stream(query):
  print(chunk, end="", flush=True)
