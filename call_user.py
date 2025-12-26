import asyncio
import os
import argparse
from dotenv import load_dotenv
from livekit import api

load_dotenv()

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")
SIP_TRUNK_ID = os.getenv("SIP_TRUNK_ID")

async def make_call(phone_number, room_name):
    if not all([LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET, SIP_TRUNK_ID]):
        print("Error: Missing configuration in .env. Please check LIVEKIT_URL, API_KEY, API_SECRET, and SIP_TRUNK_ID.")
        return

    lkapi = api.LiveKitAPI(LIVEKIT_URL, LIVEKIT_API_KEY, LIVEKIT_API_SECRET)
    
    print(f"Initiating call to {phone_number} in room {room_name}...")
    
    try:
        # Create a SIP participant to dial out
        # Note: syntax depends on exact SDK version, aiming for standard `create_sip_participant`
        # If specific method is missing, we might need to use raw request or updated SDK method.
        # As of recent SDKs, it might be under `pstn` or directly on `room_service` or via `sip` service.
        
        # Checking for SIP service or using CreateSIPParticipantRequest if available
        # Simplifying to try the high-level client first if available, else standard room creation + dialout via Trunk?
        # Actually, standard SIP dispatch in LiveKit usually requires creating a specific SIP participant.
        
        # For this example, we will assume the room exists or will be created by the agent connecting.
        # But for an outbound call, we usually need the room to rely on.
        
        await lkapi.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                sip_trunk_id=SIP_TRUNK_ID,
                sip_call_to=phone_number,
                room_name=room_name,
                participant_identity=f"sip_{phone_number}",
                participant_name="Mobile User"
            )
        )
        print("Call initiated successfully!")
        
    except Exception as e:
        print(f"Failed to initiate call: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Make an outbound SIP call using LiveKit.")
    parser.add_argument("phone_number", type=str, help="The phone number to call (E.164 format, e.g. +15550000000)")
    parser.add_argument("--room", type=str, default="outbound-room", help="The room name to connect the call to")
    
    args = parser.parse_args()
    
    asyncio.run(make_call(args.phone_number, args.room))
