import re

def validate_email(value):
    email_regex = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(email_regex, value):
        return False
    return True




class ValidateIdNumber:

    def __init__(self, idnumber):
        self.idnumber = idnumber


    def get_birthdate(self):
        idnumber = self.idnumber

        #logic to get birthdate from id number goes here
        #use idnumber varaible will contain the idnumber so use that

        #return the birthdate in this format as a string: 22-may-2024
        pass
        # Remove the pass keyword after adding your logic


    def get_age(self):
        idnumber = self.idnumber
        #logic to get age from id number goes here
        #use idnumber varaible will contain the idnumber so use that
        #return the age as an integer 
        #dont forget to removee the pass keyword
        pass

    def get_gender(self):
        idnumber = self.idnumber
        #logic to get gender from id number goes here
        #use idnumber varaible will contain the idnumber so use that
        #return the gender as a string in this fomart : 'male', 'female' 
        #dont forget to removee the pass keyword
        pass


#to run and test the script
def main(idnumber):
    validate = ValidateIdNumber(idnumber)

    birthdate= validate.get_birthdate()
    age = validate.get_age()
    gender = validate.get_gender()

    #now you can print any of these variables to test and see if it works
    #when you done delete this main function before you push
    
    #example print the id number before processing 
    #if u run this script u will get `id_number goes here as a string`
    print(idnumber)


if __name__ == '__main__':
    idnumber = 'id_number goes here as a string'
    main(idnumber)
