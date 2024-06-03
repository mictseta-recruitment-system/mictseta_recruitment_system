from datetime import datetime

def dateTryParse(date):
    result = True

    formatStr = '%m/%d/%Y'
    try:
        datetime.strptime(date, formatStr)
    except:
        result = False
    
    return result

def hasValidDate(id):
    year = id[0:2]
    month = id[2:4]
    day = id[4:6]

    date1 = f'{month}/{day}/19{year}'
    date2 = f'{month}/{day}/20{year}'

    return dateTryParse(date1) or dateTryParse(date2)

def isValidNumberWith13Digits(id):
    return len(id) == 13 and id.isdigit()

def isOdd(number):
    return number % 2 != 0

def validateSAID(id):
    result = False

    if (
        isValidNumberWith13Digits(id)
        and
        hasValidDate(id)
    ):
        sum = 0

        for idx, char in enumerate(reversed(id)):
            digit = int(char)

            if isOdd(idx):
                digit = digit * 2

                if digit > 9:
                    subSum = 0

                    while digit > 0:
                        subSum += digit % 10
                        digit = digit // 10

                    digit = subSum
            sum += digit

        result = sum % 10 == 0

    return result

def genControlDigitFor(sid):
    result = ""

    sum = 0

    for idx, char in enumerate(reversed(sid)):
        digit = int(char)

        if not isOdd(idx):
            digit = digit * 2

            if digit > 9:
                subSum = 0

                while digit > 0:
                    subSum += digit % 10
                    digit = digit // 10

                digit = subSum
        sum += digit
    
    result = (10 - sum % 10) % 10

    return result

id = "0207235794089" #Here is my id i used it to validate 
print(f'SAID: {id}')
print(f'The id is valid? {validateSAID(id)}')

sid = id[0:len(id) - 1]
controlDigit = genControlDigitFor(sid)
print(f'Control digit of {sid} is {controlDigit}')
