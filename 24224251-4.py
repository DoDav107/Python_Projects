#24224251 David Do
#This program Analyses user demographics to better understand social media usage and returns the four outputs OP1,OP2,OP3,OP4 based on the input file

def read_file(cvsfile):
    """Reads the file and returns each line in the file as a list""" 
    Data_list = []
    try:
        with open(cvsfile,"r") as file: #Opens and reads the file
            for line in file: #Iterates over each line in file
                line_of_data = line.strip().split(',') #Removes whitespaces and splits items from each line into a list  
                Data_list.append(line_of_data) #Adds items as lists in Data_list
    except: 
        return [] #Empty list will return if no data or invalid data is inputed 
    return Data_list

def main(cvsfile, age_range, country):
    """Returns the four outputs OP1,OP2,OP3,OP4"""
    Data = read_file(cvsfile)
    lower,upper = (age_range[0]),(age_range[1]) #Identifies the lower and upper bounds of age range 
    country_insensitive = country.lower() #Makes string case insensitive 
    OP1 = output1(Data,country)
    OP2 = output2(Data,lower,upper)
    OP3 = output3(Data,lower,upper)
    OP4 = output4(Data,lower,upper)
    return OP1,OP2,OP3,OP4
    
    
def output1(Data,country):
    """Returns list of student details [ID and Income]"""
    data_list = []
    country_insensitive = country.lower() 
    for element in Data[1:]:  #Iterates over each line/list to identify certain items             
        country_element = str(element[6].lower()) #Makes string case insensitive
        social_media_time = int(element[3])
        in_debt = str(element[-1].lower()) #Makes string case insensitive
        if country_element == country_insensitive and social_media_time > int(7) and in_debt == "true": #checks if user in each line meets conditions
            data_list.append((str(element[0]), round(float(element[9]),4))) #Adds valid items to list
            data_list.sort #Sorts items in list in ascending order based on ID
    if not data_list:
        print("No student(s) from the country are in debt and spends more than 7 hours on social media")
        return [] #Empty list will return if no data or invalid data is inputed 
    return data_list

def output2(Data,lower,upper):
    """Returrns list of unique countries of users whose age falls within the age range"""
    countries_list = []
    for element in Data[1:]:    #Iterates over each line/list to identify certain items  
        age = int(element[1])
        country_element = str(element[6].lower()) #Makes string case insensitive
        if lower <= age <= upper: #Checks if user age falls within given age range 
            countries_list.append(country_element) #Adds valid items to list
    if not countries_list: 
        print("No users fall within the age range for output2")
        return [] #Empty list will return if no data or invalid data is inputed 
    return sorted(list(set(countries_list))) #Removes any duplicates by turning list into a set then converts back to list and sorts items in list in alphabetical order

def time(Data,lower,upper):
    """Returns a list of the time(s) spent on social media for each user than falls within the age range"""
    time_spent_list = []
    for element in Data[1:]: #Iterates over each line to identify certain items 
        age = int(element[1])
        time = int(element[3])
        if lower <= age <= upper: #Checks if user(s) age falls within given age range 
            time_spent_list.append(time) #Adds user(s) time(s) to list
    return time_spent_list

def average_time_rounded(Data,lower,upper):
    """Calculates average time rounded to four decimal places"""
    average_time_spent_list = []
    time_spent_list = time(Data,lower,upper)
    if len(time_spent_list)==0: #checks if length of list is zero 
        print("Division by zero is not premitted")  
        return 0 #Returns zero if length of list is zero 
    else:
        average_time_spent = sum(time_spent_list)/len(time_spent_list) #Calculates average time 
        average_time_spent_rounded = round(average_time_spent,4)
        average_time_spent_list.append(average_time_spent_rounded) #Adds user(s) average time(s) to list 
    return average_time_spent_list[0]

def income1(Data,lower,upper):
    """Returns a list containing the income(s) of user(s) whose age falls within the age range"""
    income_list = []
    for element in Data[1:]: #Iterates over each line to identify certain items 
         income = int(element[9])
         age = int(element[1])
         if lower <= age <= upper: #Checks if user(s) age falls within given age range 
             income_list.append(income) #Adds the income of each user to list 
    return  income_list       

def average1(Data,lower,upper):
    """Caculates the average income of user(s) whose age falls within the age range"""
    income_list = income1(Data,lower,upper)
    if len(income_list) == 0: #checks if length of list is zero 
        print("Division by zero is not premitted")
        return 0  #Returns zero if length of list is zero 
    else:
        average_income = sum(income_list)/len(income_list) #Calculates average income
    return average_income

def standard_deviation(Data,lower,upper):
    """Calculates Standard deivation"""
    standard_deviation_list = []
    income_list = income1(Data,lower,upper)
    average_income = average1(Data,lower,upper)
    if len(income_list) == 1 or len(income_list) == 0: #Checks if length of income_list is valid for further calcualtion
        print("Division by zero is not premitted or invalid calculation")
        return 0 #Returns zero if length of list is zero or one
    else:
        variance = (sum((x-average_income)**2 for x in income_list))/(len(income_list)-1) #uses loop to iterate over every item in income_list to calculate variance
        standard_deviation = variance**0.5
        standard_deviation_rounded = round(standard_deviation,4) 
        standard_deviation_list.append(standard_deviation_rounded) #Add standard deviation to list
    return  standard_deviation_list[0]

