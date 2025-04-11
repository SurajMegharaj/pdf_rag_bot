'''
File Name : rag.py
Author : Suraj J
Created On : 11-04-2025
Description :  
               - Initialize the embeddings
               - Function vectorize() to create a vectorstore to vectorize pdf file
               - Function to provide response for the asked query
'''
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from langchain.chains import RetrivalQA

class rag:
    def __init__(self):
        self.embeddings = HuggingFaceBgeEmbeddings(repo_id = 'sentence-transformers/all-MiniLM-L6-v2')


    def vectorize(self,pdfpath):
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50
        )
        docs = text_splitter.split_documents(documents)
        vectordb = FAISS.from_documents(docs, self.embeddings)

        retriever = vectordb.as_retriever()
        return retriever
    
    def generate_answers(self,retriever,query):
        llm = HuggingFaceHub(
            repo_id = 'google/flan-t5-base',
            model_kwargs = {'temperature':0.2, 'max_length':512}
        )

        qa_chain = RetrivalQA.from_chain_type(
            llm=llm,
            retriver = retriever,
            chain_type = 'stuff'
        )

        result = qa_chain.run(query)
        return result

