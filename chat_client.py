# chat_client.py

import asyncio
import websockets
import json
import sys

# Constants
BASE_WS_URL = "ws://localhost:8000/ws/chat"
CONVERSATION_ID = "test_conv_id"  # Hardcoded conversation ID


def make_payload(event_type, content=None):
    return json.dumps({"type": event_type, "content": content or ""})


async def chat_loop(role: str):
    ws_url = f"{BASE_WS_URL}/{role}/{CONVERSATION_ID}/"
    async with websockets.connect(ws_url) as ws:
        print(f"[{role.upper()}] connected to {ws_url}")

        async def send_loop():
            while True:
                msg = await asyncio.get_event_loop().run_in_executor(
                    None, sys.stdin.readline
                )
                msg = msg.strip()
                if msg:
                    await ws.send(make_payload("chat.message", {"message": msg}))

        async def receive_loop():
            async for message in ws:
                data = json.loads(message)
                print(f"[RECEIVED] {data}")

        await asyncio.gather(send_loop(), receive_loop())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Python WebSocket Chat Client")
    parser.add_argument(
        "--role", choices=["visitor", "agent"], required=True, help="Role to connect as"
    )
    args = parser.parse_args()

    asyncio.run(chat_loop(args.role))
