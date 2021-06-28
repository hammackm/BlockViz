import string

def number_input(number) -> int:
    '''
    Number input can be either a str or an int. Removes all non-integer characters from the input
    '''

    num_str = str(number)

    result_str = ''
    for char in num_str:
        if char.isnumeric():
            result_str += char
    
    return int(result_str)

def hash_input(hash: str) -> str:

    hash_str = hash.lower()

    result_str = ''
    for char in hash_str:
        if char in string.hexdigits:
            result_str += char

    return result_str