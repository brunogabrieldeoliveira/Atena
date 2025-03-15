from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

_= load_dotenv()

"""
# lendo um arquivo
loader= PyPDFLoader(
    file_path= "FIQE3_3T24.pdf",
)
"""

# lendo varios arquivos
loader = GenericLoader(
    blob_loader=FileSystemBlobLoader(
        path="./",
        glob="*.pdf",
    ),
    blob_parser=PyPDFParser(),
)

documents= loader.load()

embeddings= OpenAIEmbeddings(   
    model="text-embedding-3-small",     # $0.02
    #model="text-embedding-ada-002",     # $0.10
    #model="text-embedding-3-large",     # $0.13
)
vectorstore= FAISS.from_documents(documents, embeddings)
retriever= vectorstore.as_retriever()

# Modelo de linguagem           custo
llm= ChatOpenAI(                # input cache  output
    model= "gpt-4o-mini",       # $0.15 $0.075 $0.60
    # model= "gpt-3.5-turbo",   # $0.50 $0.000 $1.50
   
)

rag_template= """
Você é um analista profissional do mercado financeiro.
Seu trabalho é analisar o resultados das empresas por meio da dos relatórios de disponibilizados
pelas empresas e passá-las para o cliente de forma clara e objetiva.

Contexto: {context}

Pergunta do cliente: {question}
"""

prompt= ChatPromptTemplate.from_template(rag_template)
chain= (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

while True:
    user_input= input("Você: ")
    response= chain.invoke(user_input)
    print(response.content)






