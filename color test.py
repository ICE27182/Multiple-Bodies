

def color(r, g, b):
    return f"\033[38;2;{r};{g};{b}m█\033[0m"

for c in range(512):
    if c < 256:
        print(color(0, c//2, c), end="")
    else:
        print(color(c-256, c//2, 511-c), end="")
print("")