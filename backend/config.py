# backend/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

# --- Load .env ---
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
load_dotenv(ROOT_DIR / ".env")

# --- Provider Selection ---
# אפשרויות: "huggingface", "ollama", "google"
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "huggingface").lower()

# --- Hugging Face ---
HUGGINGFACE_API_KEY: str | None = os.getenv("HUGGINGFACE_API_KEY")
HUGGINGFACE_MODEL: str = os.getenv("HUGGINGFACE_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")

# --- Ollama (מודלים מקומיים) ---
OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3")

# --- Google Gemini ---
GOOGLE_API_KEY: str | None = os.getenv("GOOGLE_API_KEY")
GOOGLE_MODEL: str = os.getenv("GOOGLE_MODEL", "gemini-1.5-flash")

# --- Data paths ---
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"
MATCHES_DIR = DATA_DIR / "matches"
REPORTS_DIR = DATA_DIR / "reports"
PROMPTS_DIR = BASE_DIR / "prompts"

for d in [PROCESSED_DIR, MATCHES_DIR, REPORTS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --- Debug log ---
print(f"✅ Loaded config: provider={LLM_PROVIDER}, "
      f"HF={HUGGINGFACE_MODEL}, Ollama={OLLAMA_MODEL}, Google={GOOGLE_MODEL}")
