"""
NyayAI - AI-Powered Legal Assistant
Main Streamlit application
"""
import streamlit as st
import os
from database import NyayAIDatabase
from ai_handler import AIHandler
from pdf_processor import PDFProcessor
from ui_components import (
    apply_custom_css, render_header, render_feature_card_with_navigation, 
    render_chat_message, render_ipc_section, render_template_card,
    render_status_indicator, render_ipc_flashcard, add_keyboard_support
)
from config import APP_TITLE, APP_DESCRIPTION, WELCOME_MESSAGE, MAX_FILE_SIZE_MB

# Page configuration
st.set_page_config(
    page_title="NyayAI - Justice Made Simple",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Home"

if "api_key_configured" not in st.session_state:
    st.session_state.api_key_configured = False

if "ai_handler" not in st.session_state:
    st.session_state.ai_handler = None

# Initialize components
def init_components():
    """Initialize database, AI handler, and PDF processor"""
    try:
        db = NyayAIDatabase()
        # Use cached AI handler or create new one
        if st.session_state.ai_handler is None:
            st.session_state.ai_handler = AIHandler()
        ai = st.session_state.ai_handler
        pdf = PDFProcessor()
        return db, ai, pdf
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return None, None, None

def update_ai_handler(provider_type: str, api_key: str):
    """Update AI handler with new provider and API key"""
    if provider_type and api_key and api_key.strip():
        # Create new AI handler if needed
        if st.session_state.ai_handler is None:
            st.session_state.ai_handler = AIHandler()
        # Configure the provider
        success = st.session_state.ai_handler.update_configuration(provider_type, api_key)
        st.session_state.api_key_configured = success
        return success
    return False

def navigate_to_page(page_name: str):
    """Navigate to a specific page"""
    st.session_state.current_page = page_name
    st.rerun()

def main():
    """Main application function"""
    try:
        # Apply custom styling and keyboard helpers
        apply_custom_css()
        add_keyboard_support()

        # Initialize components
        db, ai, pdf = init_components()
        if db is None:
            st.error("Failed to initialize database. Please refresh the page.")
            return

        # Page options (used for sidebar and navigation)
        page_options = ["🏠 Home", "💬 Legal Q&A", "📄 Document Analysis", "🃏 IPC Flashcards", "📚 IPC Sections", "📋 Legal Templates"]

        # Handle URL query param navigation (e.g., ?page=📚%20IPC%20Sections)
        try:
            params = st.query_params
            if 'page' in params:
                raw_page = params.get('page')
                # Streamlit 1.50 returns str; older experimental API returned [str]
                if isinstance(raw_page, (list, tuple)):
                    raw_page = raw_page[0] if raw_page else ""
                if raw_page:
                    # Decode any URL-encoded value
                    import urllib.parse
                    decoded = urllib.parse.unquote_plus(str(raw_page))
                    # Try exact match; then normalized match
                    target = decoded if decoded in page_options else decoded.strip()
                    if target in page_options:
                        st.session_state.current_page = target
                # Clear query params and rerun to finalize navigation without param lingering
                st.query_params.clear()
                st.rerun()
        except Exception:
            # Non-fatal: if query param handling fails, ignore and continue
            pass

        # Render header
        render_header()

        # AI Status indicator
        render_status_indicator(ai.is_online() if ai else False)

        # Sidebar navigation
        st.sidebar.title("⚖️ NyayAI Navigation")

        # Page selection with current page as default
        current_index = page_options.index(st.session_state.current_page) if st.session_state.current_page in page_options else 0

        page = st.sidebar.selectbox(
            "Choose a feature:",
            page_options,
            index=current_index,
            key="page_selector"
        )

        # Update current page if changed
        if page != st.session_state.current_page:
            st.session_state.current_page = page

        # AI Provider configuration in sidebar
        with st.sidebar.expander("⚙️ Configuration", expanded=not st.session_state.api_key_configured):
            provider_type = st.selectbox(
                "Select AI Provider",
                ["Gemini", "OpenAI", "DeepSeek", "Nemotron"],
                help="Choose your preferred AI provider",
                key="provider_type"
            )

            # All providers now use OpenRouter - single API key source
            st.info("🔑 All AI providers now use OpenRouter API. Get your API key from https://openrouter.ai/keys")
            
            provider_models = {
                "Gemini": "google/gemini-pro-1.5",
                "OpenAI": "openai/gpt-3.5-turbo",
                "DeepSeek": "deepseek/deepseek-chat-v3.1",
                "Nemotron": "nvidia/nemotron-nano-12b-v2-vl:free"
            }

            st.caption(f"Model: {provider_models[provider_type]}")

            api_key = st.text_input(
                "OpenRouter API Key",
                type="password",
                help="Get your OpenRouter API key from https://openrouter.ai/keys - works for all AI providers",
                key="api_key_input"
            )

            if st.button("🔑 Configure API Key", use_container_width=True):
                if not api_key or not api_key.strip():
                    st.warning("⚠️ Please enter a valid OpenRouter API key")
                    return

                # Try to configure the AI handler
                with st.spinner(f"Testing {provider_type} via OpenRouter..."):
                    if st.session_state.ai_handler.update_configuration(provider_type.lower(), api_key):
                        st.success(f"✅ {provider_type} configured successfully via OpenRouter! AI features are now online.")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error(f"""❌ Failed to configure {provider_type} via OpenRouter. Please check:
                        1. The OpenRouter API key is copied correctly
                        2. There are no extra spaces
                        3. Your OpenRouter account is active
                        4. The selected model is available on your plan

                        🔗 Get your API key at: https://openrouter.ai/keys""")

            if st.session_state.api_key_configured and ai and ai.is_online():
                st.success("🟢 AI Online - Full features available")
                if st.button("🔄 Reset API Key"):
                    os.environ.pop("GEMINI_API_KEY", None)
                    st.session_state.api_key_configured = False
                    st.session_state.ai_handler = None
                    st.rerun()

        # Main content based on selected page
        if st.session_state.current_page == "🏠 Home":
            render_home_page()
        elif st.session_state.current_page == "💬 Legal Q&A":
            render_qa_page(db, ai)
        elif st.session_state.current_page == "📄 Document Analysis":
            render_document_page(ai, pdf)
        elif st.session_state.current_page == "🃏 IPC Flashcards":
            render_flashcards_page(db, ai)
        elif st.session_state.current_page == "📚 IPC Sections":
            render_ipc_page(db, ai)
        elif st.session_state.current_page == "📋 Legal Templates":
            render_templates_page(db)
    except Exception as e:
        st.error(f"Application error: {e}")
        st.write("Please refresh the page or contact support.")

def render_home_page():
    """Render the home page with navigation"""
    st.markdown(WELCOME_MESSAGE)
    
    # Feature cards with navigation
    col1, col2 = st.columns(2)
    
    with col1:
        render_feature_card_with_navigation(
            "Legal Q&A Chat",
            "Ask legal questions and get AI-powered answers with relevant IPC sections and practical advice.",
            "💬",
            "💬 Legal Q&A"
        )
        render_feature_card_with_navigation(
            "IPC Flashcards",
            "Interactive flashcards to learn IPC sections with flip animations. Click or press Space to flip!",
            "🃏",
            "🃏 IPC Flashcards"
        )
        render_feature_card_with_navigation(
            "IPC Sections Database",
            "Browse and search through Indian Penal Code sections with detailed explanations.",
            "📚",
            "📚 IPC Sections"
        )
    
    with col2:
        render_feature_card_with_navigation(
            "Document Analysis",
            "Upload PDF documents for AI-powered summarization and legal analysis.",
            "📄",
            "📄 Document Analysis"
        )
        render_feature_card_with_navigation(
            "Legal Templates",
            "Access ready-to-use legal document templates for common legal needs.",
            "📋",
            "📋 Legal Templates"
        )
    
    # Quick stats
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("IPC Sections", "10+", "Core sections")
    with col2:
        st.metric("Legal Templates", "3+", "Ready to use")
    with col3:
        st.metric("Categories", "4+", "Legal areas")
    with col4:
        st.metric("Flashcards", "10+", "Interactive learning")
    
    # FAQ Section
    st.markdown("---")
    st.header("❓ Frequently Asked Questions")
    
    with st.expander("What is NyayAI and how can it help me?"):
        st.markdown("""
        NyayAI is an AI-powered legal assistant designed specifically for Indian users. It helps you:
        - Understand legal concepts and IPC sections in simple terms
        - Get preliminary guidance on legal matters
        - Analyze legal documents and contracts
        - Access legal document templates
        
        Remember: NyayAI is an AI assistant and not a substitute for professional legal advice.
        """)
    
    with st.expander("How accurate are NyayAI's responses?"):
        st.markdown("""
        NyayAI uses advanced AI technology to provide information based on:
        - Indian Penal Code (IPC) sections
        - Legal documentation and precedents
        - Common legal practices
        
        However, legal matters can be complex and situation-specific. Always verify information with a qualified legal professional.
        """)
    
    with st.expander("Is my data secure when using NyayAI?"):
        st.markdown("""
        We take data privacy seriously:
        - All conversations are processed securely
        - Document analysis is performed locally
        - We don't store sensitive user information
        - Uploaded documents are processed temporarily and not permanently stored
        
        For sensitive legal matters, consult with a lawyer in person.
        """)
        
    with st.expander("What should I do if I need immediate legal help?"):
        st.markdown("""
        If you need immediate legal assistance:
        1. Contact a qualified lawyer or legal professional
        2. Reach out to legal aid organizations
        3. Contact your local police station for criminal matters
        4. Document all relevant information and evidence
        
        NyayAI is not equipped to handle emergency situations or provide real-time legal intervention.
        """)

def render_flashcards_page(db, ai):
    """Render the IPC Flashcards page with interactive cards"""
    st.header("🃏 IPC Flashcards - Interactive Learning")
    st.write("Learn Indian Penal Code sections with interactive flashcards. Click 'Flip Card' to see punishment details!")
    
    # Instructions
    with st.expander("📖 How to use Flashcards"):
        st.markdown("""
        **Front Side:** Shows the section number, title, description, and when it applies
        
        **Back Side:** Shows detailed punishment information and sentencing guidelines
        
        **Controls:**
        - Click the "🔄 Flip Card" button to flip any card
        - Each card can be flipped independently
        - Use the search below to filter specific sections
        """)
    
    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "🔍 Search IPC sections for flashcards:",
            placeholder="Enter section number, keywords, or legal term..."
        )
    with col2:
        view_mode = st.selectbox("View Mode", ["Grid View", "List View"])
    
    # Get sections based on search
    try:
        if search_query:
            sections = db.search_ipc_sections(search_query)
            st.subheader(f"🔍 Flashcards for '{search_query}' ({len(sections)} found)")
        else:
            sections = db.get_all_ipc_sections()
            st.subheader(f"🃏 All IPC Flashcards ({len(sections)} sections)")
        
        if sections:
            if view_mode == "Grid View":
                # Grid layout for flashcards
                cols_per_row = 2
                for i in range(0, len(sections), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(sections):
                            section = sections[i + j]
                            with col:
                                render_ipc_flashcard(section, f"section_{section['section']}")
            else:
                # List view - one card per row
                for section in sections:
                    render_ipc_flashcard(section, f"section_{section['section']}")
                    st.markdown("---")
        else:
            st.info("No IPC sections found matching your search criteria.")
            
    except Exception as e:
        st.error(f"Error loading flashcards: {e}")
        st.write("Please try refreshing the page.")

def render_qa_page(db, ai):
    """Render the Legal Q&A page"""
    st.header("💬 Legal Q&A Assistant")
    
    # Show AI status
    if ai and ai.is_online():
        st.success("🤖 AI is online and ready to help!")
    else:
        st.info("🔑 Configure your AI provider in the sidebar for AI-powered responses.")
    
    st.write("Ask your legal questions and get AI-powered assistance with relevant IPC sections.")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Chat interface
    st.subheader("Chat Interface")
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for chat in st.session_state.chat_history:
            render_chat_message(chat["query"], is_user=True)
            render_chat_message(chat["response"], is_user=False)
    
    # Input form
    with st.form("qa_form", clear_on_submit=True):
        user_query = st.text_area(
            "Ask your legal question:",
            placeholder="e.g., What are the legal consequences of cheating in business?",
            height=100
        )
        submitted = st.form_submit_button("Ask NyayAI", use_container_width=True)
        
        if submitted and user_query:
            try:
                # Search for relevant IPC sections first
                relevant_sections = db.search_ipc_sections(user_query)
                
                # Prepare context from IPC sections
                context = ""
                if relevant_sections:
                    context = "Relevant IPC Sections:\n"
                    for section in relevant_sections[:3]:  # Limit to top 3 results
                        context += f"Section {section['section']}: {section['title']} - {section['description']}\n"
                
                # Generate AI response
                with st.spinner("NyayAI is thinking..."):
                    if ai and ai.is_online():
                        response = ai.generate_legal_response(user_query, context)
                    else:
                        response = ai.add_disclaimer(f"**Basic Response (Offline Mode):**\n\nI understand you're asking about: {user_query}\n\nWhile I'm in offline mode, I can provide basic assistance. For detailed AI-powered legal advice, please configure your AI provider in the sidebar.\n\n**General Legal Guidance:**\n- Always consult with a qualified lawyer for specific legal matters\n- Legal consequences depend on specific circumstances and jurisdiction\n- Keep all relevant documents and evidence")
                
                # Save to history
                chat_entry = {"query": user_query, "response": response}
                st.session_state.chat_history.append(chat_entry)
                db.save_query(user_query, response)
                
                # Show relevant IPC sections if found
                if relevant_sections:
                    st.subheader("📚 Relevant IPC Sections")
                    for section in relevant_sections[:3]:
                        render_ipc_section(section)
                
                st.rerun()
            except Exception as e:
                st.error(f"Error processing query: {e}")
    
    # Clear chat button
    if st.button("Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

def render_document_page(ai, pdf):
    """Render the Document Analysis page"""
    st.header("📄 Document Analysis")
    # Diagnostic info to help with environment/package issues
    try:
        import sys
        import importlib
        fitz_spec = importlib.util.find_spec("fitz")
        pymupdf_installed = fitz_spec is not None
        pymupdf_version = None
        if pymupdf_installed:
            try:
                import fitz
                pymupdf_version = getattr(fitz, "__doc__", None) or getattr(fitz, "__version__", None)
            except Exception:
                pymupdf_version = "(installed, import error when reading version)"

        st.caption(f"Python executable: {sys.executable}")
        if pymupdf_installed:
            st.caption(f"PyMuPDF (fitz) detected. Version info: {pymupdf_version}")
        else:
            st.warning("PyMuPDF (fitz) not detected in the runtime used by this Streamlit process.")
    except Exception:
        # Do not crash the page because of diagnostics
        pass
    
    # Show AI status
    if ai and ai.is_online():
        st.success("🤖 AI is online and ready for document analysis!")
    else:
        st.info("🔑 Configure your AI provider in the sidebar for AI-powered document analysis.")
    
    st.write("Upload PDF documents for AI-powered legal analysis and summarization.")
    
    # Check PDF processor availability
    if not pdf or not pdf.is_available():
        st.error("PDF processing is not available. Please install PyMuPDF library.")
        st.code("pip install PyMuPDF")
        return
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        help=f"Maximum file size: {MAX_FILE_SIZE_MB}MB"
    )
    
    if uploaded_file is not None:
        # Enforce app-level file size limit to match config and Streamlit server setting
        try:
            size_bytes = getattr(uploaded_file, "size", None)
            if size_bytes is None:
                # Fallback: try to compute size from buffer
                size_bytes = len(uploaded_file.getbuffer())
        except Exception:
            size_bytes = None

        if size_bytes is not None:
            max_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
            if size_bytes > max_bytes:
                st.error(f"File is too large: {(size_bytes/1024/1024):.1f} MB. Maximum allowed is {MAX_FILE_SIZE_MB} MB.")
                return

        try:
            # Display file info
            file_info = pdf.get_pdf_info(uploaded_file)
            
            if "error" not in file_info:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**File Information:**")
                    st.write(f"📄 **Pages:** {file_info['pages']}")
                    st.write(f"📝 **Title:** {file_info['title']}")
                    st.write(f"👤 **Author:** {file_info['author']}")
                
                with col2:
                    st.write("**Analysis Options:**")
                    analysis_type = st.selectbox(
                        "Choose analysis type:",
                        ["Full Document Summary", "Page Preview", "Extract Text Only"]
                    )
            
            # Quick analysis section
            col1, col2 = st.columns(2)
            
            with col1:
                # Quick Preview - Always show this immediately
                st.subheader("📖 Quick Preview")
                with st.spinner("Loading preview..."):
                    text, success = pdf.extract_text_from_pdf(uploaded_file, max_pages=2, preview_mode=True)
                    if success:
                        st.markdown(text)
                    else:
                        st.error(text)
            
            with col2:
                st.subheader("🎯 Analysis Options")
                analysis_type = st.radio(
                    "Choose analysis type:",
                    ["Quick Summary (2 pages)", "Full Analysis", "Extract Text"]
                )
                
                if st.button("🚀 Start Analysis", use_container_width=True):
                    with st.spinner("Processing document..."):
                        if analysis_type == "Quick Summary (2 pages)":
                            # Quick analysis of first 2 pages
                            text, success = pdf.extract_text_from_pdf(uploaded_file, max_pages=2, preview_mode=True)
                            if success and ai and ai.is_online():
                                with st.spinner("Generating quick summary..."):
                                    summary = ai.summarize_document(text)
                                st.success("✅ Quick summary generated!")
                                st.markdown(summary)
                            
                        elif analysis_type == "Full Analysis":
                            # Full document analysis with progress
                            text, success = pdf.extract_text_from_pdf(uploaded_file, preview_mode=False)
                            if success:
                                if ai and ai.is_online():
                                    with st.spinner("Analyzing full document..."):
                                        summary = ai.summarize_document(text)
                                    st.success("✅ Full analysis completed!")
                                    st.markdown(summary)
                                    
                                    with st.expander("📄 View Full Text"):
                                        st.text_area("Document Text", text, height=300)
                                else:
                                    st.warning("AI is offline. Please configure API key for full analysis.")
                                    
                        else:  # Extract Text
                            text, success = pdf.extract_text_from_pdf(uploaded_file)
                            if success:
                                st.markdown("📝 Extracted Text")
                                st.text_area("Document Text", text, height=400)
                                st.download_button(
                                    label="⬇️ Download Text",
                                    data=text,
                                    file_name=f"{uploaded_file.name}_extracted.txt",
                                    mime="text/plain"
                                )
                        
                        if success:
                            st.subheader("📝 Extracted Text")
                            st.text_area("Document Text", text, height=400)
                            
                            # Download button for extracted text
                            st.download_button(
                                label="⬇️ Download Text",
                                data=text,
                                file_name=f"{uploaded_file.name}_extracted.txt",
                                mime="text/plain"
                            )
                        else:
                            st.error(f"Failed to extract text: {text}")
        except Exception as e:
            st.error(f"Error processing document: {e}")

def render_ipc_page(db, ai):
    """Render the IPC Sections page"""
    st.header("📚 Indian Penal Code Sections")
    st.write("Browse and search through IPC sections with AI-powered explanations.")
    
    # Search functionality
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input(
            "Search IPC sections:",
            placeholder="Enter section number, keywords, or legal term..."
        )
    with col2:
        search_button = st.button("🔍 Search", use_container_width=True)
    
    try:
        # Display sections
        if search_query or search_button:
            if search_query:
                sections = db.search_ipc_sections(search_query)
                st.subheader(f"🔍 Search Results for '{search_query}'")
            else:
                sections = db.get_all_ipc_sections()
                st.subheader("📚 All IPC Sections")
        else:
            sections = db.get_all_ipc_sections()
            st.subheader("📚 All IPC Sections")
        
        if sections:
            # Display sections with AI explanation option
            for section in sections:
                with st.expander(f"Section {section['section']}: {section['title']}"):
                    render_ipc_section(section)
                    
                    # Additional details if available
                    if 'context' in section:
                        st.markdown("**📋 Context:**")
                        st.write(section['context'])
                    
                    if 'punishment' in section:
                        st.markdown("**⚖️ Punishment:**")
                        st.write(section['punishment'])
                    
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button(f"🤖 AI Explanation", key=f"explain_{section['section']}"):
                            if ai and ai.is_online():
                                with st.spinner("Getting AI explanation..."):
                                    explanation = ai.explain_ipc_section(section)
                                    st.markdown("**🎯 AI Explanation:**")
                                    st.markdown(explanation)
                            else:
                                st.info("🔑 Configure your AI provider in the sidebar for AI explanations")
                    
                    with col2:
                        if st.button(f"📋 Copy Section", key=f"copy_{section['section']}"):
                            section_text = f"IPC Section {section['section']}: {section['title']}\n\n{section['description']}"
                            if 'punishment' in section:
                                section_text += f"\n\nPunishment: {section['punishment']}"
                            st.code(section_text)
        else:
            st.info("No IPC sections found matching your search criteria.")
    except Exception as e:
        st.error(f"Error loading IPC sections: {e}")

def render_templates_page(db):
    """Render the Legal Templates page"""
    st.header("📋 Legal Document Templates")
    st.write("Access ready-to-use legal document templates for common legal needs.")
    
    try:
        # Get templates
        templates = db.get_legal_templates()
        
        # Category filter
        categories = list(set([template['category'] for template in templates]))
        selected_category = st.selectbox(
            "Filter by category:",
            ["All Categories"] + categories
        )
        
        # Filter templates
        if selected_category != "All Categories":
            filtered_templates = [t for t in templates if t['category'] == selected_category]
        else:
            filtered_templates = templates
        
        # Display templates
        if filtered_templates:
            for template in filtered_templates:
                with st.expander(f"📄 {template['name']} ({template['category']})"):
                    render_template_card(template)
                    
                    # Template content
                    st.markdown("**📝 Template Content:**")
                    st.text_area(
                        "Template",
                        template['content'],
                        height=300,
                        key=f"template_{template['name']}"
                    )
                    
                    # Download button
                    st.download_button(
                        label="⬇️ Download Template",
                        data=template['content'],
                        file_name=f"{template['name'].replace(' ', '_')}.txt",
                        mime="text/plain",
                        key=f"download_{template['name']}"
                    )
        else:
            st.info("No templates found for the selected category.")
    except Exception as e:
        st.error(f"Error loading templates: {e}")
    
    # Add custom template section
    st.markdown("---")
    st.subheader("➕ Need a Custom Template?")
    st.info("For custom legal document templates, please consult with a qualified legal professional or use our AI Q&A feature to get guidance on specific legal document requirements.")

if __name__ == "__main__":
    main()