def demographic(Data,lower,upper):
    """Returns a dictionary which tells the average time spent for each demographic"""
    demographics1 = {} #Define dictionaries to store required data
    demographics2 = {}
    demographic3 = {}
    for element in Data[1:]: #Iterates over each line to identify certain items 
        location = str(element[7].lower()) #Makes string case insensitive
        age = int(element[1])
        time = int(element[3])
        if lower <= age <= upper: #Checks if user(s) age falls within given age range
            demographics1[location]=demographics1.get(location, 0) +time #Adds the time spent for each demographic 
            demographics2[location]=demographics2.get(location, 0) +1 #Adds 1 user for each demographic according to each line/list 
    for location in demographics1: 
        demographic3[location] = demographics1[location]/demographics2[location] #Caculates the average time spent for each demographic
    return demographic3

def min_demographic(Data,lower,upper):
    """Finds the demographic within the age group that spent the lowest average time on social media"""
    min_demographic1 = []
    demographics = demographic(Data,lower,upper)
    if not demographics: # case where dictionary is empty/invalid 
        print("dictionary is empty or invalid data in file")
        first_demographic=None #Returns None if demographic doesnt exist
    else:
        min_demographic2 = min(demographics, key=demographics.get) #Determines the demographic with the lowest average time on social media 
        min_demographic1.append(min_demographic2) #Adds demographic to lists
        min_demographic1.sort() #Sorts demographics in alphabetical order
        first_demographic = min_demographic1[0] #Selects the first demographic according to alphabetical order 
    return first_demographic

def output3(Data,lower,upper):
    """Returns list containing average time spent, standard deviation of income and demography"""
    average_time_spent = average_time_rounded(Data,lower,upper)
    Standard_Deviation = standard_deviation(Data,lower,upper)
    first_demographic = min_demographic(Data,lower,upper)
    combine_list = [average_time_spent, Standard_Deviation, first_demographic] #combines values into a list
    return combine_list

def platform(Data,lower,upper):
    """Determines the amount of user(s) in each platform"""
    platform_dictionary = {} #Dictionary containing the total amount of users for each platform 
    for element in Data[1:]: #Iterates over each line/list to identify certain items     
        media = str(element[4].lower()) #Makes string case insensitive 
        age = int(element[1])
        platform_dictionary[media] = platform_dictionary.get(media, 0) +1 #Adds 1 user for each platform every time platform is found in each line
    if not platform_dictionary: #Checks if dictionary is empty/Invalid
        print("Invalid/Insufficient data in file")
        return None
    return platform_dictionary

def max_platform(Data,lower,upper):
    """Determines the platform with the most user(s)"""
    max_platform1 = []
    platform_dictionary = platform(Data,lower,upper)
    if not platform_dictionary: #Checks if dictionary is empty/Invalid
        print("There is no platform with the highest number of users")
        return None 
    else:
        max_platform2 = max(platform_dictionary, key = platform_dictionary.get) #Determines the platform with the most users
        max_platform1.append(max_platform2) #Adds max platform(s) to list
        max_platform1.sort() #Sorts platforms in alphabetical order
    return max_platform1[0] #returns the first platform according to alphabetical order

def income2(Data,lower,upper):
    """Returns a list containing the incomes of users from the platform with the highest users"""
    income_list2 = []
    max_platform1 = max_platform(Data,lower,upper)
    for element in Data[1:]:      #Iterates over each line/list to identify certain items     
        media = str(element[4].lower()) #Makes string case insensitive
        age = int(element[1]) 
        income = int(element[9])
        if media == max_platform1: #checks to see if the platform of the user is the  max platform 
            income_list2.append(income) #Adds user(s) income to list
    if not income_list2:
        print("No income lists exist")
        return [] #Empty list will return if no data or invalid data is inputed 
    return income_list2

def age_of_users(Data,lower,upper):
    """Returns a list containing the ages of users from the platform with the highest users"""
    age_list = []
    max_platform1 = max_platform(Data,lower,upper)
    for element in Data[1:]: #Iterates over each line/list to identify certain items 
        age = int(element[1])
        media = str(element[4].lower()) #Makes string case insensitive
        if  media == max_platform1: #checks to see if the platform of the user matches the max platform 
             age_list.append(age) #Adds user(s) age to list
    if not age_list: 
        print("No age lists exists")
        return [] #Empty list will return if no data or invalid data is inputed 
    return age_list
             
def average2(Data,lower,upper):
    """Calculates the average income"""
    income_list = income2(Data,lower,upper)
    if len(income_list) == 0: #Checks if length of list is zero 
        print("Divsion by zero error")
        return 0 #Returns zero if length of list is zero 
    else: 
        average_income = sum(income_list)/len(income_list) #Calculates average income
    return average_income

def average3(Data,lower,upper):
    """Calculates the average age"""
    age_list = age_of_users(Data,lower,upper)
    if len(age_list) == 0: #Checks if length of list is zero 
        print("Divsion by zero error")
        return 0 #Returns zero if length of list is zero 
    else:
        average_age = sum(age_list)/len(age_list) #Calculates average age 
    return average_age
    
    
def output4(Data,lower,upper):
    """Calculates the correlation value"""
    age_list = age_of_users(Data,lower,upper)
    income_list2 = income2(Data,lower,upper)
    average_age = average3(Data,lower,upper)
    average_income = average2(Data,lower,upper) 
    value1 = sum(((x - average_age) * (y - average_income) for x, y in zip(age_list, income_list2))) #uses loop and zip to combine both lists element wise for calculation 
    value2 = sum((x - average_age) ** 2 for x in age_list) #uses loop to iterate over every item in age_list for calculation 
    value3=sum((y - average_income) ** 2 for y in income_list2) #uses loop to iterate over every item in income_list2 for calculation 
    value4 = (value2*value3)**0.5
    if value4 == 0: #Checks if value 4 is zero 
        print("Division by zero error")
        return 0
    else:
        return round(value1/value4,4) #Calculates correlation by dividing value 1 by value 4
   
