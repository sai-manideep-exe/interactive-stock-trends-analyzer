import os
import streamlit as st
import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_classic.chains import RetrievalQAWithSourcesChain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import google.generativeai as genai

# --- CONFIGURATION ---
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
FAISS_INDEX_PATH = "faiss_index"

if api_key:
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ GOOGLE_API_KEY not found. Please check your .env file.")
    st.stop()

st.set_page_config(page_title="SourcedAI", page_icon="📈", layout="wide")
st.title("🔍SourcedAI")

# --- SIDEBAR ---
st.sidebar.header("News Article URLs")

urls = []
for i in range(3):
    url = st.sidebar.text_input(f"URL {i+1}", placeholder="https://example.com/article")
    if url:
        urls.append(url)

process_url_clicked = st.sidebar.button("Process URLs", type="primary")

# --- CACHED RESOURCES ---
@st.cache_resource
def get_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

embeddings = get_embeddings()

# --- PROCESSING PIPELINE ---
if process_url_clicked:
    if not urls:
        st.sidebar.error("Please enter at least one URL.")
    else:
        with st.status("Processing URLs...", expanded=True) as status:
            try:
                status.write("📥 Loading data from URLs...")
                loader = UnstructuredURLLoader(urls=urls)
                data = loader.load()
                
                status.write("✂️ Splitting text into chunks...")
                # OPTIMIZATION: Increased chunk size for better context as suggested
                text_splitter = RecursiveCharacterTextSplitter(
                    separators=['\n\n', '\n', '.', ','],
                    chunk_size=1000, 
                    chunk_overlap=150
                )
                docs = text_splitter.split_documents(data)
                
                status.write("🧠 Building vector index...")
                vectorstore = FAISS.from_documents(docs, embeddings)
                vectorstore.save_local(FAISS_INDEX_PATH)
                
                status.update(label="✅ Processing Complete!", state="complete", expanded=False)
                st.success("Ready to answer questions from articles!")
                
            except Exception as e:
                status.update(label="❌ Error occurred", state="error")
                st.error(f"An error occurred: {e}")

# --- QUERY HANDLING ---
st.divider()
query = st.text_input("Ask a question:")

if query:
    with st.spinner("Analyzing..."):
        try:
            # --- RAG MODE ---
            if os.path.exists(FAISS_INDEX_PATH):
                vectorstore = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
                llm_rag = ChatGoogleGenerativeAI(
                    model="models/gemini-2.5-flash",
                    google_api_key=api_key,
                    temperature=0.3
                )
                chain = RetrievalQAWithSourcesChain.from_llm(llm=llm_rag, retriever=vectorstore.as_retriever())
                result = chain({"question": query}, return_only_outputs=True)

                st.subheader("Answer")
                st.markdown(result["answer"])

                if result.get("sources"):
                        st.subheader("Sources")
                        for source in result["sources"].split("\n"):
                            if source.strip():
                                st.caption(source)
            else:
                st.info("👆 Please process some URLs first.")

        except Exception as e:
            st.error(f"An error occurred. \n\n**Error details:** {e}")
