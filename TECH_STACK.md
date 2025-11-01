# NyayAI - Tech Stack Documentation

## 🏗️ Complete Technology Stack

### **Frontend Framework**
- **Streamlit** (>=1.28.0)
  - Web application framework for Python
  - Provides interactive UI components (file uploaders, text inputs, buttons, expanders)
  - Session state management
  - Custom CSS/JavaScript injection for advanced styling
  - Query parameter handling for navigation

### **Backend & Core Technologies**

#### **Database**
- **SQLite3** (Python standard library)
  - Embedded relational database
  - Tables: `ipc_sections`, `legal_templates`, `query_history`
  - No separate server required
  - File-based storage: `nyayai.db`

#### **AI & Machine Learning**
- **Google Generative AI SDK** (google-generativeai >=0.3.0)
  - Gemini Pro model integration
  - Natural language processing for legal Q&A
  - Document summarization
  - IPC section explanations

- **OpenAI SDK** (openai >=1.0.0)
  - GPT-3.5-turbo model support
  - Alternative AI provider option
  - Chat completion API

- **OpenRouter API Integration** (via requests library)
  - DeepSeek Chat v3.1 model
  - Nvidia Nemotron Nano 12B v2 VL (free tier)
  - REST API communication

#### **Document Processing**
- **PyMuPDF (fitz)** (>=1.23.0)
  - PDF text extraction
  - PDF metadata reading
  - Multi-page document processing
  - Supports streaming PDF processing

#### **HTTP & API Communication**
- **Requests** (>=2.31.0)
  - HTTP client for OpenRouter API
  - Session management for API calls
  - Error handling and retries

### **Python Standard Library Modules Used**
- **sqlite3** - Database operations
- **json** - Data serialization/deserialization
- **os** - Environment variable management, file system operations
- **io** - In-memory file operations (BytesIO for PDF processing)
- **typing** - Type hints (Optional, Dict, List, Tuple, Any)
- **abc** - Abstract base classes for AI provider interface
- **urllib.parse** - URL encoding for navigation parameters

### **Frontend Technologies (Embedded)**
- **HTML5** - Custom UI components (flashcards, feature cards, chat messages)
- **CSS3** - Responsive styling, animations, gradients
  - CSS Grid & Flexbox layouts
  - 3D transforms for flashcard flip animations
  - Custom color theming
  - Dark mode UI
- **JavaScript (ES6)** - Client-side interactions
  - Sidebar toggle functionality
  - Click-outside event handling
  - Keyboard support for flashcards

### **Web Fonts**
- **Google Fonts** - Inter font family (300, 400, 500, 600, 700 weights)

---

## 📦 Project Architecture

### **Modular Design**
```
streamlit-nyayai/
├── app.py                 # Main Streamlit application & routing
├── config.py              # Configuration constants & settings
├── database.py            # SQLite database management
├── ai_handler.py          # AI provider orchestration
├── ai_providers.py        # AI provider implementations (Gemini, OpenAI, DeepSeek, Nemotron)
├── pdf_processor.py       # PDF text extraction & analysis
├── ui_components.py       # Reusable UI components & styling
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Streamlit server configuration
└── nyayai.db             # SQLite database file
```

### **Design Patterns Used**
- **Abstract Factory Pattern** - AI provider creation (`create_ai_provider()`)
- **Strategy Pattern** - Pluggable AI providers (GeminiProvider, OpenAIProvider, etc.)
- **Singleton Pattern** - Database connection management
- **MVC-like Separation** - UI components, business logic, data access layers

---

## 🎨 Key Features & Technologies

### **1. Multi-Provider AI System**
- Provider-agnostic architecture
- Automatic fallback to offline mode
- Model configuration optimization (temperature, max_tokens, top_p)

### **2. Interactive UI Components**
- **Flashcards** - 3D CSS transforms, flip animations
- **Feature Cards** - Hover effects, gradient backgrounds
- **Chat Interface** - User/AI message differentiation with custom styling
- **Document Uploader** - Size validation, preview mode

### **3. Legal Database**
- Indian Penal Code sections with:
  - Section numbers, titles, descriptions
  - Applicable contexts
  - Punishment details
  - Category classification
  - Keyword indexing for search

### **4. Document Analysis Pipeline**
- PDF upload & validation (10 MB limit)
- Text extraction with PyMuPDF
- Preview mode (first 2 pages)
- Full document analysis
- AI-powered summarization

### **5. Configuration Management**
- Environment variables for API keys
- Centralized color theming
- Model parameters tuning
- File upload limits

---

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### **Installation Steps**
```bash
# Clone the repository
git clone <repository-url>
cd streamlit-nyayai

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```

### **API Key Configuration**
Configure AI providers through the sidebar in the application:
- **Gemini**: Get API key from Google AI Studio
- **OpenAI**: Get API key from OpenAI Platform
- **DeepSeek/Nemotron**: Get OpenRouter API key from OpenRouter.ai

---

## 🔧 Technical Highlights

### **Performance Optimizations**
- Model parameter tuning (temperature: 0.3, max_tokens: 300)
- PDF preview mode for quick analysis
- Session state caching for AI handlers
- Lazy loading of AI providers

### **Security Considerations**
- API keys stored in session state (not persisted)
- Password input fields for API keys
- File size validation before processing
- Input sanitization for SQL queries

### **Responsive Design**
- Mobile-friendly UI components
- Flexible grid layouts
- Adaptive sidebar
- Touch-friendly flashcard interactions

### **Error Handling**
- Graceful degradation to offline mode
- Comprehensive exception handling
- User-friendly error messages
- Diagnostic information for debugging

---

## 📊 Database Schema

### **ipc_sections Table**
- `id` (INTEGER, PRIMARY KEY)
- `section_number` (TEXT, UNIQUE)
- `title` (TEXT)
- `description` (TEXT)
- `applicable_context` (TEXT)
- `punishment` (TEXT)
- `category` (TEXT)
- `keywords` (TEXT)

### **legal_templates Table**
- `id` (INTEGER, PRIMARY KEY)
- `template_name` (TEXT)
- `category` (TEXT)
- `template_content` (TEXT)
- `description` (TEXT)

### **query_history Table**
- `id` (INTEGER, PRIMARY KEY)
- `query` (TEXT)
- `response` (TEXT)
- `timestamp` (DATETIME)

---

## 🎯 Use Cases

1. **Legal Q&A** - Natural language queries about Indian law
2. **Document Analysis** - PDF contract/agreement review
3. **IPC Learning** - Interactive flashcards for law students
4. **IPC Reference** - Quick lookup of penal code sections
5. **Template Access** - Ready-to-use legal document templates

---

## 📝 License & Credits

This project uses open-source technologies and is built for educational and informational purposes. Not a substitute for professional legal advice.

**Built with ❤️ for the Indian legal community**
