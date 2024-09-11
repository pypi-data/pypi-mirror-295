import argparse
from peasyprofiller.profiller import profiller as pprof

def fibonacci(n: int) -> int:
    pprof.start("Fibonacci")

    last_number = 1
    current_number = 1
    for i in range(n - 1):
        new_number = last_number + current_number
        last_number = current_number
        current_number = new_number

    pprof.stop("Fibonacci")
    return current_number



parser = argparse.ArgumentParser()
parser.add_argument("n", help="The fibonacci number you want to calculate", type=int)
parser.add_argument("save", help="The path to save the profilling data", type=str)
args = parser.parse_args()

fibonacci(args.n)
pprof.save_csv(args.save)
