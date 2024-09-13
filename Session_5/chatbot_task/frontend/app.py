import gradio as gr
import websockets
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# WebSocket chat function (fully asynchronous)
async def websocket_chat(message: str) -> str:
    uri = "ws://backend:5001/ws"
    try:
        async with websockets.connect(uri) as websocket:
            logger.info(f"Sending message: {message}")
            await websocket.send(message)
            response = await websocket.recv()
            return response
    except Exception as e:
        logger.error(f"Error during WebSocket communication: {str(e)}")
        return f"Error: {str(e)}"

# Chat function (async version)
async def chat(message: str, history= None) -> str:
    if not message.strip():
        return "Please enter a valid question."
    
    return await websocket_chat(message)

# TODO: Customize the Chatbot Interface how you like

# Launch Gradio Chat Interface
gr.ChatInterface(
    fn=chat,
    chatbot=gr.Chatbot(height=400),  # Adjusted height for better usability
    textbox=gr.Textbox(placeholder="Ask me questions about your script...", container=False, scale=7),
    title="Chatbot",
    description="Ask me questions about your lecture.",
    theme="soft",
    examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
    clear_btn="Clear",
).launch(debug=True)
