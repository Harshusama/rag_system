from app.config import get_settings


settings = get_settings()

print("Configuration loaded successfully")
print("Chat model:", settings.chat_model)
print("Embedding model:", settings.embedding_model)
print("API key found:", bool(settings.openai_api_key))