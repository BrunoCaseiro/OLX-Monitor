import sys, requests, re


def priceMonitor():
    namePrice = []
    f = open("price.txt", "r")
    for line in f.readlines()[1:]:
        response = requests.get(line).text
        # grep the name of the ad from the response
        name = re.findall("(.*?)</h1>", response)[0].strip()

        # grep the price from the response
        price = str(re.findall(".pricelabel__value(.*)€", response))
        price = re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", price)

        if len(price) == 2:
            price = price[0] + "," + price[1] + "€"
        else:
            price = price[0] + "€"

        namePrice.append((name,price))
    f.close()

    fdb = open("priceDB.txt", "r")
    oldPrices = fdb.readline()
    if (str(namePrice) != oldPrices):
        print("OLD PRICES --> " + oldPrices)
        print("NEW PRICES --> " + str(namePrice))
        fdb2 = open("priceDB.txt", "w")
        fdb2.write(str(namePrice))
        fdb2.close()
    else:
        print("No price changes")

    fdb.close()
    return

def newAdMonitor():
    # SEARCH FORMAT --> https://www.olx.pt/DISTRICT/q-QUERYWORD-QUERYWORD2-QUERYWORD3/
    # Let's avoid symbols. Digits work perfectly


    namePrice = []
    f = open("query.txt", "r")
    for line in f.readlines()[1:]:
        query = line.split('"')[1::2]
        query = query[0].replace(" ", "-").strip()
        district = line.split(" ")[-1].strip()
        response = requests.get("https://www.olx.pt/" + district + "/q-" + query + "/").text
        #Gets every "strong" tag which are ad names and prices. Removes others
        x = re.findall('<strong>(.*)</strong>', response)[2:-3]
        namePrice.append([tuple(x[i:i+2]) for i in range(0, len(x), 2)])
    f.close()

    fdb = open("queryDB.txt", "r")
    oldAds = fdb.readline()
    if (str(namePrice) != oldAds):
        print("OLD ADS --> " + oldAds+"\n")
        print("NEW ADS --> " + str(namePrice))

        fdb2 = open("queryDB.txt", "w")
        fdb2.write(str(namePrice))
        fdb2.close()
    else:
        print("No new ads")

    fdb.close()
    
    return
    
    
while (True):
    print("\n\n\n")
    print("1) Check price of ads")
    print("2) Check for new ads")
    print("3) Instructions")
    print("0) Exit\n")

    c = input(">>> ")
    if(c != '1' and c != '2' and c != '0' and c != '3'):
        print("Invalid choice, quitting...")
        sys.exit(0)
    
    if (c == '0'):
        print("Quitting...")
        sys.exit()

    if(c == '1'):
        priceMonitor()
    
    if (c == '2'):
        newAdMonitor()

    if (c == '3'):
        print('This program allows you to automatically check for price changes on ads of your choice\nTo add an ad to the watchlist, please fill in the "price.txt" file\nEverytime you run the program, it will check for price changes since the last time you ran it\nObviously, when running for the first time every price will be marked as "NEW PRICE"\nYou can also add search queries in a given district or even in the entire country by filling in the "query.txt" file\nThis works in similar fashion, the program will let you know if any new ads are available (and their respective title and price) for a given search and location\nDo not use special characters in the queries and do not edit the files "priceDB.txt" and "queryDB.txt". This will lead to the program malfunctioning')


