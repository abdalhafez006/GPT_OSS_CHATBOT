import os
import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

# Get HF_TOKEN from environment
HF_TOKEN = os.getenv('HF_TOKEN')

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file")

# Initialize the InferenceClient
client = InferenceClient(api_key=HF_TOKEN)

# Language translations
TRANSLATIONS = {
    "English": {
        "title": "🤖 HF GPT-OSS Chatbot",
        "language": "Language",
        "chat_history": "Chat History",
        "new_chat": "➕ New Chat",
        "delete": "🗑️ Delete",
        "clear_history": "🗑️ Clear All History",
        "no_history": "No conversations yet",
        "error": "Error communicating with the model",
        "welcome": "Welcome to the HF GPT-OSS Chatbot! Start a new conversation.",
        "placeholder": "Type your message here...",
        "settings": "⚙️ Settings",
        "confirmation": "Are you sure?",
        "conv_deleted": "Conversation deleted"
    },
    "Arabic": {
        "title": "🤖 روبوت HF GPT-OSS",
        "language": "اللغة",
        "chat_history": "سجل المحادثات",
        "new_chat": "➕ محادثة جديدة",
        "delete": "🗑️ حذف",
        "clear_history": "🗑️ حذف الكل",
        "no_history": "لا توجد محادثات",
        "error": "خطأ في التواصل مع النموذج",
        "welcome": "مرحبا! ابدأ محادثة جديدة.",
        "placeholder": "اكتب رسالتك هنا...",
        "settings": "⚙️ الإعدادات",
        "confirmation": "هل أنت متأكد؟",
        "conv_deleted": "تم حذف المحادثة"
    },
    "Deutsch": {
        "title": "🤖 HF GPT-OSS Chatbot",
        "language": "Sprache",
        "chat_history": "Chatverlauf",
        "new_chat": "➕ Neuer Chat",
        "delete": "🗑️ Löschen",
        "clear_history": "🗑️ Alles löschen",
        "no_history": "Keine Gespräche",
        "error": "Fehler bei der Kommunikation mit dem Modell",
        "welcome": "Willkommen! Starten Sie ein neues Gespräch.",
        "placeholder": "Geben Sie Ihre Nachricht hier ein...",
        "settings": "⚙️ Einstellungen",
        "confirmation": "Sind Sie sicher?",
        "conv_deleted": "Gespräch gelöscht"
    }
}

# Initialize session state
if "language" not in st.session_state:
    st.session_state.language = "English"
if "conversations" not in st.session_state:
    st.session_state.conversations = {}
if "current_conv_id" not in st.session_state:
    st.session_state.current_conv_id = None

# Get current translations
t = TRANSLATIONS[st.session_state.language]

# Streamlit page config
st.set_page_config(
    page_title="HF GPT-OSS Chatbot",
    page_icon="🤖",
    layout="wide"
)

def create_new_conversation():
    """Create a new conversation"""
    conv_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.session_state.conversations[conv_id] = {
        "title": "New Chat",
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": []
    }
    st.session_state.current_conv_id = conv_id
    st.rerun()

def generate_title_from_message(message):
    """Generate a keyword title from a message"""
    # Common words to skip
    skip_words = {'what', 'how', 'can', 'do', 'is', 'the', 'a', 'an', 'to', 'for', 'of', 'and', 'or', 'in', 'on', 'at', 'by', 'with', 'from', 'about', 'if', 'that', 'be', 'are', 'am', 'was', 'were', 'been', 'being'}
    
    # Extract words from message
    words = message.strip().lower().split()
    
    # Find first meaningful word (not in skip list)
    for word in words:
        # Remove punctuation
        clean_word = word.strip('.,!?;:')
        if clean_word and clean_word not in skip_words and len(clean_word) > 2:
            return clean_word.capitalize()
    
    # Fallback: return first word if nothing else found
    return words[0].capitalize() if words else "Chat"

def delete_conversation(conv_id):
    """Delete a conversation"""
    if conv_id in st.session_state.conversations:
        del st.session_state.conversations[conv_id]
        if st.session_state.current_conv_id == conv_id:
            st.session_state.current_conv_id = None
        st.rerun()

def get_current_conversation():
    """Get current conversation messages"""
    if st.session_state.current_conv_id and st.session_state.current_conv_id in st.session_state.conversations:
        return st.session_state.conversations[st.session_state.current_conv_id]["messages"]
    return []

def save_message_to_conversation(role, content):
    """Save message to current conversation"""
    if st.session_state.current_conv_id:
        conv = st.session_state.conversations[st.session_state.current_conv_id]
        
        # Update title from first user message
        if role == "user" and conv["title"] == "New Chat":
            conv["title"] = generate_title_from_message(content)
        
        conv["messages"].append({
            "role": role,
            "content": content
        })

# Sidebar
with st.sidebar:
    st.title(t["settings"])
    
    # Language selector with callback
    selected_language = st.selectbox(
        t["language"],
        ["English", "Arabic", "Deutsch"],
        index=["English", "Arabic", "Deutsch"].index(st.session_state.language),
        key="language_select"
    )
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        st.rerun()
    
    st.divider()
    
    # New Chat Button
    if st.button(f"✨ {t['new_chat']}", use_container_width=True, key="new_chat_btn"):
        create_new_conversation()
    
    st.divider()
    
    # Chat History
    st.subheader(f"📜 {t['chat_history']}")
    
    if st.session_state.conversations:
        for conv_id, conv_data in st.session_state.conversations.items():
            col1, col2 = st.columns([0.85, 0.15])
            
            with col1:
                if st.button(
                    f"💬 {conv_data['title']}\n📝 {len(conv_data['messages'])} msgs",
                    key=f"conv_{conv_id}",
                    use_container_width=True
                ):
                    st.session_state.current_conv_id = conv_id
                    st.rerun()
            
            with col2:
                if st.button("✕", key=f"del_{conv_id}", use_container_width=True):
                    delete_conversation(conv_id)
    else:
        st.info(t["no_history"])
    
    st.divider()
    
    # Clear all history
    if st.button(f"🗑️ {t['clear_history']}", use_container_width=True):
        st.session_state.conversations = {}
        st.session_state.current_conv_id = None
        st.rerun()

# Main content
st.title(t["title"])

# Create first conversation if none exists
if not st.session_state.conversations:
    create_new_conversation()

if st.session_state.current_conv_id:
    # Get current conversation
    current_messages = get_current_conversation()
    
    if not current_messages:
        st.info(t["welcome"])
    
    # Display chat messages
    for message in current_messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Chat input
    if prompt := st.chat_input(t["placeholder"]):
        # Add user message
        save_message_to_conversation("user", prompt)
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate and stream response
        with st.chat_message("assistant"):
            try:
                # Get all messages for API call
                all_messages = get_current_conversation()
                
                # Create streaming response
                response_placeholder = st.empty()
                full_response = ""
                
                # Stream from the model
                stream = client.chat.completions.create(
                    model="openai/gpt-oss-120b:groq",
                    messages=all_messages,
                    stream=True,
                )
                
                # Collect streamed text
                for chunk in stream:
                    if chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.write(full_response)
                
                # Save assistant message
                save_message_to_conversation("assistant", full_response)
                
            except Exception as e:
                error_msg = f"{t['error']}: {str(e)}"
                st.error(error_msg)
                save_message_to_conversation("assistant", error_msg)
