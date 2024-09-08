import multiprocessing as mp
from typing import Any

def single(func, *args):
    try:
        res = func(*args)
        return (res, '')
    except Exception as ex:
        return ('', ex)

class run_controller():

    def __init__(self, func, args,) -> None:
        self.func = func
        self.args = args
        self.exceptions = list()

    def run(self):
        results = list()
        exceptions = list()
        for arg in self.args:
            try:
                results.append(self.func(*arg))
            except Exception as ex:
                exceptions.append((ex, arg))
        self.exceptions = exceptions
        return results
    
    def mp_run(self, process):
        results = list()
        exceptions = list()
        args = self.args_conv()
        pool = mp.Pool(process)
        output = pool.starmap(single, args)
        print(output)
        for x in output:
            print(x)
            if x[1] == '':
                results.append(x[0])
            else:
                exceptions.append(x[1])
        self.exceptions = exceptions
        return results

    def args_conv(self):
        new_args = list()
        for x in self.args:
            new_args.append((self.func, *x))
        return new_args

    def __call__(self, mp=False):
        if mp is False:  
            return self.run()
        else:
            return self.mp_run(mp)

