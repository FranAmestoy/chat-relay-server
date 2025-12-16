import asyncio
import websockets
import os

# Store all connected clients (your mods)
clients = set()

async def handler(websocket):
    clients.add(websocket)
    print(f"Client connected. Total clients: {len(clients)}")
    
    try:
        async for message in websocket:
            # Broadcast this message to ALL other clients
            disconnected = set()
            for client in clients:
                if client != websocket:  # Don't echo back to sender
                    try:
                        await client.send(message)
                    except:
                        disconnected.add(client)
            
            # Clean up disconnected clients
            clients.difference_update(disconnected)
                        
    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        clients.discard(websocket)
        print(f"Client disconnected. Total clients: {len(clients)}")

async def main():
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting relay server on port {port}")
    
    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())
