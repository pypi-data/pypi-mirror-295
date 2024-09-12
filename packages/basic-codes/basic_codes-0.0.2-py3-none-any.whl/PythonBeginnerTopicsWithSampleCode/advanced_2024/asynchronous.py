import asyncio

async def main():
    task = asyncio.create_task(another_function)
    print('Got Request')
    await another_function()
    print('Hello world')

async def another_function():
    await asyncio.sleep(1)
    print('Another Function')

asyncio.run(main())