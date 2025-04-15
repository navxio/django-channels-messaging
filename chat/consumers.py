# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
import structlog

logger = structlog.get_logger(__name__)


class VisitorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("VisitorConsumer.connect: Connection attempt started")
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.conversation_group_name = f"chat_{self.conversation_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.conversation_group_name, self.channel_name
        )
        logger.info(
            f"WebSocket connection established for conversation: {self.conversation_id}"
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.conversation_group_name, self.channel_name
        )
        logger.info(
            f"WebSocket connection closed for conversation: {self.conversation_id}, code: {close_code}"
        )

    async def receive_json(self, content, **kwargs):
        """
        Handles incoming JSON messages.
        Expects:
        {
            "type": "chat.message" | "typing" | "identify" | ...
            "content": { ... }
        }
        """
        msg_type = content.get("type")
        msg_content = content.get("content", {})

        logger.debug(f"Received message: {msg_type} with content: {msg_content}")

        if msg_type == "chat.message":
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    "type": "chat_message",
                    "sender": "visitor",
                    "message": msg_content.get("message", ""),
                },
            )

        elif msg_type == "typing":
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {"type": "typing_event", "sender": "visitor"},
            )

        else:
            logger.warning(f"Unknown message type received: {msg_type}")

    # Handlers for group messages
    async def chat_message(self, event):
        await self.send_json(
            {
                "type": "chat.message",
                "sender": event["sender"],
                "message": event["message"],
            }
        )

    async def typing_event(self, event):
        await self.send_json({"type": "typing", "sender": event["sender"]})


class AgentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logger.debug("VisitorConsumer.connect: Connection attempt started")
        self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
        self.conversation_group_name = f"chat_{self.conversation_id}"

        # Join room group
        await self.channel_layer.group_add(
            self.conversation_group_name, self.channel_name
        )
        logger.info(
            f"WebSocket connection established for conversation: {self.conversation_id}"
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.conversation_group_name, self.channel_name
        )
        logger.info(
            f"WebSocket connection closed for conversation: {self.conversation_id}, code: {close_code}"
        )

    async def receive_json(self, content, **kwargs):
        """
        Handles incoming JSON messages.
        Expects:
        {
            "type": "chat.message" | "typing" | "identify" | ...
            "content": { ... }
        }
        """
        msg_type = content.get("type")
        msg_content = content.get("content", {})

        logger.debug(f"Received message: {msg_type} with content: {msg_content}")

        if msg_type == "chat.message":
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {
                    "type": "chat_message",
                    "sender": "visitor",
                    "message": msg_content.get("message", ""),
                },
            )

        elif msg_type == "typing":
            await self.channel_layer.group_send(
                self.conversation_group_name,
                {"type": "typing_event", "sender": "agent"},
            )
        else:
            logger.warning(f"Unknown message type received: {msg_type}")

    # Handlers for group messages
    async def chat_message(self, event):
        await self.send_json(
            {
                "type": "chat.message",
                "sender": event["sender"],
                "message": event["message"],
            }
        )

    async def typing_event(self, event):
        await self.send_json({"type": "typing", "sender": event["sender"]})
