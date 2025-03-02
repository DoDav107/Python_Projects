def read_file(cvsfile):
    """Reads the file and returns each line in the file as a dictioanry in a list"""
    data_list = []
    try:
        with open(cvsfile, 'r') as file: #Opens and reads the file
            headers = file.readline().strip().split(',') #Reads first line and removes whitespaces and splits items into a list  
            headers_list = []
            for item in headers: #Iterates over each header and makes it lowercase
                headers_list.append(item.lower()) 
            
            for line in file: #Iterates over each line in file after headers
                rows = line.strip().split(',') #Removes whitespaces and splits items from each line into a list 
                row_dict = zip(headers_list, rows) #Creates a tuple by making headers as keys and rows as values  
                data_list.append(dict(row_dict)) #Adds items as lists in Data_list
                
    except FileNotFoundError:
        print("Invalid Data/File does not exist")
        return [] #Empty list will return if no data or invalid data is inputed 
    return data_list

def main(cvsfile):
    """Returns the four outputs OP1,OP2,OP3,OP4"""
    Data1 = read_file(cvsfile) #Calls on the Data intially reads
    Data2 = filtered_Data(Data1) #Calls on the filtered Data that is valid
    Valid_Data = remove_duplicates(Data2) #Calls on the filtered Data that is valid with no user duplicates
    OP1 = output1(Valid_Data)
    OP2 = output2(Valid_Data)
    OP3 = output3(Valid_Data)
    OP4 = output4(Valid_Data)
    return OP1,OP2,OP3,OP4

def is_valid(age,income,time_spent,engagement):
    """Checks if age,income,time_spent and engagement_score are all valid"""
    #Condition to check if the file contains valid inputs for age,income,time_spent and engagement_score
    if age.replace(".","").isdigit() and float(age)>=0 and income.replace(".","").isdigit() \
       and float(income) >= 0 and time_spent.replace(".","").isdigit() and float(time_spent) >= 0 \
       and engagement.replace(".","").isdigit() and float(engagement) >= 0:
        return True
    
    return False
    
def filtered_Data(Data1):
    """Returns valid data after filtering out the invalid data in the file"""
    Filtered_Data = []
    try:
        for item in Data1: #Iterates over every dictionary containing headers as keys and rows as values in Data1
            user_id = item["id"].lower()
            age = (item["age"])
            time_spent = (item["time_spent_hour"])
            engagement = (item["engagement_score"])
            income = (item["income"])
            platform = item["platform"].lower()
            profession = item["profession"].lower()
            if user_id.isalnum() and is_valid(age,income,time_spent,engagement) and platform != "" and profession != "": #Checks if Data in every dictionary in Data1 is valid
                Filtered_Data.append(item) #appends every valid dictionary in Data1 to list
    except KeyError:
        print("Key in dictionary does not exist/No valid data")
        return [] #Empty list will return if no data or invalid data is inputed
    
    return Filtered_Data

def remove_duplicates(Data2):
    """Removes user_id(s) that have duplicates"""
    user_id_count = {} #Counts the occuracnes of each user_id
    Valid_Data = [] 
    for item in Data2: #Iterates over the filtered/valid Data 
        ID = item["id"].lower()
        if ID not in user_id_count: 
            user_id_count[ID] = 1 
        else: 
            user_id_count[ID] += 1
                
    for item in Data2:      
        if user_id_count[item['id'].lower()] == 1: #Checks the user_ids that have a count of 1 
            Valid_Data.append(item) #appends valid dictionaries that doesn't have duplicate user_ids
    
    return Valid_Data
    
def output1(Valid_Data):
    """Returns a list containing two dictionary items"""
    lis1= [{},{}]
    for item in Valid_Data: #Iterates over the filtered/Valid Data
        key1 = "student"
        user_id = item['id'].lower()
        profession = item['profession'].lower()
        age = int(item['age'])
        time_spent = int(item['time_spent_hour'])
        engagement = round(float(item['engagement_score']),4)
        if profession == key1:   # Checks if the user profession is student 
            lis1[0][user_id] = [age, time_spent, engagement] #assigns the list of data to the unique user_id for student(s)
        else:
            lis1[1][user_id] = [age, time_spent, engagement] #assigns the list of data to the unique user_id for non-student(s)
    
    return lis1

def platforms(Valid_Data):
    """Returns a dictionary containing the engagement time for every platform"""
    engagement_time_dic = {}
    for item in Valid_Data: #Iterates over the filtered/Valid Data
        platform = item["platform"].lower()
        engagement = float(item["engagement_score"])
        time_spent = int(item["time_spent_hour"])
        engagement_time = (time_spent * engagement) / 100
        if platform not in engagement_time_dic:
            engagement_time_dic[platform] = [] #assigns an empty list to the platform if not found in engagement_time_dic
        engagement_time_dic[platform].append(engagement_time) #appends the engagement_time of the platform to its list
    
    return engagement_time_dic

def engagemnt_time_calculations(times):
    """Returns a list containing the total, average and standard deviation of engagemnt time of users belonging to a certain platform"""
    engagemnt_time_stats = [] #Initialising variable to avoid name errors and to make it clear that it will be used later
    total = sum(times)
    average =  total/ len(times)
    if len(times) == 1:#Checks if the length of the list containing engagemnt time(s) is valid for calculation
        standard__deviation = 0.0
        engagemnt_time_stats = [round(total,4), round(average,4) , round(standard__deviation, 4)]
    else:
        variance = sum((time - average) ** 2 for time in times) / (len(times) - 1)
        standard__deviation = variance ** 0.5
        engagemnt_time_stats = [round(total,4), round(average,4) , round(standard__deviation, 4)] #list containing the calculations for engagemnt time
   
    return engagemnt_time_stats

