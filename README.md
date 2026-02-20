# E-Commerce Voice Bot with RAG

A sophisticated voice-based customer support agent powered by LiveKit, OpenAI, and Retrieval-Augmented Generation (RAG) for accurate, real-time customer service.

## 🎯 Project Overview

This project implements an intelligent voice assistant (Shoppy) that handles customer inquiries about orders, products, and policies using natural language processing and a RAG-based knowledge retrieval system.

### Key Features

- **Voice-First Interface**: Natural conversation using Deepgram STT and ElevenLabs TTS
- **RAG-Powered Responses**: Retrieves accurate information from PDF knowledge base using FAISS vector store
- **Real-Time Order Tracking**: Instant order status and delivery information lookup
- **Policy Information**: Automated responses for shipping, returns, refunds, and warranties
- **Product Catalog**: Live product availability, pricing, and specifications

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Customer  │────▶│   LiveKit    │────▶│   Deepgram │
│    Voice    │     │   Gateway    │     │     STT     │
└─────────────┘     └──────────────┘     └─────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  Agent Core  │
                    │  (OpenAI)    │
                    └──────────────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
         ┌──────────┐ ┌─────────┐ ┌─────────┐
         │  Order   │ │ Policy  │ │ Product │
         │  Lookup  │ │  Info   │ │  Info   │
         └──────────┘ └─────────┘ └─────────┘
                │           │           │
                └───────────┼───────────┘
                            ▼
                    ┌──────────────┐
                    │ FAISS Vector │
                    │   Database   │
                    └──────────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │  ElevenLabs  │
                    │     TTS      │
                    └──────────────┘
```

## 📋 Prerequisites

- Python 3.8 or higher
- OpenAI API key
- LiveKit account and credentials
- ElevenLabs API key
- Deepgram API key

## 🚀 Installation

### 1. Unzip the zip file.

#### You will get the project files

### 2. Create Conda Environment

```bash
# Create conda environment
conda create -n Voicebot python=3.11 -y

# Activate environment
conda activate Voicebot
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
LIVEKIT_URL=your_livekit_url
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
OPENAI_API_KEY=your_openai_key
ELEVEN_API_KEY=your_elevenlabs_key
DEEPGRAM_API_KEY=your_deepgram_key
```

### 5. Set Up Knowledge Base

1. Place your PDF knowledge base in the `pdf/` directory
2. Update the path in `pdf_processing.py` if needed
3. Run the vector database creation:

```bash
python pdf_processing.py
```

This creates a FAISS vector store in the `vector_db/` directory.

## 🎮 Usage

### Running the Agent

```bash
python agent.py dev
```

The agent will:
1. Connect to your LiveKit room
2. Initialize the voice pipeline
3. Greet customers automatically
4. Handle inquiries using RAG-powered tools

### Testing the Agent

Once running, connect to your LiveKit room using:
- LiveKit web interface [agents playground]
- Custom frontend application
- LiveKit mobile SDKs

## 🛠️ Project Structure

```
ecommerce-voice-bot/
│
├── agent.py              # Main agent entry point
├── tools.py              # RAG-enabled function tools
├── pdf_processing.py     # Vector database creation
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (not in repo)
├── README.md            # This file
│
├── pdf/                 # Knowledge base PDFs
│   └── ecommerce_bot.pdf
│
├── vector_db/           # Generated FAISS index
│   ├── index.faiss
│   └── index.pkl
│
└── logs/                # Application logs (optional)
```

## 🔧 Configuration

### Agent Behavior

Modify `AGENT_INSTRUCTIONS` in `agent.py` to customize:
- Greeting style
- Response tone
- Customer tier handling
- Conversation flow

### RAG Parameters

Adjust in `pdf_processing.py`:
- `chunk_size`: Text chunk size (default: 600)
- `chunk_overlap`: Overlap between chunks (default: 100)
- `k`: Number of results to retrieve (default: 3)

### Voice Settings

Configure in `agent.py`:
- STT model: Deepgram Nova-2
- LLM: GPT-4.1 (temperature: 0.5)
- TTS: ElevenLabs Flash v2.5

## 📊 Available Tools

### 1. get_order_status
Retrieves order status and delivery information by Order ID.

**Example**: "What's the status of order ORD123?"

### 2. get_policy_info
Fetches company policies on shipping, returns, refunds, and warranties.

**Example**: "What's your return policy?"

### 3. get_product_info
Looks up product availability, pricing, and specifications.

**Example**: "Do you have the iPhone 15 in stock?"

## 🔒 Security Notes

- **Never share your `.env` file** - It contains sensitive API keys
- Store API keys securely
- Use environment variables for sensitive data
- Implement rate limiting in production
- Enable authentication for LiveKit rooms

**IMPORTANT**: Before sharing this project, create a `.env.example` file with placeholder values instead of your actual keys.

## 🐛 Troubleshooting

### Vector DB Not Loading
```
Error: Vector DB path not found
```
**Solution**: Run `python pdf_processing.py` to create the vector database.

### Connection Timeout
```
Error: Failed to connect to LiveKit room
```
**Solution**: Verify your LiveKit credentials in `.env` file.

### Audio Issues
```
Error: No audio output
```
**Solution**: Check ElevenLabs API quota and voice ID configuration.

## 📝 Development Notes

### Adding New Tools

1. Define the function in `tools.py`:
```python
@function_tool
async def your_new_tool(param: str):
    """Tool description"""
    context = await query_rag(f"Your query about {param}")
    return context
```

2. Register in `agent.py`:
```python
tools=[
    get_order_status,
    get_policy_info,
    get_product_info,
    your_new_tool,  # Add here
]
```

### Updating Knowledge Base

1. Replace or add PDFs in `pdf/` directory
2. Update path in `pdf_processing.py`
3. Run: `python pdf_processing.py`
4. Restart the agent

## 🚢 Future Enhancements

- [ ] Docker containerization
- [ ] Multi-language support
- [ ] Sentiment analysis
- [ ] Call transcription storage
- [ ] Analytics dashboard
- [ ] Escalation to human agents

## 📄 License

This project is developed for educational purposes.

## 👥 Contributors

- Project Developer: [Your Name]
- Course: [Course Name]

## 🙏 Acknowledgments

- LiveKit for real-time communication infrastructure
- OpenAI for GPT-4.1 and embeddings
- ElevenLabs for natural TTS
- Deepgram for accurate speech recognition
- LangChain for RAG implementation

---

**Last Updated**: January 2026