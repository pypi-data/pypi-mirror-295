def validation_and_cleaning(arg):
    
    english_numbers = '0123456789'
    persian_numbers = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9'}


    def cleaner(arg):
        """This Func just is for Convert English Numbers to Persian Numbers"""

        result = ''
        for item in arg:
            if item in english_numbers:
                result += item
            elif item in persian_numbers.keys():
                for key, value in persian_numbers.items():
                    if item == key:
                        result += value
            else:
                raise ValueError('[Mobile Phone Number] must be english or persian numbers.')
        return result



    if type(arg) == int:
        arg_str = str(arg)
        if len(arg_str) == 10:
            if arg_str[0] == '9':
                return arg
            else:
                raise ValueError('when entered [Mobile Phone Number] 10 digits pattern, it should start with [9].')
        else:
            raise ValueError('when entered [int] type [Mobile Phone Number] must be Entered [10] digits for its.')
        
    elif type(arg) == str:

        if len(arg) == 11:
            if arg[0:2] == '09':
                return cleaner(arg)[1:]
            else:
                raise ValueError('when entered [Mobile Phone Number] 11 digits pattern, it should start with [09]')

        elif len(arg) == 10:
            if arg[0] == '9':
                return cleaner(arg)
            else:
                raise ValueError('when entered [Mobile Phone Number] 10 digits pattern, it should start with [9]')

        else:
            raise ValueError('When Entered [str] type [Mobile Phone Number] must be Entered [10] or [11] digits for its.')

    else:
        raise ValueError('[Modile Phone Number] must be [int] or [str] Type.')


