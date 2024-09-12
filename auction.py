import json
import os.path

def menu():
    condition = True
    while condition == True:
        print("\nSilent Auction Application - v1")
        print("What would you like to do?")
        userInput = int(input("Type 1 to input auction details, Type 2 to display details of items, Type 3 to enter bids, Type 4 to compute/show bidding results, Type 9 to exit: \n"))
        if userInput == 1:
            auctionDetailInput()
        elif userInput == 2:
            displayAuction()
        elif userInput == 3:
            startAuction()
        elif userInput == 4:
            printAuctionResults()
        elif userInput == 9:
            condition = False
        else:
            print("")

def printAuctionResults():
    pass

def startAuction():
    auctionDetails = fileRead("auctions.json")
    print("\nSELECTED: COMMENCE AUCTION")
    if auctionDetails != False:
        #method = int(input("Type 1 to enter already cast bids, Type 2 to start bidding process (if bids weren't cast before)"))
        bids = enterBids(auctionDetails)
    else:
        print("AUCTIONS FILE DOES NOT EXIST, PLEASE CREATE ONE BY SELECTING TO INPUT AUCTION DETAILS")

def enterBids(auctionDetails:dict):
    print("ENTERING BIDS INTO MACHINE")
    condition = True
    invalidBids = 0
    underReserveBids = 0
    bids = []
    while condition == True:
        print("BID IDENTITY SEPARATOR ---")
        bidCode = input("Input the bid number for the bid: ")
        if bidCode.isdigit() != True:
            invalidBids = invalidBids + 1
            print("INVALID BID, PROCEEDING TO NEXT BID")
        else:
            for x in auctionDetails.keys():
                if bidCode == x:
                    validity = True
            if not validity:
                invalidBids = invalidBids + 1
            else:
                bidValue = float(input("Input the value of the bid: $"))
                if bidValue.replace(".","",1).isdigit() != True:
                    invalidBids = invalidBids + 1
                    print("INVALID BID, PROCEEDING TO NEXT BID")
                else:
                    if bidValue < auctionDetails[bidCode]["reserve"]:
                        invalidBids = invalidBids + 1
                        underReserveBids = underReserveBids + 1
                        print("INVALID BID: BID UNDER RESERVE, PROCEEDING TO NEXT BID")
                    else:
                        append = f"{bidCode}:{bidValue}"
                        bids.append(append)
                        print("BID SUCCESSFULLY CAST")
        selection = input("INPUTTING MORE BIDS? (ANYTHING FOR YES, n FOR NO)").lower()
        if selection == "n":
            condition = False
        elif not selection:
            pass
        else:
            pass
    print("Bids have all been entered into the system")
    print(f"There were {invalidBids} invalid bids, {underReserveBids} of them were under the reserve price.")
    fileSave(bids,"bids.json")

def displayAuction():
    auctionDetails = fileRead("auctions.json")
    print("\nSELECTED: READ DATA")
    if auctionDetails != False:
        totalAuctionValue = float(0)
        for auctionNumber in auctionDetails.keys():
            print(f"\nAUCTION: {auctionNumber}")
            print(f"Name: {auctionDetails[f"{auctionNumber}"]['name']}")
            print(f"Year: {auctionDetails[f"{auctionNumber}"]['year']}")
            print(f"Description: {auctionDetails[f"{auctionNumber}"]['description']}")
            print(f"Reserve: ${auctionDetails[f"{auctionNumber}"]['reserve']}")
            totalAuctionValue = totalAuctionValue + auctionDetails[f"{auctionNumber}"]['reserve']
        print(f"\nTotal Auctions: {len(auctionDetails.keys())}")
        print(f"Total Auction Value (at reserve pricing): ${round(totalAuctionValue,2)}")
    else:
        print("AUCTIONS FILE DOES NOT EXIST, PLEASE CREATE ONE BY SELECTING TO INPUT AUCTION DETAILS")

def auctionDetailInput():
    print("\nSELECTED: INPUT DATA")
    print("Item Number will be automagically assigned to each item.")
    print("We require at least 10 items to be sold at this auction.")
    auctionDetails = {}
    itemNumber = 1
    condition = True
    while condition == True:
        print(f"ENTER DETAILS BELOW for Item: {itemNumber}")
        cond2 = True
        while cond2 == True:
            artist = input("Please input the name or psuedonym of the artist: ")
            if artist != "":
                cond2 = False
            else:
                print("Try Again")
        cond2 = True
        while cond2 == True:
            itemDescription = input("Please input a simple description of the work: ")
            if itemDescription != "":
                cond2 = False
            else:
                print("Try Again")
        cond2 = True
        while cond2 == True:
            year = int(input("Please input the year of the work: "))
            if not year:
                print("Try Again")
            elif year < 0:
                print("Try Again")
            else:
                cond2 = False
        cond2 = True
        while cond2 == True:
            reserve = float(input("Please input the reserve price of the work: $"))
            if not reserve:
                print("Try Again")
            elif year < 1:
                print("RESERVE CANNOT BE UNDER $1!")
            else:
                cond2 = False
        dictionary = {}
        dictionary['name'] = artist
        dictionary['description'] = itemDescription
        dictionary['year'] = year
        dictionary['reserve'] = round(reserve,2)
        auctionDetails[f"{itemNumber}"] = dictionary
        if itemNumber > 9:
            selection = input("Do you want to continue inputting items? (0 for no, anything else but nothing for yes) ")
            if selection == "0":
                condition = False
            else:
                itemNumber = itemNumber + 1
        else:
            itemNumber = itemNumber + 1
    print("\nSaving Auction choices to file 'auctions.json'")
    fileSave(auctionDetails,'auctions.json')
    print("")

def fileSave(data,location:str):
    file = open(location,"w")
    dataJson = json.dumps(data, indent=2)
    file.write(dataJson)
    file.close()
    print(f"File saved successfully to {location}!")

def fileRead(location:str):
    if os.path.exists(location):
        file = open(location,"r")
        fileContents = file.read()
        file.close()
        fileArray = json.loads(fileContents)
        return fileArray
    else:
        return False
    
if __name__ == "__main__":
    menu()
    exit()