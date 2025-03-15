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

        # lendo varios arquivos
        loader = GenericLoader(
            blob_loader=FileSystemBlobLoader(
                path="./",
                glob="*.pdf",
            ),
            blob_parser=PyPDFParser(),  
        )

        # carregando os documentos
        documents= loader.load()
        embeddings= OpenAIEmbeddings(   

            model="text-embedding-3-small",     # $0.02
            #model="text-embedding-ada-002",     # $0.10
            #model="text-embedding-3-large",     # $0.13
        )

        # vetorizando os documentos
        vectorstore= FAISS.from_documents(documents, embeddings)
        retriever= vectorstore.as_retriever()


# body

# titulo
st.title("📝 Atena")
st.caption("🚀 Chatbot para análise documentos!")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# obtendo a pergunta
question = st.text_input(
    "",
    placeholder="Pergunte qualquer coisa sobre o documento",
    disabled=not uploaded_file
)

if len(uploaded_file) > 0:
    
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

    # definindo prompt
    prompt= ChatPromptTemplate.from_template(rag_template)
    chain= (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    # obtendo respota
    response= chain.invoke({"input": question})

    msg = response.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)



