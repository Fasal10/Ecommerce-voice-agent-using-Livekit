# Environment Setup Notes

## Creating .env File

Your `.env` file should contain these API keys:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=APIxxxxxxxxxxxxx
LIVEKIT_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxx
ELEVEN_API_KEY=sk_xxxxxxxxxxxxxxxxxxxxxx
DEEPGRAM_API_KEY=xxxxxxxxxxxxxxxxxxxxxx
```

## ⚠️ Security Warning

**NEVER share your `.env` file with anyone!**

It contains sensitive API keys that can:
- Cost you money if misused
- Access your accounts
- Violate service terms

## For Submission

When submitting this project:
1. **DO NOT include your `.env` file**
2. Create a `.env.example` file instead with placeholders:

```env
LIVEKIT_URL=wss://your-project.livekit.cloud
LIVEKIT_API_KEY=your_api_key_here
LIVEKIT_API_SECRET=your_api_secret_here
OPENAI_API_KEY=sk-proj-your_key_here
ELEVEN_API_KEY=sk_your_key_here
DEEPGRAM_API_KEY=your_key_here
```

## Getting API Keys

### LiveKit
1. Go to https://cloud.livekit.io/
2. Sign up and create a project
3. Copy: WebSocket URL, API Key, API Secret

### OpenAI
1. Go to https://platform.openai.com/
2. Create account and navigate to API Keys
3. Create new key (starts with `sk-proj-`)

### ElevenLabs
1. Go to https://elevenlabs.io/
2. Sign up and go to Profile → API Keys
3. Generate key (starts with `sk_`)

### Deepgram
1. Go to https://console.deepgram.com/
2. Sign up and navigate to API Keys
3. Create new key