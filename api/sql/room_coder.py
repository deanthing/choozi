
"""decode and encodes room numbers joining"""


def coder(room_number):
    """
    input: 3 digit room number

    takes a 3 digit number and converts each digit to a corresponding letter

    output: array of three chars
    """
    room_number = str(room_number)
    out_lst = []
    for num in room_number:
        out_lst.append(chr(ord('@')+int(num)))

    for i in range(len(out_lst)):
        if out_lst[i] == '@':
            out_lst[i] = 'Y'

    if len(out_lst) < 3:
        for i in range(3-len(out_lst)):
            out_lst.append("Z")

    return out_lst


def decoder(letters):
    """
    converts lettes to numbers
    """

    data = {
        1: 'A',
        2: 'B',
        3: 'C',
        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',
        8: 'H',
        9: 'I',
    }

    out_lst = []
    for letter in letters:
        if letter == 'Y':
            out_lst.append(0)
        else:
            for k, v in data.items():
                if v == letter:
                    out_lst.append(k)

    digits = ""
    for i in out_lst:
        digits += str(i)

    if digits:
        digits = int(digits)
    else:
        return -1
    return digits
