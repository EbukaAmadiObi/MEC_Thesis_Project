from fastapi import FastAPI, HTTPException
import docker

app = FastAPI()
client = docker.from_env()

@app.post("/create-container/")
def create_container(image: str, name: str):
    try:
        container = client.containers.run(image, name=name, detach=True)
        return {"message": "Container started", "id" : container.id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.post("/list-containers/")
def list_containers():
    containers = client.containers.list(all=True)
    return [{"id": c.id, "name": c.name, "status":c.status} for c in containers]

@app.post("/stop-container/")
def stop_container(container_id: str):
    try:
        container = client.containers.get(container_id)
        container.stop()
        return {"message": "Container stopped"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))