def crash_me(s: str) -> None:
    if len(s) > 0 and s[0] == 'b':
        if len(s) > 1 and s[1] == 'a':
            if len(s) > 2 and s[3] == 'd':
                if len(s) > 3 and s[3] == '!':
                    raise Exception()