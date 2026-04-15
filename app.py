import os
import json
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

# Load hftoken from .env first, then check Streamlit secrets (for cloud deployment)
def get_hf_token():
    """Get HuggingFace token from .env or Streamlit secrets"""
    token = os.getenv('HF_TOKEN')
    if token:
        return token
    
    # Try to get from Streamlit secrets (for cloud deployment)
    try:
        if "HF_TOKEN" in st.secrets:
            return st.secrets["HF_TOKEN"]
    except:
        pass
    
    return None

hftoken = get_hf_token()

if hftoken is None:
    st.error("❌ HF_TOKEN not found! Please set your HuggingFace token.")
    st.info("""
    **Local Setup:** Create a `.env` file with:
    ```
    HF_TOKEN=your_token_here
    ```
    
    **Streamlit Cloud:** Add to your app's secrets in the Streamlit Cloud dashboard.
    """)
    st.stop()

# Translations dictionary
TRANSLATIONS = {
    "en": {
        "title": "🤖 HuggingFace GPT-OSS Chatbot",
        "subtitle": "Powered by GPT-OSS 120B (via Groq)",
        "language": "Language",
        "english": "English",
        "arabic": "العربية",
        "german": "Deutsch",
        "chat_history": "Chat History",
        "new_chat": "New Chat",
        "clear_history": "Clear History",
        "placeholder": "Type your message here...",
        "send": "Send",
        "no_history": "No chat history yet",
        "model": "Model: GPT-OSS 120B",
        "copy": "Copy",
        "delete": "Delete",
        "settings": "⚙️ Settings",
        "about": "ℹ️ About",
        "temperature": "Temperature",
        "max_tokens": "Max Tokens",
    },
    "ar": {
        "title": "🤖 روبوت محادثة HuggingFace GPT-OSS",
        "subtitle": "مدعوم بواسطة GPT-OSS 120B (عبر Groq)",
        "language": "اللغة",
        "english": "English",
        "arabic": "العربية",
        "german": "Deutsch",
        "chat_history": "سجل الدردشة",
        "new_chat": "دردشة جديدة",
        "clear_history": "مسح السجل",
        "placeholder": "اكتب رسالتك هنا...",
        "send": "إرسال",
        "no_history": "لا يوجد سجل دردشة حتى الآن",
        "model": "النموذج: GPT-OSS 120B",
        "copy": "نسخ",
        "delete": "حذف",
        "settings": "⚙️ الإعدادات",
        "about": "ℹ️ حول",
        "temperature": "درجة الحرارة",
        "max_tokens": "الحد الأقصى للرموز",
    },
    "de": {
        "title": "🤖 HuggingFace GPT-OSS-Chatbot",
        "subtitle": "Unterstützt von GPT-OSS 120B (über Groq)",
        "language": "Sprache",
        "english": "English",
        "arabic": "العربية",
        "german": "Deutsch",
        "chat_history": "Chatverlauf",
        "new_chat": "Neuer Chat",
        "clear_history": "Verlauf löschen",
        "placeholder": "Geben Sie Ihre Nachricht hier ein...",
        "send": "Senden",
        "no_history": "Noch kein Chatverlauf",
        "model": "Modell: GPT-OSS 120B",
        "copy": "Kopieren",
        "delete": "Löschen",
        "settings": "⚙️ Einstellungen",
        "about": "ℹ️ Über",
        "temperature": "Temperatur",
        "max_tokens": "Maximale Token",
    }
}

def get_text(key, lang):
    """Get translated text"""
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "history" not in st.session_state:
        st.session_state.history = []
    if "language" not in st.session_state:
        st.session_state.language = "en"

