from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from contextlib import asynccontextmanager
import traceback

from src.bot import CustomChatBot

# Set up logger
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan manager to ensure CustomChatBot is initialized and cleaned up correctly.
    """
    logger.info("Creating instance of custom chatbot.")
    app.state.chatbot = CustomChatBot()
    try:
        yield
    finally:
        logger.info("Cleaning up chatbot instance.")
        del app.state.chatbot

# Create FastAPI app and configure CORS
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to restrict domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint that handles communication with the client.
    """
    await websocket.accept()
    logger.info('Client connected.')

    try:
        while True:
            # Receive and process input from the WebSocket client
            try:
                input_data = await websocket.receive_text()
                logger.info(f"Received input: {input_data}")

                # Invoke chatbot with the received input
                chain_result = await app.state.chatbot.ainvoke(input_data)
                logger.info(f"Sent response: {chain_result}")
                await websocket.send_text(chain_result)

            except WebSocketDisconnect as e:
                logger.info(f"WebSocket disconnected with code: {e.code}, reason: {e.reason}")
                logger.error(traceback.format_exc())
                break

            except Exception as e:
                logger.error(f"Error processing chatbot response: {str(e)}")
                logger.error(traceback.format_exc())
                await websocket.send_text(f"Error: {str(e)}")
                break

    except WebSocketDisconnect as e:
        logger.info(f"Client disconnected with code: {e.code}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        logger.info('Client disconnected.')

if __name__ == "__main__":
    # Run the FastAPI app with uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5001, reload=True, log_level="debug")
