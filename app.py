import streamlit as st
import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

from langchain_community.document_loaders import FileSystemBlobLoader
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import PyPDFParser

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# carregar variaveis de ambiente do aruqivo .env
_= load_dotenv()

# carrego modelo de linguagem (cache session)
@st.cache_resource
def llm_model():
    return ChatOpenAI(              # input cache  output
        model= "gpt-4o-mini",       # $0.15 $0.075 $0.60
        # model= "gpt-3.5-turbo",   # $0.50 $0.000 $1.50   
)

# carrego o modelo do vetor (cache session)
@st.cache_resource
def embedding_model():
    return OpenAIEmbeddings(   
        model="text-embedding-3-small",     # $0.02
        #model="text-embedding-ada-002",     # $0.10
        #model="text-embedding-3-large",     # $0.13
)

# carregos os documentos (cache session)
@st.cache_resource
def loader_document():
    loader= GenericLoader(
            blob_loader=FileSystemBlobLoader(
                path="./books",
                glob="*.pdf",
            ),
            blob_parser=PyPDFParser(),  
        )
    return loader.load()

# carrego modelo de linguagem
llm= llm_model()

# carrego o modelo do vetor
embeddings= embedding_model()

# carrego template prompt
# rag_template= """
# Você é um analista profissional do mercado financeiro.
# Seu trabalho é analisar o resultados das empresas por meio dos relatórios disponibilizados
# pelas empresas e passá-los para o cliente de forma clara e objetiva.
# Contexto: {context}
# Pergunta do cliente: {question}
# """

# carrego template prompt
rag_template= """
Você é um companheiro amigável e compreensível.
Seu trabalho é ser uma ótima companhia para conversar, entender o problema dos outros e buscar pelos melhores conselhos
e palavras de conforto.
Contexto: {context}
Pergunta do cliente: {question}
"""

# sidebar

# obtendo arquivos para analise
with st.sidebar: 

    uploaded_file = st.file_uploader(
        "Entre com um documento para análise", 
        type=("pdf"),
        accept_multiple_files= True
    )
    # obtendo o contexto
    if len(uploaded_file) > 0:

        print("msn-1")
        print("\n")    
        print(uploaded_file[0])
        print("\n")          

        # carregando os documentos
        documents= loader_document()

        # vetorizando os documentos
        vectorstore= FAISS.from_documents(documents, embeddings)
        retriever= vectorstore.as_retriever()        

# body

# titulo
st.title("📜 Atena") 
st.caption("🚀 Chatbot para análise documentos!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# obtendo a pergunta
question = st.text_input(
    "",
    placeholder="Pergunte qualquer coisa sobre o documento",
    disabled=not uploaded_file
)

if (len(uploaded_file) > 0) and question != "":
    
    # definindo o prompt
    prompt= ChatPromptTemplate.from_template(rag_template)
    chain= (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # obtendo respota
    response= chain.invoke(question)
    
    msg = response.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)



