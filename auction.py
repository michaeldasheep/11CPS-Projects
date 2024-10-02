import json
import os.path

def menu():
    condition = True
    while condition == True:
        print("\nSilent Auction Application - v1")
        print("- Type 1 to input auction details")
        print("- Type 2 to display details of items")
        print("- Type 3 to enter bids/commence auction")
        print("- Type 4 to compute auction results")
        print("- Type 9 to exit")
        userInput = int(input("What would you want to do? "))
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
    bids = fileRead("bids.json")
    auctionDetails = fileRead("auctions.json")
    print("\nSELECTED: AUCTION RESULTS")
    if bids == False or auctionDetails == False:
        print("BIDS or AUCTION FILE DOES NOT EXIST, CREATE ONE BY COMMENCING AN AUCTION OR INPUTTING DATA.")
    else:
        auctionHighestValueDict = {}
        auctionBidsCastCount = {}
        auctionOutputFile = {}
        auctionSuccess = 0
        for auction in auctionDetails.keys():
            auctionHighestValueDict[auction] = f"NO-ONE:{auctionDetails[auction]['reserve'] - 0.01}"
            auctionBidsCastCount[auction] = 0
        for bidNum in bids.keys():
            xData = bids[bidNum].split(":")
            highestValue = auctionHighestValueDict[xData[0]].split(':')
            if float(xData[1]) > float(highestValue[1]):
                auctionHighestValueDict[xData[0]] = f"{bidNum}:{xData[1]}"
            auctionBidsCastCount[xData[0]] = auctionBidsCastCount[xData[0]] + 1
        for auction in auctionHighestValueDict.keys():
            print(f"\nAUCTION RESULTS FOR AUCTION {auction}:")
            if float(highestValue[1]) == float(auctionDetails[auction]['reserve'] - 0.01) or auctionBidsCastCount[auction] == 0:
                print(f"The work '{auctionDetails[auction]['description']}' by '{auctionDetails[auction]['name']}' is being bid on.")
                print(f"The reserve for this product was ${auctionDetails[auction]['reserve']}.")
                print(f"There were no valid bids cast for this product.")
                print(f"The winner of this auction was no one, the reserve was not met.")
                dictionary = {}
                dictionary['Artist'] = auctionDetails[auction]['name']
                dictionary['Description'] = auctionDetails[auction]['description']
                dictionary['Reserve Price'] = auctionDetails[auction]['reserve']
                dictionary['Bids Cast'] = 0
                dictionary['Winner'] = "no one"
                dictionary['Winning Bid Value'] = 0
                dictionary['Commision'] = 0
                dictionary['Total Payable'] = 0
                dictionary['Sold'] = False
                auctionOutputFile[f"Auction {auction}"] = dictionary
            else:
                xData = auctionHighestValueDict[auction].split(":")
                print(f"The work '{auctionDetails[auction]['description']}' by '{auctionDetails[auction]['name']}' is being bid on.")
                print(f"The reserve for this product was ${auctionDetails[auction]['reserve']}.")
                print(f"There were {auctionBidsCastCount[auction]} valid bids cast for this product.")
                print(f"The winner of this auction was bid number {xData[0]}, with the their bid of ${xData[1]}.")
                commision = float(xData[1]) * 0.1
                print(f"The total price payable is ${round(commision + float(xData[1]),2)} with a ${round(commision,2)} (10%) commision added.")
                dictionary = {}
                dictionary['Artist'] = auctionDetails[auction]['name']
                dictionary['Description'] = auctionDetails[auction]['description']
                dictionary['Reserve Price'] = float(auctionDetails[auction]['reserve'])
                dictionary['Bids Cast'] = int(auctionBidsCastCount[auction])
                dictionary['Winner'] = f"Bid Number: {xData[0]}"
                dictionary['Winning Bid Value'] = float(xData[1])
                dictionary['Commision'] = round(commision,2)
                dictionary['Total Payable'] = round(commision + float(xData[1]),2)
                dictionary['Sold'] = True
                auctionOutputFile[f"Auction {auction}"] = dictionary
                auctionSuccess = auctionSuccess + 1
        print("\nSaving Auction Results to auctionResults.json")
        fileSave(auctionOutputFile,"auctionResults.json")

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
    bids = {}
    while condition == True:
        print("BID IDENTITY SEPARATOR ---")
        bidCode = input("Input the bid product number for the bid: ")
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
                bidNum = int(input("Input the bid number for the bidder: "))
                if not bidNum:
                    print("INVALID BID, PROCEEDING TO NEXT BID")
                else:
                    bidValue = float(input("Input the value of the bid: $"))
                    if isFloat(bidValue) != True:
                        invalidBids = invalidBids + 1
                        print("INVALID BID, PROCEEDING TO NEXT BID")
                    else:
                        if float(bidValue) < float(auctionDetails[bidCode]["reserve"]):
                            invalidBids = invalidBids + 1
                            underReserveBids = underReserveBids + 1
                            print("INVALID BID: BID UNDER RESERVE, PROCEEDING TO NEXT BID")
                        else:
                            append = f"{bidCode}:{bidValue}"
                            bids[bidNum] = append
                            print("BID SUCCESSFULLY CAST")
        selection = input("INPUTTING MORE BIDS? (ANYTHING FOR YES, n FOR NO) ").lower()
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

def isFloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

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