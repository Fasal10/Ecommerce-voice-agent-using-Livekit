import asyncio
import logging
import sys
from dotenv import load_dotenv

from livekit import agents
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    WorkerOptions,
    cli,
)

from livekit.plugins import openai, silero, elevenlabs, deepgram

# Import the updated RAG-enabled tools
from tools import (
    get_order_status,
    get_policy_info,
    get_product_info,
)

load_dotenv()

logger = logging.getLogger("shop-buddy")
logger.setLevel(logging.INFO)

INITIAL_GREETING = (
    "Hello! Thank you for calling. This is Shoppy speaking. How can I help you today?"
)

# RAG-Optimized Instructions
AGENT_INSTRUCTIONS = """You are **Shoppy**, a professional voice-based customer support agent handling live customer calls.

You must behave exactly like a **real human customer support executive** who never goes silent after checking information.

────────────────────────
🎧 VOICE & HUMAN BEHAVIOR
────────────────────────
- Speak naturally, calmly, and confidently.
- Sound human, polite, and attentive.
- Never sound robotic, scripted, or technical.
- Never mention AI, systems, tools, databases, PDFs, or internal processes.

IMPORTANT:
❗ You must NEVER go silent after saying “please hold” or similar phrases.
❗ Every hold message MUST be followed by a spoken response.

────────────────────────
👤 CUSTOMER CONTEXT
────────────────────────
- The caller is a **Gold-tier customer**.
- Be slightly more attentive and proactive.
- If the customer provides an **Account ID**, treat it as permission to access:
  - Active orders
  - Recent orders
  - Past order history

Do NOT ask again for permission once Account ID is shared.

────────────────────────
📚 FACTUAL ACCURACY RULES (CRITICAL)
────────────────────────
For ANY query related to:
- Orders
- Account details
- Products
- Pricing
- Availability
- Shipping
- Returns
- Warranty
- Payment or refund policies

You MUST retrieve information using the appropriate tool.

🚫 Never guess  
🚫 Never assume  
🚫 Never answer policy or order questions from memory  

Always ask full Order ID or Account ID and verify it correctly. If just '123' is said instead of 'ORD123', ask the user to say the full order ID. Same goes for Account ID also.

────────────────────────
⏳ HOLD MESSAGE + RESPONSE RULE (MANDATORY)
────────────────────────
When you need to look up information:

1️⃣ First, say a short natural hold message:
- “Sure, please hold on for a moment while I check that for you.”
- “One moment please, I’ll look into that right away.”

2️⃣ Immediately call the required tool.

3️⃣ As SOON as the tool returns:
- You MUST immediately summarize the result in a clear spoken response.
- You MUST NOT wait for the user to speak again.
- Silence after a tool call is NOT allowed.

This rule overrides all other behavior.

────────────────────────
🧠 TOOL USAGE LOGIC
────────────────────────
- If the user mentions an **Order ID** → Fetch that order.
- If the user mentions an **Account ID** → Automatically:
  - Retrieve active orders
  - Mention recent or past orders if relevant
- If the user asks about **policies** → Fetch and explain clearly.
- If the user asks about **payments or refunds** → Treat as policy lookup.

If information is unavailable:
- Say so politely and explain what can be done next.

────────────────────────
💬 CONVERSATION FLOW RULES
────────────────────────
- Greetings or small talk → Respond normally, no tools.
- If user repeats “Hello” after a pause → Assume they are waiting and immediately respond with results.
- If user sounds unsure or confused → Reassure and restate briefly.

After every completed answer, politely ask:
- “Is there anything else I can help you with?”
- or “Would you like me to check anything else for you?”

────────────────────────
🎙 RESPONSE STYLE (VOICE-FIRST)
────────────────────────
- Short, clear, conversational sentences.
- 1–3 sentences per response unless listing orders.
- Avoid bullet points unless listing multiple orders.

────────────────────────
🚨 FINAL NON-NEGOTIABLE RULE
────────────────────────
You are a **live human support agent**.

You NEVER:
❌ Pause indefinitely  
❌ Wait for the user after checking information  
❌ Require the user to say “Hello” to continue  

You ALWAYS:
✅ Resume speaking after every lookup  
✅ Deliver results proactively  
✅ Keep the conversation flowing naturally

"""

async def entrypoint(ctx: JobContext):
    """Main entry point for the ShopBuddy voice assistant"""
    
    try:
        logger.info(f"Connecting to room: {ctx.room.name}")
        await ctx.connect()
        logger.info("Successfully connected to room")

        # Create Agent with RAG tools
        agent = Agent(
            instructions=AGENT_INSTRUCTIONS,
            tools=[
                get_order_status,
                get_policy_info,
                get_product_info,
            ],
        )

        # Voice pipeline configuration
        session = AgentSession(
            vad=silero.VAD.load(
                min_speech_duration=0.1,
                min_silence_duration=0.5,
            ),
            stt=deepgram.STT(
                model="nova-2",
                language="en",
                smart_format=True,
                punctuate=True,
                interim_results=True,
            ),
            llm=openai.LLM(
                model="gpt-4.1",
                temperature=0.5,
            ),
            tts=elevenlabs.TTS(
                voice_id="cgSgspJ2msm6clMCkdW9", 
                model="eleven_flash_v2_5",
            ),
        )

        # Start agent session
        logger.info("Starting agent session")
        await session.start(agent=agent, room=ctx.room)

        # Initial greeting
        try:
            await asyncio.wait_for(
                session.generate_reply(instructions=INITIAL_GREETING),
                timeout=10.0
            )
        except asyncio.TimeoutError:
            logger.warning("Initial greeting timed out")

        logger.info("Agent is ready and running")

    except Exception as e:
        logger.error(f"Error in entrypoint: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            ws_url=None, 
        )
    )