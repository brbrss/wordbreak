
def print_progress(k, n):
    a = n//100
    if k % a == 0:
        print(k, '/', n)
