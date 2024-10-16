# BEFORE EVERYTHING, PLEASE INSTALL ALL IN THE REQUIREMENTS.TXT FILE BY pip install -r requirements.txt INTO YOUR VENV, IT WILL NOT WORK IF NOT DONE.
# Import JSON (storage), os.path (check for file), rich (for tables and prettifying)
import json
import os.path
import rich
import rich.console
import rich.table

# Defines the menu
def menu():
    cond = True
    # Creates a loop to allow restarts for invalid input
    while cond == True:
        # Gives the options
        print("\nBus Investigation Application - v1")
        print("- Type 1 to input data")
        print("- Type 2 to search the data")
        print("- Type 3 to read the data and print statistics")
        print("- Type 9 to exit")
        userInput = int(input("What would you like to do? "))
        if userInput == 1:
            inputData()
        elif userInput == 2:
            searchData()
        elif userInput == 3:
            readData()
        elif userInput == 9:
            cond = False
        else:
            print("INVALID INPUT, TRY AGAIN \n")

# Data Search Engine ( very complicated )
def searchData():
    # Reads the file
    data = fileRead()
    print("\nReading Data..")
    # Checks the validity of the file
    if data != False and type(data) is dict:
        condition = True
        print("\nBUS INVESTIGATION SEARCH ENGINE")
        while condition == True:
            # Search by day, week or route
            selection = int(input("Search by (1) day, (2) week, (3) route, (4) day/week/route, (9) exit: \n"))
            # Search by all parameters
            if selection == 4:
                condition2 = True
                while condition2 == True:
                    route = input("What route are you looking at? (q to exit) ").upper()
                    if route == buses[0] or route == buses[1] or route == buses[2] or route == buses[3] or route == buses[4] or route == buses[5]:
                        condition3 = True
                        while condition3 == True:
                            week = int(input("What week are you looking at? "))
                            if week == weeks[0] or week == weeks[1] or week == weeks[2] or weeks == weeks[3]:
                                condition4 = True
                                while condition4 == True:
                                    day = input("What day are you looking at? ").lower()
                                    if day == days[0].lower() or day == days[1].lower() or day == days[2].lower() or day == days[3].lower() or day == days[4].lower():
                                        print(f"\nFound: Bus {route} on week {week} and day {day.capitalize()}.")
                                        busTime = data[f'{route}{week}{day.capitalize()}']
                                        if busTime < 0:
                                            busTime2 = busTime * -1
                                            print(f"Your bus is running late by {busTime2} minutes.")
                                        elif busTime == 0:
                                            print(f"Your bus is running on time!")
                                        elif busTime > 0:
                                            print(f"Your bus is running {busTime} minutes ahead!")
                                        print("")
                                        condition4 = False
                                    else:
                                        print("We could not find your particular day on our system, please try again.")
                                        condition4 = False
                                condition3 = False
                            else:
                                print("We could not find your particular week in our system, please try again.")
                                condition3 = False
                    elif route == "Q":
                        condition2 = False
                    else:
                        print("We could not find your particular route in our system, please try again.")
            # Search by route
            elif selection == 3:
                condition2 = True
                while condition2 == True:
                    route = input("What route are you looking at? (9 to exit) ").upper()
                    # Prints route information in table
                    if route == buses[0] or route == buses[1] or route == buses[2] or route == buses[3] or route == buses[4] or route == buses[5]:
                        print(f"Printing Bus Punctuality Table for Route {route}:\n")
                        table = rich.table.Table(title=f"Bus Punctuality for Route {route}")
                        table.add_column("Week:")
                        for day in days:
                            table.add_column(day)
                        for week in weeks:
                            table.add_row(str(week),str(data[f'{route}{week}{days[0]}']),str(data[f'{route}{week}{days[1]}']),str(data[f'{route}{week}{days[2]}']),str(data[f'{route}{week}{days[3]}']),str(data[f'{route}{week}{days[4]}']))
                        console = rich.console.Console()
                        console.print(table)
                        print("Key: \nPositive Number means ahead of schedule by n minutes. \nNegative number means behind schedule by n minutes. \n0 means on time.\n")
                        noLate = 0
                        busLate = False
                        # Prints buses that were late below
                        for week in weeks:
                            for day in days:
                                number = int(data[f'{route}{week}{day}'])
                                if number < 0:
                                    if busLate == False:
                                        busLate = True
                                        print("BUSES THAT WHERE LATE:")
                                    noLate = noLate + 1
                                    print(f"Bus Route {route} on Week {week} on Day {day} was late by {data[f'{route}{week}{day}'] * -1} minutes.")
                        print(f"Number of times bus route {route} was late: {noLate}\n")
                    elif route == "9":
                        condition2 = False
                    else:
                        print("We could not find your particular route in our system, please try again.")
            # Search by week
            elif selection == 2:
                condition2 = True
                while condition2 == True:
                    week = int(input("What week are you looking at? (9 to exit) "))
                    # Print week timetable for buses in table
                    if week == weeks[0] or week == weeks[1] or week == weeks[2] or week == weeks[3]:
                        print(f"Printing Bus Punctuality table for week {week}...\n")
                        table = rich.table.Table(title=f"Bus Punctuality for Week {week}")
                        table.add_column("Route")
                        for day in days:
                            table.add_column(day)
                        for bus in buses:
                            table.add_row(str(bus),str(data[f'{bus}{week}{days[0]}']),str(data[f'{bus}{week}{days[1]}']),str(data[f'{bus}{week}{days[2]}']),str(data[f'{bus}{week}{days[3]}']),str(data[f'{bus}{week}{days[4]}']))
                        console = rich.console.Console()
                        console.print(table)
                        print("Key: \nPositive Number means ahead of schedule by n minutes. \nNegative number means behind schedule by n minutes. \n0 means on time.\n")
                        noLate = 0
                        busLate = False
                        # Prints a new section with only buses that where late
                        for bus in buses:
                            for day in days:
                                if data[f'{bus}{week}{day}'] < 0:
                                    if busLate == False:
                                        busLate = True
                                        print("BUSES THAT WHERE LATE:")
                                    noLate = noLate + 1
                                    print(f"Bus Route {bus} on Week {week} on Day {day} was late by {data[f'{bus}{week}{day}'] * -1} minutes.")
                        print(f"Number of times bus was late in week {week}: {noLate}\n")
                    elif week == 9:
                        condition2 = False
                    else:
                        print("We could not find your particular week in the system, please try again.")
            # Search by day
            elif selection == 1:
                condition2 = True
                while condition2 == True:
                    day = input("What day are you looking at? (9 to exit) ").lower()
                    # Output day timetable for buses in a table
                    if day == days[0].lower() or day == days[1].lower() or day == days[2].lower() or day == days[3].lower() or day == days[4].lower():
                        print(f"Printing Bus Punctuality table for day {day.capitalize()}...\n")
                        table = rich.table.Table(title=f"Bus Punctuality for Day {day.capitalize()}")
                        table.add_column("Week")
                        for bus in buses:
                            table.add_column(str(bus))
                        for week in weeks:
                            table.add_row(str(week),str(data[f'{buses[0]}{week}{day.capitalize()}']),str(data[f'{buses[1]}{week}{day.capitalize()}']),str(data[f'{buses[2]}{week}{day.capitalize()}']),str(data[f'{buses[3]}{week}{day.capitalize()}']),str(data[f'{buses[4]}{week}{day.capitalize()}']),str(data[f'{buses[5]}{week}{day.capitalize()}']))
                        console = rich.console.Console()
                        console.print(table)
                        print("Key: \nPositive Number means ahead of schedule by n minutes. \nNegative number means behind schedule by n minutes. \n0 means on time.\n")
                        noLate = 0
                        busLate = False
                        # Print out all the buses that were late or nothing if no buses were late. 
                        for bus in buses:
                            for week in weeks:
                                if data[f'{bus}{week}{day.capitalize()}'] < 0:
                                    if busLate == False:
                                        busLate = True
                                        print("BUSES THAT WHERE LATE:")
                                    noLate = noLate + 1
                                    print(f"Bus Route {bus} on Week {week} on Day {day} was late by {data[f'{bus}{week}{day.capitalize()}'] * -1} minutes.")
                        print(f"Number of times bus was late on day {day} throughout all {len(weeks)} weeks: {noLate}\n")
                    elif day == "9":
                        condition2 = False
                    else:
                        print("We could not find your particular day in the system, please try again.")
            elif selection == 9:
                condition = False
            else:
                print("INVALID INPUT, TRY AGAIN.")
    else:
        print("DATA.JSON NOT PRESENT OR CORRUPTED \n")

