"""
Memory utilities for LLM views module.
"""

from typing import List, Dict, Any
from ...models.db_models import ConversationHistory, ShortTermMemory
from .constants import MAX_DIALOGUES_THRESHOLD, RECENT_MEMORIES_COUNT


def get_recent_dialogues(room_id: str) -> tuple[List[ConversationHistory], int]:
    """
    Get recent dialogues for a room.

    Returns the latest 10 dialogues in chronological order.

    Returns:
        Tuple of (dialogues list, total count)
    """
    all_dialogues = ConversationHistory.objects.filter(room_id=room_id)
    total_dialogues = all_dialogues.count()

    # Get latest 10 dialogues in chronological order
    recent_dialogues = list(all_dialogues.order_by('-created_at')[:MAX_DIALOGUES_THRESHOLD])
    recent_dialogues.reverse()

    return recent_dialogues, total_dialogues


def get_recent_memories(room_id: str, limit: int = RECENT_MEMORIES_COUNT) -> List[ShortTermMemory]:
    """Get recent short-term memories for a room."""
    recent_memories = list(
        ShortTermMemory.objects.filter(room_id=room_id)
        .order_by('-created_at')[:limit]
    )
    recent_memories.reverse()
    return recent_memories


def build_core_memory(
    dialogues: List[ConversationHistory],
    memories: List[ShortTermMemory]
) -> List[Dict[str, Any]]:
    """Build core memory from dialogues and short-term memories."""
    core_memory = []

    # Add dialogues to core memory
    for dialogue in dialogues:
        core_memory.append({
            'type': 'dialogue',
            'character_id': dialogue.character_id,
            'character_name': dialogue.character_name,
            'content': dialogue.content,
            'location': dialogue.current_location,
            'status': dialogue.status,
            'timestamp': dialogue.created_at.isoformat()
        })

    # Add short-term memories to core memory
    for memory in memories:
        core_memory.append({
            'type': 'memory',
            'content': memory.content,
            'timestamp': memory.created_at.isoformat()
        })

    return core_memory
