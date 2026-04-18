import json
import logging
import os
import time
from datetime import datetime

logger = logging.getLogger("signal_mcp_client")


def get_history(session_dir, session_id, limit):
    messages_dir = session_dir / session_id / "messages"
    if not messages_dir.exists():
        return []
    message_files = sorted(messages_dir.glob("*.json"))
    messages = [json.load(open(file_path)) for file_path in message_files[-limit:]]
    if not messages:
        return []

    # Strip leading tool messages orphaned by the context window slice
    while messages and messages[0]["role"] == "tool":
        messages = messages[1:]

    # Repair dangling tool_use sequences: an assistant message with tool_calls must be
    # immediately followed by a tool result for every call. If results are missing (e.g.
    # the service was restarted mid-turn), drop that assistant message and any partial
    # results so the history stays valid.
    repaired = []
    i = 0
    while i < len(messages):
        msg = messages[i]
        if msg["role"] == "assistant" and msg.get("tool_calls"):
            expected_ids = {tc["id"] for tc in msg["tool_calls"]}
            j = i + 1
            result_map = {}
            while j < len(messages) and messages[j]["role"] == "tool":
                result_map[messages[j].get("tool_call_id")] = messages[j]
                j += 1
            if expected_ids.issubset(result_map.keys()):
                repaired.append(msg)
                repaired.extend(result_map[tc_id] for tc_id in expected_ids)
                i = j
            else:
                missing = expected_ids - result_map.keys()
                logger.warning(f"Dropping incomplete tool_use sequence — missing results for: {missing}")
                i = j  # skip the assistant msg and any partial results
        else:
            repaired.append(msg)
            i += 1

    return repaired


def add_message(session_dir, session_id, message):
    messages_dir = session_dir / session_id / "messages"
    messages_dir.mkdir(parents=True, exist_ok=True)

    base_ts = int(time.time() * 1000)
    file_path = messages_dir / f"{base_ts}.json"
    counter = 1
    while file_path.exists():
        file_path = messages_dir / f"{base_ts}_{counter:03d}.json"
        counter += 1

    with open(file_path, "w") as f:
        json.dump(message, f, indent=2)


def clear_history(session_dir, session_id):
    messages_dir = session_dir / session_id / "messages"
    if messages_dir.exists():
        message_files = sorted(messages_dir.glob("*.json"))
        for file_path in message_files[:-2]:
            os.remove(file_path)


def add_user_message(session_dir, session_id, content):
    timestamp_str = datetime.now().strftime("[%Y.%m.%d %H:%M]")
    message = {"role": "user", "content": [{"type": "text", "text": f"{timestamp_str} {content}"}]}
    add_message(session_dir, session_id, message)
    logger.info(f"user_message: {message['content'][0]['text'][:60]}...")


def add_assistant_message(session_dir, session_id, content, tool_calls=None):
    """Add a simple assistant text message."""
    if content is None:
        logger.info("assistant_message: None")
    else:
        logger.info(f"assistant_message: {content[:60]}...")
    message = {"role": "assistant", "content": content}
    if tool_calls:
        temp_tool_calls = []
        for tool_call in tool_calls:
            temp_tool_calls.append(
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {"name": tool_call.function.name, "arguments": tool_call.function.arguments},
                }
            )
        logger.info(
            f"tool_calls: {', '.join([f'{tool_call.function.name}({tool_call.function.arguments})' for tool_call in tool_calls])}"
        )
        message["tool_calls"] = temp_tool_calls

    if content or tool_calls:
        add_message(session_dir, session_id, message)


def add_tool_response(session_dir, session_id, tool_call_id, name, tool_result_text):
    """Add a tool response message."""
    message = {
        "role": "tool",
        "tool_call_id": tool_call_id,
        "name": name,
        "content": [{"type": "text", "text": tool_result_text}],
    }
    add_message(session_dir, session_id, message)
    logger.info(f"tool_response: {tool_result_text[:60]}...")
