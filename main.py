import asyncio
from dotenv import load_dotenv
from livekit.agents import AgentSession, Agent, AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.plugins import openai, silero

load_dotenv()

async def entrypoint(ctx: JobContext):
    # Connect to the room, audio only
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    # Create the “Agent” — this encapsulates the LLM logic / instructions
    agent = Agent(
        instructions=(
            "You are a voice assistant created by LiveKit. "
            "You interface with users via voice. Use short, clear responses, "
            "and avoid hard-to-pronounce punctuation."
        )
    )

    # Create a session with your audio / speech plugins
    session = AgentSession(
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(),
        tts=openai.TTS(),
    )

    # Start the session in the room, with the agent
    await session.start(room=ctx.room, agent=agent)

    # After starting, you can generate a voice reply
    await session.generate_reply(instructions="Hey, how can I help you today?")

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
