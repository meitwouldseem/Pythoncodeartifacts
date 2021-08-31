mem = {}

def memorize(func):

    def inner(*arg):
        if arg not in mem:
            mem[arg] = func(*arg)
        return mem[arg]

    return inner
    
@memorize
def ack(x, y):
    if x == 0:
        return y + 1
    
    elif y == 0:
        return ack(x-1,1)
    
    else:
        return ack(x-1, ack(x, y-1))

print(ack(2,2))
