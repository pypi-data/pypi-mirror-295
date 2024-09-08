persian_numbers = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹',
                    '۰': '۰', '۱': '۱', '۲': '۲', '۳': '۳', '۴': '۴', '۵': '۵', '۶': '۶', '۷': '۷', '۸': '۸', '۹': '۹',
                   '-': '-', ':': ':', '.': '.', ' ': ' '}
english_numbers = {'۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4', '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
                    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
                   '-': '-', ':': ':', '.': '.', ' ': ' '}


def english_to_persian(arg):
    
    result = ''
    
    try:
        for item in str(arg):
            result += persian_numbers[item]
        return result
    except:
        raise ValueError('Just can Entre Date or Datetime with Persian or English Language.You Can use "- : ." for Seperate your datetime.')


def persian_to_english(arg):

    result = ''
    
    try:
        for item in str(arg):
            result += english_numbers[item]
        return result
    except:
        raise ValueError('Just can Entre Date or Datetime with Persian or English Language.You Can use "- : ." for Seperate your datetime.')




