#!/bin/bash

echo "🧠 Pulling model llama3..."
ollama pull llama3

echo "🚀 Starting Ollama server on 0.0.0.0:11434..."
ollama serve --host 0.0.0.0
