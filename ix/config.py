import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    PROVIDER = os.getenv("PROVIDER", "openai")
    LLAMA_MODEL_PATH = os.getenv("LLAMA_MODEL_PATH", "./models/7B/ggml-model.gguf")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
