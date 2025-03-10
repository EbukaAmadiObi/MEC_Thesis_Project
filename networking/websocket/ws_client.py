import asyncio
import websockets
import json

async def send_to_container(container_id, command):
    async with websockets.connect("ws://127.0.0.1:3000") as websocket:
        # Send command to container
        request = {"action": "send", "id": container_id, "input": command}
        await websocket.send(json.dumps(request))

        # Receive and print response
        async for message in websocket:
            print("Container Output:", message)

# Example: Sending "ls" to a running container
container_id = "your-container-id"
command = "ls"
asyncio.run(send_to_container(container_id, command))