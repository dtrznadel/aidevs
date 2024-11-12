#!/bin/bash
# Wait for Ollama to be ready
sleep 15

# Pull models
docker exec ai ollama pull gemma:2b
docker exec ai ollama pull llama2:3.2b

# Verify models are downloaded
docker exec ai ollama list