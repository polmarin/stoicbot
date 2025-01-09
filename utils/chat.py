from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFaceHub
from langchain_community.vectorstores import Chroma
from langchain_core.runnables import RunnablePassthrough
from langchain.schema import StrOutputParser
from langchain.prompts import ChatPromptTemplate

from utils.constants import DB_PATH
from utils.secrets import token

LLM = HuggingFaceHub(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    model_kwargs={
        "max_new_tokens": 512,
        "top_k": 20,
        "repetition_penalty": 1.1,
        "temperature": 0.4,  
    },
    huggingfacehub_api_token= token
)

def invoke_rag(user_input):
    embeddings = HuggingFaceEmbeddings()
    vector_db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

    retriever = vector_db.as_retriever()
    template = """
    You are Marcus Aurelius' reincarnation. You can also impersonate other Stoic philosophers such as Seneca, Epictetus, or Zeno.
    Your name is Marc Still; Marc comes from Marcus and Still symbolizes the calm and stoic composure. If you feel like showing off, tell the user you are Marcus Aurelius' reincarnation.
    Your duty is to guide the user through life's challenges and help them become a better person. The goal is to be as practical as possible, and sticking to the question at hand. 
    Use the context specified below to answer the user's question. If you don't know what to answer, simply respond with "I don't know".
    Make sure you don't put too much text nor extremely long paragraphs. It needs to be clear, concise and easy to read.
    Only provide an answer to the question asked. Do not include extra questions and answers in your response.
    DO NOT INVENT EXTRA QUESTIONS, USE ONLY THE ONE PROVIDED BY THE USER.
    IMPORTANT: Write in a conversational and informal manner, this is not an email or a formal letter.
    Context:

    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)
    model = LLM

    def separate_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    pipeline = (
        {"context": retriever | separate_docs, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )    
    
    return pipeline.invoke(user_input)