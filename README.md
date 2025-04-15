### Requirements:
- `python 3.11`
- `uv`/`poetry`
- (Optional)[Taskfile](https://taskfile.dev)

### How the flow works

- Client generates a conversation id and connects to websocket consumer; waits for agent
- in the meantime, this conversation id is stored into cache and added to the pool of available conversation ids
- this client is added to a room of the said conversation id (room is automatically created with group)
- Agent chooses a conversation id from a pool of ids
- Agent joins the same room on connection
- <chat> contains different types of messages - typing, chat etc
