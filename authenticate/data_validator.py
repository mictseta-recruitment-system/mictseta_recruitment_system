import re
from datetime import datetime

def validate_email(value):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, value):
        return False
    return True




class ValidateIdNumber:

    def __init__(self, idnumber):
        self.idnumber = idnumber


    def dateTryParse(self, date):
        result = True

        formatStr = '%m/%d/%Y'
        try:
            datetime.strptime(date, formatStr)
        except:
            result = False
        
        return result

    def get_birthdate(self):
        date = False
        try:
            year = self.idnumber[0:2]
            month = self.idnumber[2:4]
            day = self.idnumber[4:6]

            if int(year[0]) == 0:
                date = f'{month}/{day}/20{year}'
            else:
                date = f"{month}/{day}/19{year}"

            return date
        except:
            return date

    def get_age(self):
        age = False
        try:
            year = self.get_birthdate()
            year = int(year.split('/')[-1])
            now = datetime.now()
            age = now.year - year
            return age
        except Exception as e:
            return e

    def get_gender(self):
        gender = False
        digit = int(self.idnumber[6])
        if digit >0 and digit < 5:
            gender = 'female'
        elif digit > 4 and digit < 10:
            gender = 'male'
        else:
            gender = False
        return gender

    def isValidNumberWith13Digits(self):
        return len(self.idnumber) == 13 and self.idnumber.isdigit()
        
    def isOdd(self,number):
        return number % 2 != 0

    def validateSAID(self):
        result = False

        if (self.isValidNumberWith13Digits() and self.get_birthdate() ):
            sum = 0
            for idx, char in enumerate(reversed(self.idnumber)):
                digit = int(char)

                if self.isOdd(idx):
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




#to run and test the script
# def main(idnumber):
#     validate = ValidateIdNumber(idnumber)
#     is_valid = validate.validateSAID()
#     birthdate= validate.get_birthdate()
#     age = validate.get_age()
#     gender = validate.get_gender()
#     print("is valid: ", is_valid)
#     print("birthdate: ", birthdate)
#     print('age : ', age)
#     print("gender: ", gender)


# if __name__ == '__main__':
#     idnumber = ''
#     main(idnumber)
