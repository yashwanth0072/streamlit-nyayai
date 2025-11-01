# ⚖️ NyayAI - AI-Powered Legal Assistant

**Justice Made Simple** - Your intelligent companion for understanding Indian law and legal matters.

![Python](https://img.shields.io/badge/python-3.13+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.50.0-FF4B4B.svg)

---

## 🌟 Overview

NyayAI is an AI-powered legal assistant designed specifically for Indian users. It simplifies complex legal concepts, provides guidance on IPC (Indian Penal Code) sections, analyzes legal documents, and offers preliminary legal information in an easy-to-understand format.

### ✨ Key Features

- **💬 Legal Q&A Chat** - Ask legal questions and get AI-powered answers with relevant IPC sections
- **📄 Document Analysis** - Upload and analyze PDF documents with AI-powered summarization
- **🃏 Interactive IPC Flashcards** - Learn IPC sections with 3D flip animations
- **📚 IPC Sections Database** - Browse and search through Indian Penal Code sections
- **📋 Legal Templates** - Ready-to-use legal document templates
- **🤖 Multi-Provider AI Support** - Gemini, OpenAI, DeepSeek, and Nemotron via OpenRouter

---

## 🚀 Quick Start

### Prerequisites

- Python 3.13+ (or Python 3.10+)
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yashwanth0072/streamlit-nyayai.git
   cd streamlit-nyayai
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install streamlit>=1.28.0 requests>=2.31.0 PyMuPDF>=1.23.0
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Access the app**
   - Open your browser and go to: http://localhost:8501

---

## 🔑 API Configuration

NyayAI uses [OpenRouter](https://openrouter.ai/) for all AI providers. You only need **ONE** API key!

1. Get your free API key from: https://openrouter.ai/keys
2. In the app sidebar, select your preferred AI provider (Gemini, OpenAI, DeepSeek, or Nemotron)
3. Enter your OpenRouter API key
4. Click "Configure API Key"

That's it! The app will work with any AI provider you choose.

---

## 📖 Features Guide

### 1. Legal Q&A Chat
- Ask any legal question in plain language
- Get AI-powered responses with 5 structured sections:
  - Quick Answer
  - Legal Consequences
  - Applicable Laws
  - What You Should Do
  - Legal Advice & Contacts
- View relevant IPC sections automatically
- Chat history saved for the session

### 2. Document Analysis
- Upload PDF documents (max 10MB)
- Quick preview of first 2 pages
- Full document analysis and summarization
- Extract text for download
- Supports legal contracts, agreements, and case files

### 3. IPC Flashcards
- Interactive learning with 3D flip animations
- Front: Section number, title, description, context
- Back: Detailed punishment and sentencing guidelines
- Grid or list view options
- Search functionality

### 4. IPC Sections Database
- Browse all IPC sections
- Search by section number, keywords, or legal terms
- AI explanations on demand
- Copy section text for reference
- Detailed punishment information

### 5. Legal Templates
- Ready-to-use legal document templates
- Categories: Contracts, Notices, Complaints
- Editable and downloadable
- Professional formatting

---

## 🛠️ Technical Stack

### Core Technologies
- **Frontend:** Streamlit 1.50.0
- **Backend:** Python 3.13
- **Database:** SQLite3 (built-in)
- **PDF Processing:** PyMuPDF (fitz)
- **AI Integration:** OpenRouter API

### Architecture
```
streamlit-nyayai/
├── app.py              # Main application & routing
├── ai_handler.py       # AI orchestration logic
├── ai_providers.py     # AI provider implementations
├── database.py         # SQLite database operations
├── pdf_processor.py    # PDF text extraction
├── ui_components.py    # UI rendering components
├── config.py           # Configuration & constants
├── .streamlit/
│   └── config.toml     # Streamlit server config
└── README.md           # This file
```

### Design Patterns
- **Abstract Factory** - AI provider creation
- **Singleton** - Database initialization
- **Separation of Concerns** - Clean layered architecture

---

## ⚙️ Configuration

### File Upload Limits
Maximum file size: **10MB**

Configure in `.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 10
```

### AI Model Settings
Temperature: 0.3  
Max Tokens: 300  
Top P: 0.8

Adjust in `config.py` if needed.

---

## 🎨 Features Highlights

### Same-Tab Navigation
- Click any feature card to navigate in the same tab
- Clean URL-based routing with query parameters
- Sidebar navigation stays in sync

### Responsive UI
- Custom CSS with gradient backgrounds
- Dark theme optimized
- Mobile-friendly design
- Smooth animations and transitions

### Offline Mode
- Works without AI API key (limited features)
- Fallback responses for common queries
- All database features available offline

---

## 🔒 Security

- ✅ No hardcoded API keys
- ✅ Environment variable based configuration
- ✅ Parameterized SQL queries (no injection risk)
- ✅ File upload size validation
- ✅ Input sanitization throughout
- ✅ Secure session state management

---

## 📊 Performance

- Session state caching for AI handler
- PDF preview mode (limits processing to 2 pages)
- Text truncation for API efficiency
- Connection pooling (requests.Session)
- Optimized database queries

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is currently unlicensed. All rights reserved by the author.

---

## ⚠️ Disclaimer

**Important:** NyayAI is an AI-powered legal information tool and **NOT a substitute for professional legal advice**. 

- The information provided is for educational and informational purposes only
- Always consult with a qualified lawyer for specific legal matters
- Legal consequences depend on specific circumstances and jurisdiction
- Keep all relevant documents and evidence for legal proceedings

---

## 🙏 Acknowledgments

- **Streamlit** - For the amazing web framework
- **OpenRouter** - For unified AI provider access
- **PyMuPDF** - For PDF processing capabilities
- **Indian Legal System** - For IPC section data

---

## 📧 Contact

**Developer:** Yashwanth  
**GitHub:** [@yashwanth0072](https://github.com/yashwanth0072)  
**Email:** balajivvsy@gmail.com

---

## 🚀 Deployment

### Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set your OpenRouter API key in Secrets:
   ```toml
   OPENROUTER_API_KEY = "your-api-key-here"
   ```
5. Deploy!

### Local Production

```bash
# Install dependencies
pip install -r requirements.txt

# Run with production settings
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## 📚 Documentation

For detailed documentation, see:
- [Code Audit Report](./miscellenious/CODE_AUDIT_REPORT.md) - Comprehensive code review
- [Tech Stack](./miscellenious/TECH_STACK.md) - Technical details
- [API Documentation](./miscellenious/API_DOCS.md) - API reference

---

## 🎯 Roadmap

- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] Voice input for queries
- [ ] Case law database integration
- [ ] Lawyer directory
- [ ] Mobile app version
- [ ] Advanced document comparison
- [ ] Legal case tracking

---

<div align="center">

**Made with ❤️ for the Indian Legal System**

⚖️ **NyayAI - Justice Made Simple** ⚖️

[Report Bug](https://github.com/yashwanth0072/streamlit-nyayai/issues) · [Request Feature](https://github.com/yashwanth0072/streamlit-nyayai/issues)

</div>
