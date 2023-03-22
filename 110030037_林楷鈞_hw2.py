# -*- coding: UTF-8 -*-

import sys

# money input
while 1:
    
    money_str = input("How much money do you have ?")

    try: #data process

         money = int(money_str) 
         break 

    except: # error detect

        if len(money_str)==0:

            print("Empy input, try again")

        else:

            print("Please enter numerical digits of money, try again !")

#record input
while 1:
    
    record_str  = input(\
    """Add an expense or income record with description and amount:
desc1 amt1, desc2 amt2, desc3 amt3, ...
""")
    
    

    try: #data process

        records = record_str.split(",")

        for i in range(len(records)):

            record = records[i].split()
            
            record[-1] = int(record[-1])

            records[i]=tuple(record)

        break

    except: # error detect

        if len(record_str)==0:
        
            print("Emty input, try again !")

        else:

            print("Please enter correct format, try again !")


# balance calculation

diff = 0 

print("Here's your expense and income records:")

for record in records:

    print(record[0],record[-1])

    diff+=record[-1]

money += diff

print(f"Now you have {money} dollars.")
