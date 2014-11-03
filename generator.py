
def generator():
    with open('test.js', 'r') as f:
        within = False
        another = False
        info = ''

        for line in f:
            line = line.strip()

            if another:
                info += line + '\n'
                block(info)
                info = ''
                another = False

            if line == '/**':
                info += line + '\n'
                within = True

            elif line == '*/':
                info += line + '\n'
                within = False
                another = True

            elif within:
                info += line + '\n'




def block(info):
    print(info)


if __name__ == '__main__':
    print('Generator')
    generator()
