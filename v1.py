import json

def menu():
    cond = True
    while cond == True:
        print("Bus Investigation Application - v1")
        print("What would you like to do?")
        userInput = input("Type 1 to input data, Type 2 to search the data, Type 3 to read the data, Type e to exit: \n").lower()
        if userInput == "1":
            inputData()
#        elif userInput == "2":
#            searchData()
#        elif userInput == "3":
#            readData()
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
        inputWriteToFile(data)

def batchInputData():
    data = {}
    buses = ["A","B","C","D","E","F"]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weeks = [1, 2, 3, 4]
    for bus in buses:
        condition = True
        while condition == True:
            batchUserInput = input(f"Input the data for the on time performance of the bus {bus} for days in format num1,num2,num3,...etc with them being in order of day from Monday1 - Sunday1, Monday2 - Sunday2, etc: \n")
            batchUserArray = batchUserInput.split(",")
            if len(batchUserArray) == 20:
                nd = 0
                nw = 0
                for x in batchUserArray:
                    if nw < 6:
                        currentDay = days[nd]
                        currentWeek = weeks[nw]
                        append = int(x)
                        data[f'{bus}{currentWeek}{currentDay}'] = append
                        if nd == 4:
                            nw = nw + 1
                            nd = 0
                        else:
                            nd = nd + 1
                    else:
                        pass
                condition = False
            else:
                print("INPUT A CORRECT SET OF DATA PLEASE")
    inputWriteToFile(data)

def inputWriteToFile(data: dict):
    file = open("data.json", "w")
    fileContents = json.dumps(data)
    file.write(fileContents)
    file.close()
    print("Successfully written data to file!\n")
    return True

if __name__ == "__main__":
    menu()
    exit()