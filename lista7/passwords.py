import random
import string
from logger import log
import logging

@log(logging.INFO)
class PasswordGenerator:
    def __init__(self, length, charset=(string.ascii_letters + string.digits), count=10):
        self.length = length
        self.charset = charset
        self.count = count
        self.generated = 0      # counter

    def __iter__(self):
        return self

    def __next__(self):
        if self.generated >= self.count:
            raise StopIteration
        password = ''.join(random.choices(self.charset, k=self.length))
        self.generated += 1
        return password


if __name__ == '__main__':

    print("next test: \n")
    gen = PasswordGenerator(length=20, count=3)
    print(next(gen))  
    print(next(gen))  
    print(next(gen))  
    # print(next(gen)) # raises an error because generated > count

    print("\n\nloop & custom charset test: \n")
    for password in PasswordGenerator(length=8, charset="abc16!", count=4):
        print(password)

