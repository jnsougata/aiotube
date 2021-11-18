import concurrent.futures


class _Thread:

    def __init__(self):
        pass


    @classmethod
    def run(cls, function, args: list) -> list:
        num = len(args) if len(args) > 0 else 1
        if args:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num) as exec:
                return list(exec.map(function, args))

        
