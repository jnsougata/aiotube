import time
import asyncio
import concurrent.futures


class _HyperThread:

    def __init__(self):
        pass


    @classmethod
    def run(cls, function, args:list):
        num = len(args) if len(args) > 0 else 1
        if len(args) > 0:
            async def _main():
                start = time.time()
                with concurrent.futures.ThreadPoolExecutor(max_workers=num) as executor:
                    loop = asyncio.get_event_loop()
                    futures = [
                        loop.run_in_executor(
                            executor, function, item
                        )
                        for item in args
                    ]
                    data = []
                    for ret in await asyncio.gather(*futures):
                        data.append(ret)
                end = time.time()
                print(f'Executed in {round(end - start, 3)}s.')
                return data

            return asyncio.run(_main())
        
