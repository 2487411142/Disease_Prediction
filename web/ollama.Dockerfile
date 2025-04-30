FROM ollama/ollama:latest

WORKDIR /app

COPY ollama_start.sh .
RUN ["chmod", "+x", "ollama_start.sh"]

ENTRYPOINT ["./ollama_start.sh"]
