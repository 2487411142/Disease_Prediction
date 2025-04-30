#!/bin/bash
ollama serve &
OLLAMA_PID=$!

sleep 2
ollama pull gemma3:12b

wait $OLLAMA_PID
