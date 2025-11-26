# Interactive Stock Trends Analyzer 📈

A intelligent news research application that analyzes multiple news articles using AI-powered semantic search and retrieval. Built with **LangChain v1.x**, **OpenAI**, and **Streamlit**.

**Live Demo:** [https://interactive-stock-trends-analyzer-bs7m9vf7je9eabewh9lv2p.streamlit.app/](https://interactive-stock-trends-analyzer-bs7m9vf7je9eabewh9lv2p.streamlit.app/)

---

## Features

✨ **Multi-URL Content Loading** — Load and process content from multiple news sources simultaneously  
🧠 **AI-Powered Search** — Uses OpenAI embeddings to understand semantic meaning, not just keywords  
📚 **Vector Store with FAISS** — Fast similarity search across document chunks  
🔍 **Source Attribution** — Every answer includes clickable links to original sources  
⚡ **Real-time Processing** — Progressive status updates while loading and indexing  
🛡️ **Error Handling** — Graceful fallbacks for failed URLs or API issues  
🔐 **Secure API Keys** — Environment-based configuration for production

---

## How It Works

1. **Load URLs** → Fetches and parses content from provided news article links
2. **Split & Embed** → Breaks content into chunks and creates semantic embeddings
3. **Store** → Saves vector embeddings in a FAISS index for fast retrieval
4. **Query** → User asks a question; app retrieves top 3 relevant document chunks
5. **Answer** → ChatOpenAI generates an answer based on retrieved context
6. **Source** → Displays source URLs for verification

---

## Installation

### Local Setup

#### Prerequisites
- Python 3.10+
- OpenAI API key ([get one here](https://platform.openai.com/api-keys))

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
OPENAI_API_KEY=your_openai_api_key_here
```

Or export it in your shell:
```bash
export OPENAI_API_KEY="your_openai_api_key_here"
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
   - Supported sources: Reuters, BBC, MoneyControl, etc.
   - Any website with readable text content works

2. **Process URLs**
   - Click "Process URLs" button
   - Wait for:
     - ✅ Data Loading (fetches content)
     - ✅ Text Splitter (chunks into ~1000 char pieces)
     - ✅ Embedding Vector Building (5-30 seconds depending on content size)

3. **Ask Questions**
   - Type any question about the loaded content
   - The app searches for relevant sections and generates an answer
   - Sources are displayed below with direct links

### Example Queries
- "What was the stock price change?"
- "Who are the key people mentioned?"
- "What are the main points in this article?"
- "How did the company perform?"

---

## Deployment to Streamlit Cloud

### Step 1: Push to GitHub

```bash
git add app.py requirements.txt
git commit -m "News Research Tool - LangChain v1.x with OpenAI integration"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository: `interactive-stock-trends-analyzer`
4. Set main file: `app.py`
5. Set branch: `main`
6. Click **"Deploy"**

### Step 3: Add Secrets

In the Streamlit Cloud app settings, add under **"Secrets"**:

```toml
OPENAI_API_KEY = "sk-..."
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
│  OpenAI Embeddings         │  Creates semantic vectors
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
│  ChatOpenAI                  │  Generates answer from context
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
| `OPENAI_API_KEY` | ✅ Yes | — | Your OpenAI API key |

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

## Troubleshooting

### "Error: API key not found"
- **Local:** Make sure `.env` file exists with `OPENAI_API_KEY=...`
- **Streamlit Cloud:** Add secret via app settings (Settings → Secrets)

### "HTTP Error 403: Forbidden"
- Some websites block automated scraping
- **Solution:** Try different URLs from Reuters, BBC, or other sources
- The app includes a User-Agent header to bypass basic bot detection

### "No content could be loaded"
- URL might be behind a paywall or require authentication
- Try a publicly accessible news article
- Check if the website allows scraping in its `robots.txt`

### Slow response times
- **First load:** Embeddings take 10-30 seconds (depends on content size)
- **Query time:** OpenAI API calls typically take 5-10 seconds
- This is normal; consider caching for production use

### Out of memory error
- Large articles create many chunks
- Reduce chunk size in code (line 57: `chunk_size=1000`)
- Or process fewer/shorter articles

---

## Dependencies

Core packages (see `requirements.txt` for exact versions):
- **streamlit** — Web UI framework
- **langchain** — LLM orchestration (v1.x)
- **langchain-openai** — OpenAI integration
- **langchain-community** — Document loaders & vector stores
- **faiss-cpu** — Vector similarity search
- **openai** — API client
- **python-dotenv** — Environment management

---

## Performance Tips

### For Production Deployment

1. **Cache Vector Stores**
   ```python
   @st.cache_resource
   def load_vectorstore(filepath):
       # Load FAISS index
   ```

2. **Add Request Timeout**
   ```python
   requests_timeout = 30  # seconds
   ```

3. **Rate Limiting**
   - OpenAI has usage limits
   - Streamlit Cloud has memory limits (2GB)
   - Monitor costs at https://platform.openai.com/account/billing/overview

4. **Optimize Chunk Size**
   - Larger chunks = fewer embeddings = faster & cheaper
   - Smaller chunks = better precision
   - Sweet spot: 500-1500 characters

---

## Future Enhancements

- [ ] **Multi-language support** (GPT-4 translation)
- [ ] **PDF/document upload** (not just URLs)
- [ ] **Vector store persistence** (S3/GitHub LFS)
- [ ] **Conversation history** (session state)
- [ ] **Advanced filtering** (date range, source domain)
- [ ] **Cost tracking** (per-query OpenAI spend)
- [ ] **Batch processing** (API for programmatic access)
- [ ] **Different LLMs** (support Claude, Llama, etc.)

---

## Costs

**Approximate costs per query (based on OpenAI pricing as of Nov 2025):**

| Component | Cost |
|-----------|------|
| Embedding 10KB content | ~$0.002 |
| LLM answer generation | ~$0.01 |
| **Total per use** | ~$0.012 |

**Monthly estimate:** Processing 100 articles = ~$1.20

See [OpenAI pricing](https://openai.com/pricing) for current rates.

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

## Support & Contact

- **Report Issues:** [GitHub Issues](https://github.com/sai-manideep-exe/interactive-stock-trends-analyzer/issues)
- **Questions?** Open a discussion or reach out!

---

## Changelog

### v1.0.0 (Nov 26, 2025)
- ✅ Migrated from LangChain v0.x to v1.x
- ✅ Replaced deprecated `RetrievalQAWithSourcesChain` with modern retrieval pattern
- ✅ Added User-Agent headers for bot detection bypass
- ✅ Comprehensive error handling and user feedback
- ✅ Production-ready Streamlit Cloud deployment

---

**Built with ❤️ using LangChain, OpenAI, and Streamlit**
