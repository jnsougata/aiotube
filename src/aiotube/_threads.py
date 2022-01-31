import concurrent.futures


class _Thread:

    def __init__(self):
        pass

    @staticmethod
    def run(function, args: list) -> list:
        num = len(args) if len(args) > 0 else 1
        if args:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num) as exe:
                return list(exe.map(function, args))
