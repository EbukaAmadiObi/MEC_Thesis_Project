import json
import docker
import asyncio
import websockets
from typing import Dict

import websockets.exceptions
import websockets.server

# init docker client
client = docker.from_env()

# dict to store connected clients
active_clients = {}

#
async def handle_clients(websocket):
    """Handle incoming websocket connections"""
    global active_clients
    try:
        async for message in websocket:
            data = json.loads(message)  # load json data
            action = data.get("action")     # get desired action from received data

            if action == "start":   # client wants to start service
                container_id = data["id"]   #TODO: client should send name of model to be used that converts to a container id server side
                asyncio.create_task(start_service(websocket, container_id))


            elif action == "send":  # client wants to send data to service within container
                container_id = data["id"]   
                command = data["input"]
                asyncio.create_task(send_command(websocket, container_id, command))
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        # remove client from active sessions
        for container_id in list(active_clients.keys()):
            if active_clients[container_id] == websocket:
                del active_clients[container_id]

async def start_service(websocket, container_id):
    """start a container and attach client to it, stream data in real-time"""
    container = client.containers.get(container_id)

    # store active session
    active_clients[container_id] = websocket

    try:
        for line in container.logs(stream=True, follow=True):
            if container_id in active_clients and active_clients[container_id] == websocket:
                await websocket.send(line.decode("utf-8"))
            else:
                break   # stop sending if client disconnects
    except Exception as e:
        await websocket.send(json.dumps({"error": str(e)}))

async def send_command(websocket, container_id, command):
    """send command to running container"""
    try:
        container = client.containers.get(container_id)
        exec_result = container.exec_run(command, stream=True)

        for line in exec_result.output:
            await websocket.send(line.decode("utf-8"))
    except Exception as e:
        await websocket.send(json.dumps({"error": str(e)}))

async def main():
    """start websocket server"""
    async with websockets.serve(handle_clients, "0.0.0.0", 3000):
        print("WebSocket server running on 0.0.0.0:3000")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())