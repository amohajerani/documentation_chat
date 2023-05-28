from langchain.document_loaders import BSHTMLLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
import pdb
from dotenv import find_dotenv, load_dotenv
import os

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_KEY")
persist_directory = 'synapse_db'

embeddings = OpenAIEmbeddings()
def store_to_vector_db(html_link):
    ##### Step 1 ######
    # Load your document
    loader = BSHTMLLoader(html_link)
    data = loader.load()

    ##### Step 2 ######
    # chunk the doc
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 1000,
        chunk_overlap  = 100,
        length_function = len,
    )
    docs = text_splitter.split_documents(data)

    ##### Step 3 ######
    # vectorize the chunks
    

    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    vectordb.persist()

    return None

file_directory = './downloaded_website'
file_list = os.listdir(file_directory)
file_list.sort()
# store the vector for each url
for file_name in ['page_10.html','page_11.html']:
    store_to_vector_db(os.path.join(file_directory, file_name))

# Now we can load the persisted database from disk, and use it as normal. 
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
query = "What is ACH?"
results = vectordb.similarity_search(query)
print(results)


##### Step 4 ######
# Convert the search results to answers
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
chain = load_qa_chain(llm, chain_type="stuff")
answer = chain.run(input_documents=results, question=query)
print(answer)