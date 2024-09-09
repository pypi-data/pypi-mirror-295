import os

class TreeGear:
    
    async def __call__(self, scope, receive, send) -> None:
        if scope['type'] == 'http':
            await send({
                "type": "http.response.start",
                "status": 200,
                "headers": [[b"content-type", b"text/plain"]]
                })
            await send({
                "type": "http.response.body",
                "body": self.write_message().encode()
                })
        elif scope['type'] == 'websocket':
            pass
        elif scope['type'] == 'lifespan':
            while True:
                message = await receive()
                if message['type'] == 'lifespan.startup':
                    # TreeGear lifespan startup processing.
                    await self.__lifespan_startup__()
                    ... # Do some startup here!
                    await send({'type': 'lifespan.startup.complete'})
                elif message['type'] == 'lifespan.shutdown':
                    # TreeGear lifespan shutdown processing.
                    await self.__lifespan_shutdown__()
                    ... # Do some shutdown here!
                    await send({'type': 'lifespan.shutdown.complete'})
                    return

    def write_message(self, message: str = 'OK and hello from TreeGear!') -> bytes:
        return os.environ.get('TRGR_MESSAGE', message)
    

if __name__ == '__main__':
    print('If you want just run the package for test,',
          'then you should run this with command e.g.:',
          '"python -m uvicorn treegear:TreeGear".',
          'else better if you add a python file (e.g. "app.py")',
          'with simple text inside:',
          '"\nfrom treegear import TreeGear\n',
          'trgr = TreeGear()\n',
          'if __name__ == \'__main__\':',
          '    quit(0)\n"',
          'and run it with command: "python -m uvicorn app:trgr"\n',
          'But your command also works fine,',
          'please pay your attention log-messages below.', sep='\n')
    import uvicorn
    uvicorn.run(TreeGear())
    