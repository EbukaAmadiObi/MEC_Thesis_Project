"""Test for WebSocket based MEC server - most suitable so far"""
import json
import docker
import asyncio
import websockets

import websockets.exceptions

# init docker client
client = docker.from_env()

# dict to store connected clients
active_clients = {}

async def handle_clients(websocket):
    """Handle incoming websocket connections"""
    global active_clients
    try:
        async for message in websocket:
            data = json.loads(message)
            action = data.get("action")

            if action == "start":   # client wants to start a new service
                image_name = data["image_name"]   #TODO: client should send name of model to be used that converts to an image name server-side
                asyncio.create_task(start_service(websocket, image_name))

            elif action == "send":  # client wants to send data to service within container
                container_id = data["id"]   # TODO: Container to send commands to should be determined server side from active clients dict
                command = data["input"]
                asyncio.create_task(send_command(websocket, container_id, command))

    except websockets.exceptions.ConnectionClosed:  # TODO: This doesn't work, and disconnecting a client should delete the container too
        print("Clients disconnected")

async def start_service(websocket, image_name):
    """start a container from given image name and stream data to it in real-time"""

    try:
        container = client.containers.run(image=image_name, detach=True)    # TODO: manage cpu resources and priority and stuff
        container_id = container.id

        # store active session
        active_clients[container_id] = websocket

        print(f"Client at {websocket.remote_address} started container {container_id} running image {image_name}")
        print(active_clients)

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
        
        # Create an exec instance with proper stdin/stdout setup
        exec_id = container.client.api.exec_create(
            container_id,
            command,
            stdin=True,
            tty=True
        )
        
        # Start the exec instance with a socket
        socket = container.client.api.exec_start(
            exec_id['Id'],
            socket=True,
            tty=True
        )
        
        print(f"Client at {websocket.remote_address} executed command {command} in container {container_id}")
        print(active_clients)

        # Send the command to the container's stdin
        socket._sock.sendall(command.encode() + b'\n')
        
        # Stream the output
        for line in socket:
            await websocket.send(line.decode("utf-8"))
            
    except Exception as e:
        await websocket.send(json.dumps({"error": str(e)}))

async def main():
    """start websocket server"""
    ip = "localhost"
    port = 3000
    async with websockets.serve(handle_clients,ip, port):
        print(f"WebSocket server running on {ip}:{port}")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())