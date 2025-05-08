from functools import reduce

def acronym(words):
    return ''.join(map(lambda word: word[0].upper(), words))

def median(numbers):
    x = sorted(numbers)
    n = len(x)
    return (x[(n-1)//2] + x[n//2]) / 2

def pierwiastek(x, epsilon):
    if x < 0:
        raise ValueError("No square root for negative numbers")
     
    def iterate(y):
        return y if abs(y*y - x) < epsilon else iterate(0.5 * (y + x / y))
    return iterate(x)   

def make_alpha_dict(text):
    words = text.split()
    letters = filter(str.isalpha, ''.join(words))
    return dict(
        map(
            lambda ch: (ch, list(filter(lambda word: ch in word, words))),
            letters
        )
    )

def flatten(seq):
    return reduce(
        lambda acc, x: acc + flatten(x) if isinstance(x, (list, tuple)) else acc + [x],
        seq,
        []
    )

def forall(pred, iterable):
    return all(map(pred, iterable))

def exists(pred, iterable):
    return any(map(pred, iterable))

def atleast(n, pred, iterable):
    return sum(map(lambda x: pred(x), iterable)) >= n

def atmost(n, pred, iterable):
    return sum(map(lambda x: pred(x), iterable)) <= n


if __name__ == '__main__':
    # print(median([1,1,19,2,3,4,4,5,1]))
    # print(acronym(["Zakład", "Ubezpieczeń", "Społecznych"]))
    # print(pierwiastek(10, 0.1))
    # print(make_alpha_dict("on i ona ida"))
    # print(flatten([1, [2, (3, 4)], [[5], 6], 7]))
    
    is_even = lambda x: x % 2 == 0
    nums = [2, 4, 6, 1]

    print(forall(is_even, nums))        
    print(exists(is_even, [1, 3, 5])) 
    print(atleast(2, is_even, [1, 5, 4]))
    print(atmost(1, is_even, [1, 2, 3,4])) 




