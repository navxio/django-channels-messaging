from django.core.cache import cache
import structlog

logger = structlog.get_logger(__name__)

AVAILABLE_CONVERSATIONS_KEY = "available_conversations"
MAX_POOL_SIZE = 100  # optional cap


def add_to_available_pool(conversation_id):
    conversations = cache.get(AVAILABLE_CONVERSATIONS_KEY, [])
    if conversation_id not in conversations:
        conversations.append(conversation_id)
        if len(conversations) > MAX_POOL_SIZE:
            conversations = conversations[-MAX_POOL_SIZE:]  # keep only latest
        cache.set(AVAILABLE_CONVERSATIONS_KEY, conversations)
        logger.debug(f"Added to pool: {conversation_id}")


def remove_from_available_pool(conversation_id):
    conversations = cache.get(AVAILABLE_CONVERSATIONS_KEY, [])
    if conversation_id in conversations:
        conversations.remove(conversation_id)
        cache.set(AVAILABLE_CONVERSATIONS_KEY, conversations)
        logger.debug(f"Removed from pool: {conversation_id}")


def get_available_conversations():
    return cache.get(AVAILABLE_CONVERSATIONS_KEY, [])
