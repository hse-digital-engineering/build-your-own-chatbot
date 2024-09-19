#!/usr/bin/env bash
: "${OLLAMA_LOGS:=/data/logs/ollama.log}"
: "${MODEL_NAME:=sam4096/qwen2tools:1.5b}"

mkdir -p "$(dirname "$OLLAMA_LOGS")"

printf "\nStarting ollama server\n\n"

/bin/bash -c "/bin/ollama serve &> $OLLAMA_LOGS" &

timeout 5 tail -f $OLLAMA_LOGS

printf "\nOLLAMA_MODELS ${OLLAMA_MODELS}\n"
printf "OLLAMA_LOGS   ${OLLAMA_LOGS}\n"

printf "\nollama server is now started\n\n"

printf "\nollama start running now ${MODEL_NAME}\n\n"

/bin/bash -c "/bin/ollama run ${MODEL_NAME} &> $OLLAMA_LOGS"