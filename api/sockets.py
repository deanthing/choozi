from .main import app


@app.sio.event
def connect(sid, environ):
    print(f"{sid } is connected.")

@app.sio.on('roundStarted')
async def handle_join(id: int):
    await print("round starteed", id)
    # await app.sio.emit('connected', 'User has joined')
