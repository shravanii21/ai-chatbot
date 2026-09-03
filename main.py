import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# Configure the Gemini client — key is read from the environment, never hardcoded
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

client = genai.Client(api_key=GEMINI_API_KEY)

# Resolve paths relative to this file so they work from any working directory
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app = FastAPI(title="AI Chatbot", description="A simple chatbot powered by Gemini API")


# --- Request / Response models ---

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


# --- API Routes ---

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Send a message and receive an AI-generated reply via the Interactions API."""
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    try:
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=user_message,
        )
        reply = interaction.output_text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

    return ChatResponse(reply=reply)


@app.get("/health")
async def health():
    """Health check endpoint used by Render."""
    return {"status": "ok"}


@app.get("/")
async def root():
    """Serve the main chat UI."""
    return FileResponse(str(STATIC_DIR / "index.html"))


# --- Serve static assets (CSS, JS, images) ---
# Mounted after API routes so /chat and /health are not shadowed
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# --- Entry point ---
if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
