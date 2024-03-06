from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import GPT4AllEmbeddings

embedding = GPT4AllEmbeddings()
vectorstore = Chroma(persist_directory="storage/test/chroma", embedding_function=embedding)
vectorstore.delete_collection()
