import concurrent.futures


class _HyperThread:

    def __init__(self):
        pass


    @classmethod
    def run(cls, function, args: list) -> list:
        """
        Applicable for single-func 1-arg each thread
        :param function: the single-agred parent func to be executed
        :param args: list of arg
        :return: whole list of the values returned by the parent func in each thread
        """

        num = len(args) if len(args) > 0 else 1
        if len(args) > 0:
            with concurrent.futures.ThreadPoolExecutor(max_workers=num) as exec:
                res = list(exec.map(function, args))
            return res

        
