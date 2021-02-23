from app import chat
import asyncio
import websockets

async def bot(websocket, path):
    while True:
        message = await websocket.recv()
        print(f"< {message}")
        response = chat(message)
        await websocket.send(response)
        print(f"> {response}")

if __name__ == '__main__':
    start_server = websockets.serve(bot, "0.0.0.0", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
