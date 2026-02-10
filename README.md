# 🔍SourcedAI

A intelligent news research application that analyzes multiple news articles using AI-powered semantic search and retrieval. Built with **LangChain v1.x**, **Google Gemini**, **HuggingFace**, and **Streamlit**.

**Live Demo:** [https://interactive-stock-trends-analyzer-bs7m9vf7je9eabewh9lv2p.streamlit.app/](https://interactive-stock-trends-analyzer-bs7m9vf7je9eabewh9lv2p.streamlit.app/)
---

## Features

✨ **Multi-URL Content Loading** — Load and process content from multiple news sources simultaneously  
🧠 **AI-Powered Search** — Uses HuggingFace embeddings to understand semantic meaning locally
📚 **Vector Store with FAISS** — Fast similarity search across document chunks  
🔍 **Source Attribution** — Every answer includes clickable links to original sources  
⚡ **Real-time Processing** — Progressive status updates while loading and indexing  
🛡️ **Error Handling** — Graceful fallbacks for failed URLs or API issues  
🔐 **Secure API Keys** — Environment-based configuration for production  
🆓 **Free to Use** — Runs on Google Gemini (Free Tier) and Open Source Embeddings

---

## How It Works

1. **Load URLs** → Fetches and parses content from provided news article links
2. **Split & Embed** → Breaks content into chunks and creates semantic embeddings using HuggingFace
3. **Store** → Saves vector embeddings in a FAISS index (Text chunks → Numbers)
4. **Query** → User asks a question; app retrieves top 3 relevant document chunks
5. **Answer** → Google Gemini 2.5 Flash generates an answer based on retrieved context
6. **Source** → Displays source URLs for verification

---

## Installation

### Local Setup

#### Prerequisites
- Python 3.10+
- Google API Key ([get one here](https://aistudio.google.com/))

#### Steps

1. **Clone the repository:**
```bash
git clone https://github.com/sai-manideep-exe/interactive-stock-trends-analyzer.git
cd interactive-stock-trends-analyzer
```

2. **Create a virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file in the project root:
```env
GOOGLE_API_KEY=your_google_api_key_here
```

Or export it in your shell:
```bash
export GOOGLE_API_KEY="your_google_api_key_here"
```

5. **Run the app:**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## Usage

### Local Testing

1. **Enter News URLs**
   - Paste 1-3 news article URLs in the sidebar
   - Supported sources: MoneyControl, CNBC, Bloomberg, etc.
   - Any website with readable text content works

2. **Process URLs**
   - Click "Process URLs" button
   - Wait for:
     - ✅ Data Loading (fetches content)
     - ✅ Text Splitter (chunks into ~1000 char pieces)
     - ✅ Embedding Vector Building (Local HuggingFace model)

3. **Ask Questions**
   - Type any question about the loaded content
   - The app searches for relevant sections and generates an answer
   - Sources are displayed below with direct links

### Example Queries
- "What was the target price mentioned?"
- "Why did the stock jump today?"
- "What are the key risks for this company?"
- "Summarize the financial results."

---

## Deployment to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git add gem.py requirements.txt
git commit -m "Migrated to Gemini 2.5 and HuggingFace Embeddings"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository
4. Set main file: `gem.py`
5. Set branch: `main`
6. Click **"Deploy"**

### Step 3: Add Secrets

In the Streamlit Cloud app settings, add under **"Secrets"**:

```toml
GOOGLE_API_KEY = "AIzaSy..."
```

The app will automatically restart and use the secret.

---

## Architecture

```
┌─────────────────────┐
│   User Interface    │  (Streamlit)
│  (URLs + Question)  │
└──────────┬──────────┘
           │
┌──────────▼─────────────────┐
│  UnstructuredURLLoader     │  Fetches & parses web content
└──────────┬─────────────────┘
           │
┌──────────▼──────────────────────────┐
│  RecursiveCharacterTextSplitter    │  Chunks into 1000-char pieces
└──────────┬──────────────────────────┘
           │
┌──────────▼─────────────────┐
│  HuggingFace Embeddings    │  Creates semantic vectors locally
│  (all-MiniLM-L6-v2)        │
└──────────┬─────────────────┘
           │
┌──────────▼─────────────────┐
│  FAISS Vector Store        │  Fast similarity search
└──────────┬─────────────────┘
           │
┌──────────▼──────────────┐
│  Retriever (Top-3)      │  Fetches relevant chunks
└──────────┬──────────────┘
           │
┌──────────▼──────────────────┐
│  Google Gemini 2.5 Flash     │  Generates answer from context
└──────────┬──────────────────┘
           │
┌──────────▼──────────────┐
│  Display Answer + Sources │  (Streamlit UI)
└─────────────────────────┘
```

---

## Configuration

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | — | Your Google Gemini API Key |

### Streamlit Config

To customize the app behavior, create `.streamlit/config.toml`:

```toml
[client]
showErrorDetails = true

[theme]
primaryColor = "#0084D9"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

---

## Dependencies

Core packages (see `requirements.txt` for exact versions):
- **streamlit** — Web UI framework
- **langchain** — LLM orchestration
- **langchain-google-genai** — Google Gemini integration
- **sentence-transformers** — Open source embeddings
- **faiss-cpu** — Vector similarity search
- **python-dotenv** — Environment management

---

## Performance Tips

### For Production Deployment

1. **Cache Models**
   The app uses `@st.cache_resource` for the embedding model to prevent reloading the 80MB model on every interaction.

2. **Rate Limiting**
   - Google Gemini 2.5 Flash (Free Tier) has rate limits (approx 15 RPM).
   - If you hit `429 Resource Exhausted`, wait 60 seconds.

3. **Memory Usage**
   - Streamlit Cloud has a ~1GB-3GB RAM limit.
   - The HuggingFace model (`all-MiniLM-L6-v2`) is optimized for low memory (~200MB), making it perfect for free cloud deployment.

---

## Future Enhancements

- [ ] **Multi-language support** (Gemini translation)
- [ ] **PDF/document upload** (not just URLs)
- [ ] **Conversation history** (session state)
- [ ] **Stock Charts** (integration with YFinance)

---

## Costs

**Approximate costs per query:**

| Component | Cost |
|-----------|------|
| Embeddings (HuggingFace) | **$0.00** (Runs locally) |
| LLM (Gemini 2.5 Flash) | **$0.00** (Free Tier) |
| **Total per use** | **$0.00** |

*Note: Free tier data may be used for improvement by Google. Use paid enterprise tier for strict privacy.*

---

## Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source and available under the MIT License.

---

**Built with ❤️ using LangChain, Google Gemini, and Streamlit**
