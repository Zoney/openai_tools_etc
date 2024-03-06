from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import sys
import pathlib
from asyncio import run as run_async
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
import glob


file_path = "storage/test/test/"

def read_directory(directory_path):
        entries = pathlib.Path(directory_path).iterdir()
        for entry in entries:
          print(f'Found entry: {entry}')
          if entry.is_dir():
              print(f'Found directory: {entry}')
              read_directory(entry)
              process_directory(entry)
def process_directory(directory_path):
  try:
        print(f'Processing directory: {directory_path}')
        docs = []
        pdf_files = glob.glob(str(directory_path / "*.pdf"))
        txt_files = glob.glob(str(directory_path / "*.txt"))
        print(f'number of txt files in {directory_path}: {len(txt_files)}')
        for txt_file in txt_files:
          print(f'Processing TXT file: {txt_file}')
          txt_loader = TextLoader(txt_file)
          txt_docs = txt_loader.load()
          docs.extend(txt_docs)
          
        for pdf_file in pdf_files:
          print(f'Processing PDF file: {pdf_file}')
          pdf_loader = UnstructuredPDFLoader(pdf_file)
          pdf_docs = pdf_loader.load()
          docs.extend(pdf_docs)

        print(f'Loaded documents: {docs}')
        if(len(docs) == 0):
            print(f'No documents to process')
            return
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=500, chunk_overlap=100
        )
        all_splits = text_splitter.split_documents(docs)
        print(f'All splits: {all_splits}')

        embedding = GPT4AllEmbeddings()

        # Indexdb2 = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")

        vectorstore = Chroma.from_documents(
          all_splits,
          embedding,
          persist_directory="storage/test/chroma"
        )
  except Exception as e:
    print(f'Error processing directory: {directory_path} - {e}')

        # Print collection statistics
        # print(vectorstore.stats())

        # index = vectorstore.Index("test-index")

        # if text_splitter and len(docs) > 0:
        #     # embed the PDF documents
        #     vectorstore.from_documents(all_splits, embedding, {
        #         'textKey': "text",
        #     })
        # else:
        #     print("No documents to embed")
  

def main():
    print(sys.argv)
    # if args[2].lower() == 'purge':
    #     print(f'Purging namespace: {arg1}')
    #     return

    current_dir = os.getcwd()
    directory_path = f'{current_dir}/{file_path}'
    read_directory(directory_path)

    print("ingestion complete")

if __name__ == "__main__":
  main()
