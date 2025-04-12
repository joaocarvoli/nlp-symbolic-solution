# Creates symbols and words dictionaries from our portuguese semantic and morphologic dictionary
def dic_reader():
    symbols = dict()
    words = dict()
    with open('../../data/LIWC2015_pt2-sem-pulo-linhas.dic', 'r', encoding="utf-8") as file:
        symbol_read = False
        for line in file:
            line = line.strip()
            if line == '%':
                symbol_read = not symbol_read
                continue
            line = line.replace('\t', ' ')
            line_split = line.split(' ')
            if symbol_read:
                symbols[int(line_split[0])] = ' '.join(line_split[1:])
            else:
                values = line_split[1:]
                key = line_split[0]
                if '*' in values:
                    key = key + '*'
                    values.remove('*')
                values = {int(number) for number in values if number != ''}
                words[key] = values

    return symbols, words