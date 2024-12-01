import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    PROVIDER = os.getenv("PROVIDER", "local")
    LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "./models/7B/ggml-model.gguf")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
