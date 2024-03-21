from flask import Flask, render_template, request, redirect, url_for
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS

load_dotenv()
os.getenv("GOOGLE_API_KEY")

app = Flask(__name__)

# Define functions for interacting with LangChain

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
    return response["output_text"]

# Define Flask routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Process registration form submission
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        # Additional validation and registration logic can be added here
        return redirect(url_for('disease_recommendation'))
    return render_template('register.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Process sign-in form submission
        email_or_phone = request.form['email_or_phone']
        password = request.form['password']
        # Additional validation and sign-in logic can be added here
        return redirect(url_for('disease_recommendation'))
    return render_template('signin.html')

@app.route('/disease-recommendation', methods=['GET', 'POST'])
def disease_recommendation():
    if request.method == 'POST':
        user_question = request.form['user_question']
        response = user_input(user_question)
        return render_template('disease.html', response=response)
    return render_template('disease.html', response=None)

if __name__ == '__main__':
    app.run(debug=True)
