import gradio as gr
import websockets

# WebSocket chat function (fully asynchronous)
async def websocket_chat(message):
    uri = "ws://localhost:5000/ws"
    async with websockets.connect(uri) as websocket:
        await websocket.send(message)
        response = await websocket.recv()
        return response

# Chat function (async version)
async def chat(message, history):
    response = await websocket_chat(message)
    return response

# Launch Gradio Chat Interface
gr.ChatInterface(
    chat,
    chatbot=gr.Chatbot(height=300),
    textbox=gr.Textbox(placeholder="Ask me questions about your script...", container=False, scale=7),
    title="Chatbot",
    description="Ask Yes Man any question",
    theme="soft",
    examples=["What is supervised learning?", "What is deep learning?", "What is a linear regression?"],
    cache_examples=True,
    retry_btn=None,
    undo_btn="Delete Previous",
    clear_btn="Clear",
).launch()
