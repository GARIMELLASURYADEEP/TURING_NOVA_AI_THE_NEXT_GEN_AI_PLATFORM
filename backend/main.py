# backend/main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure generated_sites exists
os.makedirs("generated_sites", exist_ok=True)

@app.post("/api/save-artifact")
async def save_artifact(request: Request):
    data = await request.json()
    filename = data.get("filename", "untitled.html")
    content = data.get("content", "")
    
    # Sanitize filename
    filename = "".join(x for x in filename if x.isalnum() or x in "._-")
    
    path = os.path.join("generated_sites", filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return {"status": "success", "path": path}

# Serve the generated sites for preview if needed
app.mount("/previews", StaticFiles(directory="generated_sites"), name="previews")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
