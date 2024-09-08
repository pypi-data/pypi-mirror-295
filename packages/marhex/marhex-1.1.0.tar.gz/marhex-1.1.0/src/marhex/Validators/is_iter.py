def is_persian_char(arg):
    char_list = ' ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
    result: bool
    if type(arg) == str: 
        for item in arg:
            if item in char_list:
                result = True
            else:
                result = False
                break

        return result
    else:
        raise ValueError('Arg must be String Type')

