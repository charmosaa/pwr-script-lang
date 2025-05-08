from functools import lru_cache
import time
from logger import log
import logging

@log(logging.INFO)
def make_generator_mem(f):
    cached_f = lru_cache(maxsize=None)(f)
    return make_generator(cached_f)

@log(logging.DEBUG)
def make_generator(f):
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1

    return generator()

def fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a


def fibRec(n):
    if n <= 2:
        return 1
    return fibRec(n-1) + fibRec(n-2)


@lru_cache(maxsize=None)
def fibRecCache(n):
    if n <= 2:
        return 1
    return fibRecCache(n-1) + fibRecCache(n-2)

if __name__ == '__main__':

    # fibonacci test
    print('Fibonacci sequence: ')
    
    fib_gen = make_generator(fibRec)
    for _ in range(30):
        print(next(fib_gen), end=' ')  


    # # lamba test
    # print('\n\nLamba sequence tests: ')

    # print('\nGeometrical sequence tests: ')
    # # geometrical sequence starting from 2 with ratio = 5
    # geo_gen = make_generator(lambda n: 2 * 5 ** (n-1)) 
    # print([next(geo_gen) for _ in range(5)]) 

    # print('\nArythmetical sequence tests: ')
    # # arythmetical sequence starting from 7 with step = 4
    # arth_gen = make_generator(lambda n: 7 + (n-1) * 4) 
    # print([next(arth_gen) for _ in range(5)]) 

    # cache test

    print('\nMem test fibonacci: ')
    
    # start = time.time()
    fib_gen = make_generator_mem(fibRecCache)
    for _ in range(30):
        print(next(fib_gen), end=' ')
    # print(f'\ntime: {time.time() - start}\n')


