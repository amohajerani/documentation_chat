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
def create_docs(html_link):
    loader = BSHTMLLoader(html_link)
    data = loader.load()
    print('html_link: ',html_link)

    ##### Step 2 ######
    # chunk the doc
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size = 800,
        chunk_overlap  = 80,
        length_function = len,
    )
    splitted_docs =  text_splitter.split_documents(data)
    return splitted_docs

    ##### Step 3 ######
    # vectorize the chunks
    
    
    

file_directory = './downloaded_website'
file_list = os.listdir(file_directory)
docs = []
def embed_corpus(file_list):
    for file_name in file_list:
        file_docs = create_docs(os.path.join(file_directory, file_name))
        docs.extend(file_docs)
        print('len(docs): ', len(docs))
    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=persist_directory)
    vectordb.persist()
    vectordb = None

# Uncomment the line below to re-generate the vector db.
# embed_corpus(file_list)
# Now we can load the persisted database from disk, and use it as normal. 
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

import csv
def find_url_by_file(csv_file, file_name):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['File'] == file_name:
                return row['URL']
##### Step 4 ######
# Convert the search results to answers
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
llm = OpenAI(temperature=0, openai_api_key=os.environ["OPENAI_API_KEY"])
chain = load_qa_chain(llm, chain_type="stuff")
while True:
    print('----------------------------------')
    query = input('your question please: ')
    results = vectordb.similarity_search(query)
    answer = chain.run(input_documents=results[:3], question=query)
    # find the links for each result
    print('answer:')
    print(answer)
    print('\nReferences')
    urls = []
    for result in results:
        file_name=result.metadata['source'].replace('./downloaded_website/','')
        url = find_url_by_file('./map.csv', file_name+'.html')
        if url not in urls and url:
            urls.append(url)
    [print(url) for url in urls]