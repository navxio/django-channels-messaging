# chat_client.py

import asyncio
import websockets
import json
import sys

# Customize this URL as needed
SERVER_URL = "ws://localhost:8000/ws/chat/room_id/"


def make_payload(event_type, content=None):
    return json.dumps({"type": event_type, "content": content or ""})


async def chat_loop(role: str):
    async with websockets.connect(SERVER_URL) as ws:
        print(f"[{role.upper()}] connected to {SERVER_URL}")

        # Identify self
        await ws.send(make_payload("identify", {"role": role}))
        print(f"[{role.upper()}] sent identify")

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
