# app.py

import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import uuid

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_text(pdf_files):
    text = ""
    for pdf_file in pdf_files:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "You have a mild Infection ,consult with a nearby doctor.", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """

    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)
    chain = get_conversational_chain()
    response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)
    st.write("Reply: ", response["output_text"])

def main():
    st.set_page_config(layout="wide", page_icon='/home/sandeep/Desktop/HACK/NEW/2.png')
    st.write("<p style='font-size: 40px; color: grey; font-weight: bold;'>TECHTURTLES</p>", unsafe_allow_html=True)
    st.write("---")
    st.write("###") 
    
    # Sidebar for registration
    with st.sidebar:
        st.title("Registration")

        username_register = st.text_input("Username")
        email_register = st.text_input("Email", placeholder="Enter your email (e.g., example@domain.com)")
        password = st.text_input("Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")

        if password != confirm_password:
            st.error("Passwords do not match!")
            return

        if st.button("Register"):
            st.success("Registration successful! Redirecting...")

            # Navigate to the Streamlit page with PDF processing functionality
            st.experimental_set_query_params(next_page="streamlit_page")

    user_question = st.text_input("ADD SYMPTOMS!!!")
    st.write("---")

    # Specify PDF files directly here
    pdf_files = ["/home/sandeep/Desktop/HACK/hii.pdf"]

    with st.spinner("Welcome..."):
        # Extract text from PDF files
        raw_text = get_pdf_text(pdf_files)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)

    if user_question:
        user_input(user_question)

if __name__ == "__main__":
    main()