def apply_theme():
    """Apply dark theme to Streamlit"""
    st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stSidebar {
        background-color: #010409 !important;
        color: #c9d1d9 !important;
    }
    [data-testid="stSidebar"] * {
        color: #c9d1d9 !important;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] h5, 
    [data-testid="stSidebar"] h6 {
        color: #c9d1d9 !important;
    }
    .stChatMessage {
        background-color: #161b22;
        color: #c9d1d9;
    }
    </style>
    """, unsafe_allow_html=True)

def stream_response(messages):
    """Stream response from the model"""
    try:
        client = InferenceClient(token=hftoken)
        
        response_text = ""
        
        # Use chat.completions.create for streaming
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b:groq",
            messages=messages,
            stream=True,
            temperature=st.session_state.get("temperature", 0.7),
            max_tokens=st.session_state.get("max_tokens", 512),
        )
        
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response_text += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
        
        return response_text
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        yield error_msg

def save_to_history():
    """Save entire conversation to history"""
    if not st.session_state.messages:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Extract keywords from first user message for naming
    first_user_msg = next((m["content"] for m in st.session_state.messages if m["role"] == "user"), "Conversation")
    keywords = extract_keywords(first_user_msg)
    chat_name = keywords if keywords else first_user_msg[:30]
    
    chat_entry = {
        "timestamp": timestamp,
        "name": chat_name,
        "messages": st.session_state.messages.copy()  # Store entire conversation
    }
    st.session_state.history.append(chat_entry)

def extract_keywords(text):
    """Extract keywords from text for naming conversations"""
    # Common words to exclude
    stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been", "been", 
                  "what", "how", "why", "tell", "me", "please", "can", "could", "would"}
    
    words = text.lower().split()
    keywords = [w.strip(".,!?;:") for w in words if len(w) > 3 and w.lower() not in stop_words]
    
    if keywords:
        return " ".join(keywords[:3])
    return text[:20]

def main():
    """Main Streamlit app"""
    initialize_session_state()
    
    # Configure page
    st.set_page_config(
        page_title="GPT-OSS Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar configuration
    with st.sidebar:
        st.header(get_text("settings", st.session_state.language))
        
        lang = st.session_state.language
        
        # Language selection
        lang_options = {"English": "en", "العربية": "ar", "Deutsch": "de"}
        selected_lang = st.selectbox(
            get_text("language", lang),
            options=lang_options.keys(),
            index=["en", "ar", "de"].index(st.session_state.language),
            key="lang_select"
        )
        if lang_options[selected_lang] != st.session_state.language:
            st.session_state.language = lang_options[selected_lang]
            st.rerun()
        
        st.divider()
        
        # Additional Options
        st.subheader("🎛️ Advanced Options")
        
        if "temperature" not in st.session_state:
            st.session_state.temperature = 0.7
        if "max_tokens" not in st.session_state:
            st.session_state.max_tokens = 512
        
        temp = st.slider(
            get_text("temperature", lang),
            min_value=0.0,
            max_value=2.0,
            value=st.session_state.temperature,
            step=0.1,
            help="Higher values = more creative, Lower values = more focused"
        )
        st.session_state.temperature = temp
        
        tokens = st.number_input(
            get_text("max_tokens", lang),
            min_value=1,
            max_value=2048,
            value=st.session_state.max_tokens,
            step=100,
            help="Maximum number of tokens in response"
        )
        st.session_state.max_tokens = tokens
        
        st.divider()
        
        # Chat History
        lang = st.session_state.language
        st.subheader(get_text("chat_history", lang))
        
        if st.button(get_text("new_chat", lang), use_container_width=True):
            # Auto-save current chat before starting new one
            if st.session_state.messages:
                save_to_history()
            st.session_state.messages = []
            st.rerun()
        
        if st.button(get_text("clear_history", lang), use_container_width=True):
            st.session_state.history = []
            st.rerun()
        
        st.divider()
        
        # Display history with full conversations
        if st.session_state.history:
            st.subheader("📋 Recent Chats")
            for i, chat in enumerate(reversed(st.session_state.history[-5:])):
                chat_name = chat.get("name", f"Chat {i+1}")
                with st.expander(f"💬 {chat_name}", expanded=False):
                    # Display full conversation
                    messages = chat.get("messages", [])
                    for msg in messages:
                        role = msg["role"]
                        content = msg["content"]
                        if role == "user":
                            st.markdown(f"**👤:** {content}")
                        else:
                            st.markdown(f"**🤖:** {content}")
                    
                    # Load conversation button
                    if st.button(f"Load this chat", key=f"load_{i}_{chat['timestamp']}", use_container_width=True):
                        st.session_state.messages = messages
                        st.rerun()
                    
                    st.caption(f"⏰ {chat['timestamp']}")
        else:
            st.info(get_text("no_history", lang))
        
        st.divider()
        st.markdown("---")
        st.subheader(get_text("about", lang))
        st.markdown(f"**{get_text('model', lang)}**")
        st.caption("Built with Streamlit & HuggingFace")
    
    # Apply dark theme
    apply_theme()
    
    # Main content
    lang = st.session_state.language
    st.title(get_text("title", lang))
    st.caption(get_text("subtitle", lang))
    
    # Display messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input(get_text("placeholder", lang)):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Prepare messages for API
        api_messages = [{"role": m["role"], "content": m["content"]} 
                        for m in st.session_state.messages]
        
        # Stream response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            for chunk in stream_response(api_messages):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": full_response})

if __name__ == "__main__":
    main()
