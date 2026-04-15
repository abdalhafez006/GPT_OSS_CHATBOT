# 🤖 HuggingFace GPT-OSS Chatbot

A powerful, user-friendly chatbot web application powered by HuggingFace's GPT-OSS 20B model with streaming responses.

## ✨ Features

- **⚡ Real-time Streaming** - Get responses streamed instantly as they're generated
- **💬 Conversation History** - Automatically save and restore complete conversations
- **🌍 Multi-language Support** - Available in English, Arabic (العربية), and German (Deutsch)
- **🎨 Dark Mode UI** - Sleek dark interface with Streamlit
- **⚙️ Advanced Controls** - Adjust temperature and max tokens for response control
- **📱 Responsive Design** - Works seamlessly on desktop and tablet devices
- **🔒 Secure API** - Token management via environment variables

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- HuggingFace API token (get from [huggingface.co](https://huggingface.co))
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/abdalhafez006/GPT_Oss-Chatbot.git
   cd GPT_Oss-Chatbot
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```
   HF_TOKEN=your_huggingface_token_here
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

The app will open in your browser at `http://localhost:8501`

## � Streamlit Cloud Deployment

To deploy on Streamlit Cloud:

1. **Push your code to GitHub** (already done!)

2. **Go to [Streamlit Cloud](https://share.streamlit.io/)** and sign in with GitHub

3. **Create new app** and select this repository:
   - Repository: `abdalhafez006/GPT_Oss-Chatbot`
   - Branch: `main`
   - Main file path: `app.py`

4. **Add secrets** (important!):
   - Click on "Advanced settings"
   - Under "Secrets", add your HuggingFace token:
   ```
   HF_TOKEN = "your_huggingface_token_here"
   ```

5. **Deploy** - Your app will be live in seconds!

## �🎯 Usage

1. **Start a Conversation** - Type your message in the input box at the bottom
2. **Adjust Settings** - Use the sidebar to:
   - Switch languages (English/Arabic/German)
   - Control response creativity (Temperature slider)
   - Set maximum response length (Max Tokens)
3. **View History** - See your previous conversations in the sidebar
4. **Load Conversations** - Click "Load this chat" to restore any saved conversation
5. **Start Fresh** - Click "New Chat" to begin a new conversation (current one is auto-saved)

## 🔧 Configuration

### Temperature
- **Lower values (0.0-0.5)** - More focused, deterministic responses
- **Medium values (0.5-1.0)** - Balanced responses
- **Higher values (1.0-2.0)** - More creative, diverse responses

### Max Tokens
- Number of tokens in the generated response
- Higher values = longer responses
- Range: 1-2048

## 📦 Dependencies

- **streamlit** - Web UI framework
- **python-dotenv** - Environment variable management
- **huggingface-hub** - HuggingFace API client

## 📁 Project Structure

```
GPT_Oss-Chatbot/
├── app.py              # Main Streamlit application
├── .env                # Environment variables (not in repo)
├── .gitignore          # Git ignore file
├── README.md           # This file
└── requirements.txt    # Python dependencies
```

## 🌐 Supported Languages

- **English** - Full interface translation
- **العربية (Arabic)** - Complete Arabic interface
- **Deutsch (German)** - Complete German interface

## 🔐 Security Notes

- Never commit your `.env` file or API tokens
- Keep your HuggingFace token private
- The `.env` file is listed in `.gitignore` for security

## 💡 Tips & Tricks

- Use clear, specific prompts for better responses
- Experiment with temperature to find your sweet spot
- Load previous conversations to continue discussions
- History is automatically saved when creating a new chat

## 🐛 Troubleshooting

### "HFTOKEN not found"
- Ensure your `.env` file contains `HF_TOKEN=your_token`
- Verify the file is in the project root directory

### Application crashes
- Check your internet connection
- Verify your HuggingFace token is valid
- Ensure all dependencies are installed: `pip install -r requirements.txt`

### Slow responses
- Check your internet connection
- Verify Groq services are operational
- Try reducing max tokens

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [HuggingFace](https://huggingface.co/) for the model and API
- [Groq](https://groq.com/) for the inference infrastructure
- [Streamlit](https://streamlit.io/) for the web framework

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Made with ❤️ by abdalhafez006**