def output2(Valid_Data):
    """Returns a dictionary where the keys are the platforms and the values are the lists containing information about engagement time of users""" 
    p = platforms(Valid_Data)
    engagemnt_time_stats = {}
    for platform, times in p.items(): #Iterates over every key and value pair in the dictionary
        engagemnt_time_stats[platform] = engagemnt_time_calculations(times) #assigns the list containing the statistics of engagemnt_time(s) to each platform
   
    return engagemnt_time_stats

def output3(Valid_Data):
    """Returns a list containing cosine similarity scores"""
    value5 = 0 #Initialising variables to avoid name errors and to make it clear that value5 and 10 will be used later
    value10 = 0
    age_list = []
    income_list = []
    age_list2 = []
    income_list2 = []
    for item in Valid_Data: #Iterates over the filtered/Valid Data
        key1 = "student"
        profession = item["profession"].lower()
        age = int(item["age"])
        income = int(item["income"])
        if profession == key1:   # Checks if the user profession is student 
            age_list.append(age)
            income_list.append(income)
            value1 = sum((x * y for x, y in zip(age_list, income_list))) 
            value2 = sum(x**2 for x in age_list) **0.5
            value3 = sum(y**2 for y in income_list) **0.5
            value4 = value2 * value3
            value5 = round(value1/value4,4) # cosine similarity score for student(s)
        else: #Calculations for non-student(s)
            age_list2.append(age)
            income_list2.append(income)
            value6 = sum((a * b for a, b in zip(age_list2, income_list2)))
            value7 = sum(a**2 for a in age_list2) **0.5
            value8 = sum(b**2 for b in income_list2) **0.5
            value9 = value7 * value8
            value10 = round(value6/value9,4) # cosine similarity score for non-student(s)
            
    return [value5,value10]
                
def engagement_time_of_users(Valid_Data):
    """Returns two lists containing engagement times for users who are students or non-students"""
    lis1 = []
    lis2 = []
    for item in Valid_Data: #Iterates over the filtered/Valid Data
        key1 = "student"
        profession = item["profession"].lower()
        engagement = float(item["engagement_score"])
        time_spent = int(item["time_spent_hour"])
        engagement_time = (time_spent * engagement) / 100
        if profession == key1: # Checks if the user profession is student 
            lis1.append(engagement_time) #appends the engagement_time(s) of users who are students

        else:
            lis2.append(engagement_time) #appends the engagement_time(s) of users who aren't students
    
    return lis1,lis2

def averages(Valid_Data):
    """Returns the averages of the engagement times for students and non-students""" 
    lis1,lis2 = engagement_time_of_users(Valid_Data)
    if len(lis1)!=0 and len(lis2)!=0: #Checks if the lengths of the lists are valid for calculation 
        average1 = sum(lis1)/len(lis1)
        average2 = sum(lis2)/len(lis2)
        return average1,average2
    else:
        print("Division by Zero Error/Invalid Data")
        return 0,0

def standard_deviation(Valid_Data):
    """Calculates the standard deviation of engagement times for students and non-students"""
    lis1,lis2 = engagement_time_of_users(Valid_Data)
    average1,average2 = averages(Valid_Data)
    if len(lis1)>1 and len(lis2)>1:  #Checks if the lengths of the lists are valid for calculation 
        variance1 = (sum((x-average1)**2 for x in lis1))/(len(lis1)-1)  #uses loop to iterate over every item in engagement_time_ of student(s) to calculate variance
        standard_deviation1 = variance1**0.5  #calculates standard_deviation for student(s)
        variance2 = (sum((y-average2)**2 for y in lis2))/(len(lis2)-1)  #uses loop to iterate over every item in engagement_time of non-student(s) to calculate variance
        standard_deviation2 = variance2**0.5  #calculates standard_deviation for non-student(s)
    else:
        print("Division by Zero Error/Invalid Data")
        return 0,0 #Returns a values of zero if there is invalid Data or calculation
    
    return standard_deviation1, standard_deviation2

def pooled_standard_deviation(Valid_Data):
    """Calculates the pooled standard deviation of engagement times for students and non-students"""
    lis1,lis2 = engagement_time_of_users(Valid_Data)
    standard_deviation1, standard_deviation2 = standard_deviation(Valid_Data)
    if standard_deviation1 != 0 and standard_deviation2 != 0: #Checks if the values of standard deviations are valid for calculation 
        n1 = len(lis1)
        n2 = len(lis2)
        value1 = (n1-1)*((standard_deviation1)**2)
        value2 = (n2-1)*((standard_deviation2)**2)
        value3 = value1 + value2
        value4 = n1 + n2 - 2
        value5 = (value3/value4)**0.5
    else:
        print("Error due to Invalid data")
        return 0 #Returns a value of zero if there is invalid Data for the standard deviations/Calculation
    
    return value5
    
def output4(Valid_Data):
    """Returns a numeric value for Cohen's test for engagement time of students and non-students"""
    average1,average2 = averages(Valid_Data)
    s = pooled_standard_deviation(Valid_Data)
    if s!=0: #Checks if the value of pooled_standard_deviation is valid for calculation 
        d = (average1 - average2)/s
        return round(d,4)
    else:
        print("Divsion by Zero Error/Invalid Data")
        return 0

            