def readData():
    # Read the data from json file
    data = fileRead()
    print("\nReading Data: ")
    # Verify data exists
    if data != False and type(data) is dict:
        writeDictionary = {}
        totalLateList = {}
        # Write out statistics for each bus
        for bus in buses:
            print(f"\nStatistics for Bus {bus}")
            noLate,avgLate,avgLateofLate, statDictionary = statBuses(bus, data)
            print(f"Number of times late: {noLate}")
            print(f"Average time of arrival: {avgLate}")
            print(f"Average time late: {avgLateofLate}")
            totalLateList[bus] = noLate
            writeDictionary[f"Bus {bus}"] = statDictionary
        noLatest = -1
        noLatestBus = ""
        # Compute and write out statistics for all the buses
        for bus, noLate in totalLateList.items():
            if noLate > noLatest:
                noLatest = noLate
                noLatestBus = bus
            elif noLate == noLatest:
                noLatestBus = f"{noLatestBus} and {bus}"
        print(f"\nThe bus that was late the most was Bus {noLatestBus} with it being late {noLatest} times throughout the 4 weeks.")
        # Write the statistics dictionary to statistics.json
        inputWriteToFile(writeDictionary,"statistics.json")
    else:
        print("DATA.JSON NOT PRESENT OR CORRUPTED \n")

