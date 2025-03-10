import asyncio
import websockets
import json

async def start_service(image_name):
    """start new service from image name"""
    async with websockets.connect("ws://127.0.0.1:3000") as websocket:
        request = {"action": "start", "image_name":image_name}
        await websocket.send(json.dumps(request))

        # Receive and print response
        async for message in websocket:
            print("Container Output:", message)


async def send_to_container(container_id, command):
    async with websockets.connect("ws://127.0.0.1:3000") as websocket:
        # Send command to container
        request = {"action": "send", "id": container_id, "input": command}
        await websocket.send(json.dumps(request))

        # Receive and print response
        async for message in websocket:
            print("Container Output:", message)

image_name = "ebukaamadiobi/knn-model"
asyncio.run(start_service(image_name))