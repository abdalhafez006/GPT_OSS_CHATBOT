# 🤖 HF GPT-OSS Chatbot

A modern, multi-language chatbot powered by Hugging Face's GPT-OSS-120B model through Groq. Built with Streamlit for a sleek, user-friendly interface.

## ✨ Features

- **🌐 Multi-Language Support**: English, Arabic (العربية), and German (Deutsch)
- **⚡ Real-time Streaming**: Experience smooth, streaming responses from the AI model
- **💬 Conversation History**: Organize multiple conversations with auto-generated keyword titles
- **🎯 Smart Chat Naming**: Conversations are automatically named based on the first user message
- **🗑️ Conversation Management**: 
  - Create new conversations
  - Delete individual conversations
  - Clear all history at once
- **📱 Responsive Design**: Clean, professional interface that works on all screen sizes
- **🔐 Secure Token Management**: HF_TOKEN loaded from `.env` file

## 📋 Requirements

- Python 3.8+
- pip or conda

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/abdalhafez006/GPT_OSS_CHATBOT.git
cd "HF-GptOss-Assistent chatbot"
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate  # On Windows
source .venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```
HF_TOKEN=your_huggingface_token_here
```

Get your token from: https://huggingface.co/settings/tokens

## 📖 Usage

### Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Terminal-Based CLI
```bash
python app.py
```

Simple command-line chatbot for terminal users.

## 🎨 UI Features

### Sidebar
- **Language Selector**: Switch between 3 languages instantly
- **New Chat Button**: Start fresh conversations
- **Chat History**: View all previous conversations with message counts
- **Delete Button**: Remove individual conversations
- **Clear All**: Delete entire conversation history

### Main Chat Area
- Message display with user/bot distinction
- Real-time streaming responses
- Clean chat input interface

## 🗣️ Supported Languages

| Language | Code |
|----------|------|
| English | EN |
| العربية (Arabic) | AR |
| Deutsch (German) | DE |

## 📦 Project Structure

```
HF-GptOss-Assistent chatbot/
├── streamlit_app.py          # Main Streamlit web application
├── app.py                    # CLI version
├── .env                      # Environment variables (create this)
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Technologies Used

- **Streamlit**: Modern web framework for Python
- **Hugging Face Hub**: Access to GPT-OSS model
- **Python 3.10+**: Programming language
- **Groq**: High-performance inference for GPT-OSS

## 💡 How It Works

1. **Authentication**: Your HF_TOKEN is loaded from `.env` file
2. **Session Management**: Streamlit maintains conversation state
3. **Smart Naming**: First user message is analyzed to create a keyword title
4. **Streaming**: Model responses stream in real-time for better UX
5. **Persistence**: Conversations persist during your session (stored in memory)

## 🌟 Key Features Explained

### Auto-Generated Titles
When you start a new chat, the title is automatically generated from your first message:
- Extracts meaningful keywords (skips common words)
- Examples:
  - "What is Python?" → `Python`
  - "How to learn machine learning?" → `Learning`
  - "Tell me about AI" → `About`

### Conversation History
- View all previous conversations in the sidebar
- Each shows message count
- One-click to switch between chats
- Individual delete buttons for each conversation

### Multi-Language Support
- All UI text translates instantly
- Conversation history titles work in any language
- Full support for RTL languages (Arabic)

## 🐛 Troubleshooting

### "HF_TOKEN not found in .env file"
- Ensure `.env` file exists in the project root
- Verify token is correctly added: `HF_TOKEN=hf_xxxxx...`

### Streamlit not starting
```bash
pip install --upgrade streamlit
```

### Slow responses
- Check your internet connection
- Verify HF_TOKEN is valid
- Groq API may have rate limits

## 📝 Example Usage

1. Launch the app: `streamlit run streamlit_app.py`
2. Select your preferred language from the sidebar
3. Type your first message (this becomes the chat title)
4. Watch the AI response stream in real-time
5. Continue the conversation or start a new chat
6. Delete conversations individually or clear all history

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest improvements
- Add new features

## 📄 License

This project is open source and available under the MIT License.

## 🔗 Links

- [Hugging Face Hub](https://huggingface.co/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Groq](https://console.groq.com/)

## 📧 Support

For issues or questions, please create an issue on the GitHub repository.

---

**Built with ❤️ using Streamlit and Hugging Face**
