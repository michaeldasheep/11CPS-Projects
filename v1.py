import json

def menu():
    cond = True
    while cond == True:
        print("Bus Investigation Application - v1")
        print("What would you like to do?")
        userInput = input("Type 1 to input data, Type 2 to search the data, Type 3 to read the data, Type e to exit: \n").lower()
        if userInput == "1":
            inputData()
        elif userInput == "2":
            searchData()
        elif userInput == "3":
            readData()
        elif userInput == "e":
            cond = False
        else:
            print("INVALID INPUT, TRY AGAIN \n")

def inputData():
    print("\nDATA INPUT SECTION:")
    selection = input('How would you like to input your data (either 1 for one by one or 2 for in batches) (default: 1): \n')
    if selection == "2":
        array = batchInputData()
        return array
    else:
        data = {}
        buses = ["A","B","C","D","E","F"]
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        weeks = [1, 2, 3, 4]
        for bus in buses:
            for week in weeks:
                for day in days:
                    condition = True
                    while condition == True:
                        userInputBusData = int(input(f"For Week {week}, what was the on time performance of the bus on {day} (-number for late by number or number for early by number?): \n"))
                        if userInputBusData.isdigit() == True:
                            data[f'{bus}{day}{week}'] = userInputBusData
                            condition = False
                        else:
                            print("Please input a valid number!")
        file = open("data.json", "w")
        fileContents = json.dumps(data)
        file.write(fileContents)
        file.close()
        return True

def batchInputData():
    buses = ["A","B","C","D","E","F"]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weeks = [1, 2, 3, 4]
    for bus in buses:
        batchUserInput = input("Input the data for the on time performance of the bus for days in format num1,num2,num3,...etc with them being in order of day from Monday1 - Sunday1, Monday2 - Sunday2, etc: \n")
        batchUserArray = batchUserInput.split(",")
        condition = True
        while condition == True:
            batchUserNum = len(batchUserArray)

if __name__ == "__main__":
    menu()