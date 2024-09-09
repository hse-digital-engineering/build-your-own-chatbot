from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from contextlib import asynccontextmanager
import traceback

from src.bot import CustomChatBot

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Create instance of custom chatbot.")
    app.state.chatbot = CustomChatBot()
    try:
        yield
    finally:
        logger.info("Delete instance of custom chatbot.")
        del app.state.chatbot


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info('Client has connected.')

    try:
        while True:
            input_data = await websocket.receive_text()
            logger.info(f"Received input: {input_data}")

            # Handle chatbot's response using ainvoke method
            try:
                chain_result = await app.state.chatbot.ainvoke(input_data)
                await websocket.send_text(chain_result)
                logger.info(f"Sent response: {chain_result}")

            except Exception as e:
                logger.error(f"Error processing chatbot response: {str(e)}")
                await websocket.send_text(f"Error: {str(e)}")
                break

    except WebSocketDisconnect as e:
        logger.info(f"WebSocket disconnected with code: {e.code}, reason: {e.reason}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        logger.info('Client disconnected.')



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=5000, reload=True, log_level="debug")