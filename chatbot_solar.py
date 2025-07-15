
# from langchain_openai import OpenAI # Para interagir com a API da OpenAI via LangChain
from langchain_google_genai import ChatGoogleGenerativeAI # Para interagir com a API Gemini
from langchain.prompts import PromptTemplate # Para criar templates de prompt
from langchain.chains import LLMChain # Para encadear o LLM com o prompt
from dotenv import load_dotenv # Para carregar variáveis de ambiente do .env
import os # Para acessar variáveis de ambiente

import os

load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY") # Obtém a chave da API do Google

# llm = OpenAI(api_key=api_key)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=google_api_key, temperature=0.7)



template = """Você é um assistente prestativo e informativo especializado em energia solar.
Responda à pergunta do usuário com base nas informações fornecidas sobre energia solar.
Se a pergunta não for sobre energia solar ou se você não tiver informações para responder, diga que não pode ajudar com essa questão.

Informações sobre Energia Solar:
{context}

Pergunta do usuário: {question}
Resposta:
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

with open("solar_info.txt", "r", encoding="utf-8") as f:
    solar_context = f.read()
    
    

from langchain.chains import LLMChain

qa_chain = LLMChain(llm=llm, prompt=prompt)


def chat_solar():
    print("Olá! Sou seu assistente de energia solar. Pergunte o que quiser (digite 'sair' para encerrar).")
    while True:
        user_input = input("Sua pergunta: ")
        if user_input.lower() == 'sair':
            print("Até logo!")
            break

        response = qa_chain.run(context=solar_context, question=user_input)
        print(f"Assistente: {response.strip()}")

if __name__ == "__main__":
    chat_solar()