def statBuses(busCode:str, data:dict):
    # Computes statistics of late times for each bus
    noLate = 0
    lateTimes = []
    times = []
    for week in weeks:
        for day in days:
            number = int(data[f'{busCode}{week}{day}'])
            if number < 0:
                noLate = noLate + 1
                lateTimes.append(number)
            times.append(number)
    lateTimesTotal = 0
    # Computes statistics of late times and average late times for all data
    for i in lateTimes:
        lateTimesTotal = lateTimesTotal + i
    if noLate != 0:
        lateTimesAvg = round(lateTimesTotal / noLate)
    else:
        lateTimesAvg = 0
    timesTotal = 0
    for i in times:
        timesTotal = timesTotal + i
    timesAvg = round(timesTotal / len(times))
    # Outputs all the data to a dictionary and returns.
    dictionary = {}
    dictionary['Total amount of times bus was late'] = noLate
    dictionary['Average of lateness of times when bus was late'] = lateTimesAvg
    dictionary['Total times the bus arrived'] = len(times)
    dictionary['Average time of bus arrival (0 is on-time, -num is late)'] = timesAvg
    return noLate, timesAvg, lateTimesAvg, dictionary

def inputData():
    print("\nDATA INPUT SECTION:")
    # IGNORE THIS SECTION
    """selection = input('How would you like to input your data (anything for one by one or 2 for in batches) (default: 1): \n')
    if selection == "2":
        array = batchInputData()
        return array
    else:
        data = {}
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
        inputWriteToFile(data,"data.json")"""
    # IGNORE THIS SECTION ( ONLY SO MY FLOWCHART DOESN'T BE BIG )
    # Hands the process over to batchinputdata function
    array = batchInputData()
    return array

def batchInputData():
    data = {}
    # For each bus, input on time performance in schema num1,num2,num3... etc.
    for bus in buses:
        condition = True
        while condition == True:
            batchUserInput = input(f"Input the data for the on time performance of the bus {bus} for days in format num1,num2,num3,...etc with them being in order of day from Monday1 - Sunday1, Monday2 - Sunday2, etc: \n")
            batchUserArray = batchUserInput.split(",")
            # Verifies data with verify function
            if verifyDataArray(batchUserArray) == True:
                nd = 0
                nw = 0
                # Appends all the data to a dictionary.
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
    # Writes the data to data.json
    inputWriteToFile(data,"data.json")

def verifyDataArray(array:dict):
    # Verifies the data by seeing if there is 20 entries.
    if len(array) != 20:
        return False
    else:
        # Computes if every data is a integer digit
        for i in array:
            if i.isdigit() != True:
                return False
        return True

def inputWriteToFile(data: dict,file: str):
    # Defines a file to be opened
    file = open(file, "w")
    # Dump data in json to the file
    fileContents = json.dumps(data, indent=2)
    file.write(fileContents)
    file.close()
    print("Successfully written data to file!\n")
    return True

def fileRead():
    # If the file exists
    if os.path.exists("data.json"):
        # Open the data.json file and read the objects in the file
        file = open("data.json","r")
        fileContents = file.read()
        file.close()
        # Convert file to json.
        fileArray = json.loads(fileContents)
        return fileArray
    else:
        return False

def loadGlobal():
    # Load the global variables
    global buses
    global days
    global weeks
    buses = ["A","B","C","D","E","F"]
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    weeks = [1, 2, 3, 4]

if __name__ == "__main__":
    # Start the app by loading the global variables and starting the menu. 
    loadGlobal()
    menu()
    # Exiting when menu is exited. 
    exit()