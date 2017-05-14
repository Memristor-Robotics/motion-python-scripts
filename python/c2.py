
def c(x):
    if x < 0:
        x = x + 2**16
    return hex(x)

