# chatbot_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=google_api_key)

with open("solar_info.txt", "r", encoding="utf-8") as f:
    solar_context = f.read()

template = """
Você é um assistente prestativo e informativo especializado em energia solar.
Responda à pergunta do usuário com base nas informações fornecidas sobre energia solar.
Se a pergunta não for sobre energia solar ou se você não tiver informações para responder, diga que não pode ajudar com essa questão.

Informações sobre Energia Solar:
{context}

Pergunta do usuário: {question}
Resposta:
"""

prompt = PromptTemplate(template=template, input_variables=["context", "question"])
qa_chain = LLMChain(llm=llm, prompt=prompt)

app = FastAPI()

class Question(BaseModel):
    question: str

@app.post("/ask")
def ask_solar(q: Question):
    answer = qa_chain.run(context=solar_context, question=q.question)
    return {"response": answer.strip()}
