import logging
import asyncio
from dotenv import load_dotenv
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli, llm
try:
    from livekit.agents.voice.agent_session import AgentSession
except ImportError:
    # Fallback or error handling if path is different (e.g. 1.0 vs 1.3)
    from livekit.agents.pipeline import VoicePipelineAgent as AgentSession

from livekit.plugins import openai
from livekit.plugins import deepgram
from livekit.plugins import silero
from livekit.plugins import elevenlabs
from prompt_manager import PromptManager
from knowledge_base import KnowledgeBase
from tools import AgentTools

load_dotenv()
logger = logging.getLogger("voicebot")

async def entrypoint(ctx: JobContext):
    logger.info("ENTRYPOINT TRIGGERED! Job Received.")
    # Initialize dynamic components
    prompt_manager = PromptManager()
    knowledge_base = KnowledgeBase()
    
    # Initialize contexts
    initial_ctx = llm.ChatContext()
    initial_ctx.add_message(role="system", content=prompt_manager.get_prompt())

    logger.info(f"Connecting to room {ctx.room.name}")
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Wait for the first participant (important for SIP calls to know who we are talking to)
    logger.info("Waiting for participant...")
    participant = await ctx.wait_for_participant()
    logger.info(f"Participant connected: {participant.identity}")

    # Extract Caller ID if available (SIP usually puts phone number in identity or name)
    caller_id = participant.identity 
    
    # Use the correct Agent class from voice module
    from livekit.agents.voice import Agent
    from tools import AgentTools
    
    # Define our custom Agent that includes the tools
    class VoiceBotAgent(Agent, AgentTools):
        pass

    from livekit.agents import AgentSession

    # Initialize Agent with components
    agent = VoiceBotAgent(
        instructions=prompt_manager.get_prompt(),
        vad=silero.VAD.load(
            min_silence_duration=0.1,
            min_speech_duration=0.1,
        ),
        stt=deepgram.STT(model="nova-2", language="hi"),
        tts=elevenlabs.TTS(
            voice_id="DpnM70iDHNHZ0Mguv6GJ",
            voice_settings=elevenlabs.VoiceSettings(
                stability=0.5,
                similarity_boost=0.75,
            ),
            model="eleven_turbo_v2_5", # Turbo model for lowest latency 
        ),
        llm=openai.LLM(model="gpt-4o-mini")
    )
    
    # Inject Caller ID into context if needed
    if caller_id:
        pass

    # Start the agent using AgentSession
    session = AgentSession()
    
    # Note: Assuming start takes agent, room, participant (based on documentation/usage patterns)
    await session.start(agent, room=ctx.room)

    # Load intro message
    try:
        with open("intro_message.txt", "r", encoding="utf-8") as f:
            intro_text = f.read().strip()
    except FileNotFoundError:
        intro_text = "Namaste! I am ready."

    await session.say(intro_text, allow_interruptions=True)
    
    # Keep the agent entrypoint running until the session shuts down
    shutdown_event = asyncio.Event()
    
    @session.on("shutdown")
    def on_shutdown():
        shutdown_event.set()
    
    await shutdown_event.wait()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
