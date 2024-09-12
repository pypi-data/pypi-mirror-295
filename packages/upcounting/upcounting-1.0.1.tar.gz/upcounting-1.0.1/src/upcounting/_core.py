def count_up(start=0, stop=None, step=1):
    ans = start
    while True:
        if stop is None:
            pass
        elif callable(stop):
            if stop(ans):
                break
        else:
            if ans >= stop:
                break
        yield ans
        ans += step
