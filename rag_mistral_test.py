from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain import hub
from langchain_core.output_parsers import StrOutputParser
import sys

def runRAG():
  llm = Ollama(model="mistral")

  query = """Hva er meningen med livet? Svar på norsk. 
  Vær litt spøkefull, og få inn noen referanser til Monty Python, samt Hitchhiker's Guide to the Galaxy.
  Formater det som et mermaid diagram."""
  embedding = GPT4AllEmbeddings()
  vectorstore = Chroma(persist_directory="storage/test/chroma", embedding_function=embedding)
  # if arg = "del", delete the index
  
  question = "Tell me what you know of Motril"
  retriever = vectorstore.as_retriever()
  
  documents = retriever.get_relevant_documents(question)
  
  # documents = vectorstore.similarity_search(question)
  
  prompt = hub.pull("rlm/rag-prompt")

  rag_chain = prompt | llm | StrOutputParser()

    # Run
  # chain = rag_chain.invoke({"context": documents, "question": question})
  # print(generation)
  # return {"keys": {"documents": documents, "local": local, "question": question}}
  for chunk in rag_chain.invoke({"context": documents, "question": question}):
    print(chunk, end="", flush=True)

def main():
  print("Hello, World!")
  return

if __name__ == "__main__":
  runRAG()