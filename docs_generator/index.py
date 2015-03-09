def array(s, subs):
    result = []

    for sub in subs:
        result.extend(string(s, sub))

    result.sort()
    return result


def string(s, sub):
    index = 0
    result = []

    while index < len(s):
        index = s.find(sub, index)
        if index == -1:
            break

        result.append(index)
        index += len(sub)

    result.sort()
    return result


def split(s, index):
    result = []
    start = 0

    for end in index:
        sub = s[start:end]

        if len(sub) > 0:
            result.append(sub)

        start = end

    result.append(s[start:])

    return result


def header(s, level):
    header = ''

    for l in range(0, level):
        header += '#'

    return header + ' ' + s
