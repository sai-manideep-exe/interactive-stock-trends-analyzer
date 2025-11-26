import os
import streamlit as st
import pickle
import time
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("Error: API key not found. Please check your .env file or environment variables.")
    raise ValueError("API key not found. Please check your .env file or environment variables.")

# Initialize the OpenAI LLM with the API key (using ChatOpenAI for v1.x compatibility)
llm = ChatOpenAI(temperature=0.9, max_tokens=500, openai_api_key=openai_api_key)

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
    # Validate URLs
    valid_urls = [url for url in urls if url.strip()]
    if not valid_urls:
        st.error("❌ Please enter at least one valid URL.")
        st.stop()
    
    try:
        # Add headers to bypass 403 Forbidden blocks (simulate browser request)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        loader = UnstructuredURLLoader(urls=valid_urls, headers=headers)
        main_placeholder.text("Data Loading...Started...✅✅✅")  # Display loading message
        data = loader.load()
        
        if not data:
            st.error("❌ No content could be loaded from the URLs. Please check the URLs and ensure they contain readable content.")
            st.stop()

        # Split data into smaller documents
        text_splitter = RecursiveCharacterTextSplitter(
            separators=['\n\n', '\n', '.', ','],
            chunk_size=1000
        )
        main_placeholder.text("Text Splitter...Started...✅✅✅")  # Display text splitting message
        docs = text_splitter.split_documents(data)
        
        if not docs:
            st.error("❌ No documents were created after text splitting. The content may be too short or invalid.")
            st.stop()

        # Create embeddings from documents and build FAISS index
        main_placeholder.text("Embedding Vector Started Building (this may take a minute)...⏳")
        embeddings = OpenAIEmbeddings()
        
        try:
            vectorstore_openai = FAISS.from_documents(docs, embeddings)
        except IndexError as ie:
            st.error(f"❌ Failed to create embeddings. This may indicate an OpenAI API issue. Details: {str(ie)}")
            st.stop()
        except Exception as ve:
            st.error(f"❌ Error creating vector store: {str(ve)}")
            st.stop()
        
        pkl = vectorstore_openai.serialize_to_bytes()
        main_placeholder.text("Embedding Vector Started Building...✅✅✅")  # Display embedding vector building message
        time.sleep(2)  # Simulate processing time

        # Save the FAISS index to a pickle file
        with open(file_path, "wb") as f:
            pickle.dump(pkl, f)
            
        st.success("✅ URLs processed and vector store created successfully!")
        
    except Exception as e:
        st.error(f"❌ An unexpected error occurred: {str(e)}")
        import traceback
        st.error(traceback.format_exc())

# Input field for user query
query = main_placeholder.text_input("Question: ")

if query:
    if os.path.exists(file_path):
        try:
            with open(file_path, "rb") as f:
                pkl = pickle.load(f)
                # Deserialize the FAISS index
                vectorstore = FAISS.deserialize_from_bytes(embeddings=OpenAIEmbeddings(), serialized=pkl, allow_dangerous_deserialization=True)
                
                # Use modern retrieval: get relevant documents and let the LLM answer
                with st.spinner("🔍 Searching and generating answer..."):
                    # Retrieve relevant documents using modern invoke() method
                    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
                    relevant_docs = retriever.invoke(query)
                    
                    if not relevant_docs:
                        st.warning("⚠️ No relevant documents found for your query.")
                    else:
                        # Build context from retrieved docs
                        context = "\n\n".join([f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}" for doc in relevant_docs])
                        
                        # Create a prompt for the LLM
                        qa_prompt = PromptTemplate(
                            template="Based on the following context, answer the question. If you can't find the answer in the context, say so.\n\nContext:\n{context}\n\nQuestion: {question}\n\nAnswer:",
                            input_variables=["context", "question"]
                        )
                        
                        # Generate answer using the LLM with invoke()
                        formatted_prompt = qa_prompt.format(context=context, question=query)
                        answer_obj = llm.invoke(formatted_prompt)
                        answer = answer_obj.content if hasattr(answer_obj, 'content') else str(answer_obj)
                        
                        # Display results
                        st.header("Answer")
                        st.write(answer)
                        
                        # Display sources
                        st.subheader("Sources:")
                        for doc in relevant_docs:
                            source_text = doc.metadata.get('source', 'Unknown')
                            st.markdown(f"- **Source:** `{source_text}`")
        except Exception as e:
            st.error(f"❌ Error processing query: {str(e)}")
    else:
        st.warning("⚠️ Please process the URLs first by clicking the 'Process URLs' button.")
