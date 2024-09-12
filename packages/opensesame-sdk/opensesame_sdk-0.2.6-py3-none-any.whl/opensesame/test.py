from opensesame import OpenSesame_openai
from opensesame import OpenSesame_gemini
from opensesame import OpenSesame_anthropic 
from opensesame import OpenSesame_groq
from opensesame import OpenSesame_huggingface
from opensesame import OpenSesame_cohere 
from opensesame import OpenSesame_azure_openai
from opensesame import OpenSesame_langchain
from langchain.chains import LLMChain, RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain, RetrievalQA, ConversationalRetrievalChain
from langchain.chains import RetrievalQA
from langchain_pinecone import PineconeVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
import os


load_dotenv(override=True, dotenv_path=".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_INDEX = os.getenv("PINECONE_INDEX")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
AZURE_API_KEY = os.getenv("AZURE_API_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AZURE_DEPLOYMENT = os.getenv("AZURE_DEPLOYMENT")
OPEN_SESAME_KEY = os.getenv("OPEN_SESAME_KEY")

# openai test
def test_openai() :
    client = OpenSesame_openai({
        'api_key': OPENAI_API_KEY,
        'open_sesame_key': OPEN_SESAME_KEY,
        'project_name': 'proj1',  # Make sure this is correct
    })

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role" : "system", "content" : "You are a scientist"},{"role": "user", "content": "Explain nuclear fission in simple steps"}]
        )
        print("*********")
        print(completion)
    except Exception as e:
        print(f"An error occurred: {e}")

# gemini test
def test_gemini() :
    client = OpenSesame_gemini({
        "api_key" : GEMINI_API_KEY,
        "open_sesame_key" : OPEN_SESAME_KEY,
        'project_name': 'proj1'
    })

    try :
        response = client.GenerativeModel(model_name="gemini-1.5-pro").generate_content(prompt="Who holds the record for the longest recorded swim")
        print(response)
    except Exception as e:
        print(f"An error occured {e}")

def test_anthropic() :
    client = OpenSesame_anthropic({
    'api_key': ANTHROPIC_API_KEY,
    'open_sesame_key': OPEN_SESAME_KEY,
    'project_name': 'proj1'
    })

    message = client.Messages(client).create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        system="You are an honest and helpful assistant",
        messages=[
            {"role": "user", "content": "How does a GPU work"}
        ]
    )
    print(message)

def test_groq() :
    client = OpenSesame_groq({
    'api_key': GROQ_API_KEY,
    'open_sesame_key': OPEN_SESAME_KEY,
    'project_name': 'proj1'
    })
    
    result = client.ChatCompletions(client).create(
        model="llama3-8b-8192",
        messages=[
            {"role" : "system", "content" : "You are an honest and helpful assistant"},
            {"role": "user", "content": "Who build the llama language models ?"}
        ]
    )

    print(result)

def test_hf() :
    client = OpenSesame_huggingface({
    "hf_api_token":HUGGINGFACE_API_TOKEN,
    "open_sesame_key":OPEN_SESAME_KEY,
    "project_name" : 'proj1'
    })   

    result = client.generate_text(
        model_name="gpt2",
        prompt="What is gpt2"
    )

    print(f"********** This is the result ***************** {result}")

def test_cohere() :
    co = OpenSesame_cohere({
        'api_key': COHERE_API_KEY,
        'open_sesame_key': OPEN_SESAME_KEY,
        'project_name': 'proj1'
    })

    result = co.chat(
        message = "Who invented chocolate ?",
        preamble = "You are an honest and helpful assistant"
    )

    print(result)

def test_os() :
    from opensesame import OpenSesame 

    os = OpenSesame(
        open_sesame_key = "6def3c47-847e-428d-a7bd-899da351a19c",
        project_name = "proj1"
    )

    response = os.evaluate(prompt="The user prompt", answer="The LLM response")

def test_azure() :
    endpoint=AZURE_ENDPOINT
    deployment=AZURE_DEPLOYMENT
    api_key=AZURE_API_KEY
    api_version="2024-06-01"
    config = {
    'api_key': api_key,
    'azure_endpoint': endpoint,
    'deployment': deployment,
    'api_version' : api_version,
    'open_sesame_key': OPEN_SESAME_KEY,
    'project_name': 'proj1'
    }   

    client = OpenSesame_azure_openai(config)
    response = client.call(
        prompt='What is japans population decline rate'
    )

    print(response)

def os_langchain() :
    # -------------------------------------
    os_langchain = OpenSesame_langchain({
        'open_sesame_key': OPEN_SESAME_KEY,
        'project_name': 'proj1'
    })
    callback_manager = os_langchain.rag_callback_manager()
    # -------------------------------------
   
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

    embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY, model="text-embedding-ada-002")
    vectorstore = PineconeVectorStore(index_name=PINECONE_INDEX, embedding=embeddings, text_key="text", pinecone_api_key=PINECONE_API_KEY)
    retriever = vectorstore.as_retriever()
    # Set up a "refine" QA chain
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="refine", retriever=retriever, callback_manager=callback_manager)
    response = chain.invoke({"query": "How has AI evolved in the last decade?"})
    print("*********RETRIEVALQA OVER***************")
    retriever = vectorstore.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=retriever, callback_manager=callback_manager)
    response = chain.invoke({"question": "What is the capital of India?", "chat_history":[]})
    print("*********CONVERSATIONALRETRIEVALCHAIN OVER***************")
    prompt = "Is dark chocolate healthier than milk chocolate ?"
    chain =  llm | StrOutputParser()
    #response = chain.invoke(prompt, config={"callbacks": [callback_manager.handlers[0]]})
    print(response)
    print("*********LLMCHAIN OVER***************")
    #chain1 = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["product"], template="What is a good name for a company that makes {product}?"))
    #chain2 = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["company_name", "product"], template="Write a catchphrase for {company_name} that sells {product}."))
    #chain = SequentialChain(chains=[chain1, chain2], input_variables=["product"], output_variables=["company_name", "text"])
    #response = chain.invoke({"product": "color TVs"})
    
test_os()










