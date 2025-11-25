import os
import streamlit as st
import pickle
import time
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import UnstructuredURLLoader
from langchain.vectorstores import FAISS
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Check if the API key is being read properly
openai_api_key = st.secrets["OPENAI_API_KEY"]
if not openai_api_key:
    st.error("Error: API key not found. Please check your .env file or environment variables.")
    raise ValueError("API key not found. Please check your .env file or environment variables.")

# Initialize the OpenAI LLM with the API key
llm = OpenAI(temperature=0.9, max_tokens=500, openai_api_key=openai_api_key)

# Streamlit app setup
st.title("News Research Tool 📈")
st.sidebar.title("News Article URLs")

# Get URLs from the sidebar
urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}")
    urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs")  # Button to initiate processing of entered URLs
file_path = "faiss_store_openai.pkl"  # File path for storing serialized FAISS index

main_placeholder = st.empty()  # Placeholder for main content area

if process_url_clicked:
    loader = UnstructuredURLLoader(urls=urls)
    main_placeholder.text("Data Loading...Started...✅✅✅")  # Display loading message
    data = loader.load()

    # Split data into smaller documents
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    main_placeholder.text("Text Splitter...Started...✅✅✅")  # Display text splitting message
    docs = text_splitter.split_documents(data)

    # Create embeddings from documents and build FAISS index
    embeddings = OpenAIEmbeddings()
    vectorstore_openai = FAISS.from_documents(docs, embeddings)
    pkl = vectorstore_openai.serialize_to_bytes()
    main_placeholder.text("Embedding Vector Started Building...✅✅✅")  # Display embedding vector building message
    time.sleep(2)  # Simulate processing time

    # Save the FAISS index to a pickle file
    with open(file_path, "wb") as f:
        pickle.dump(pkl, f)

# Input field for user query
query = main_placeholder.text_input("Question: ")

if query:
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            pkl = pickle.load(f)
            # Deserialize the FAISS index and create a retrieval question-answering chain
            vectorstore = FAISS.deserialize_from_bytes(embeddings=OpenAIEmbeddings(), serialized=pkl, allow_dangerous_deserialization=True)
            chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorstore.as_retriever())
            result = chain({"question": query}, return_only_outputs=True)
            # result will be a dictionary of this format --> {"answer": "", "sources": [] }
            st.header("Answer")  # Display header for answer
            st.write(result["answer"])  # Display the answer

            # Display sources, if available
            sources = result.get("sources", "")
            if sources:
                st.subheader("Sources:")  # Display subheader for sources
                sources_list = sources.split("\n")  # Split sources by newline
                for source in sources_list:
                    st.write(source)  # Display each source
