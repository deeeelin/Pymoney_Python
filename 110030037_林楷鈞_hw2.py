# -*- coding: UTF-8 -*-
from typing import List,TypeVar,Tuple
from datetime import datetime
import sys

def check_error(string:str,error_message:str)->None: #check exceptions

    if len(string)==0:
    
        sys.stderr.write("Emty input, try again !")

    else:

        sys.stderr.write(error_message)
    
    sys.stderr.write('\n')

    return 
        
class pymoney:
    def __init__(self)->None:
        """constructor"""
        self.money=0
        self.records=[]

    def input_money(self)->None:
        """Input the amount of money"""
        
        while 1: # money input
            
            money_str = input("How much money do you have ?")

            try: #data process

                self.money = int(money_str) 
                break 

            except: # error detect

                check_error(money_str,"Please enter numerical digits of money, try again !")

        return 

    def add_record(self)->None:
        """Add income or expense record"""
        
        while 1:  #record input
            
            record_str  = input("Add an expense or income record with description and amount:\n")
            
            try:  #data process

                now = datetime.now()

                date = now.strftime("%Y-%m-%d %H:%M:%S")

                records = record_str.split(",")

                for i in range(len(records)):

                    record = records[i].split()
                    
                    record[1] = int(record[1])

                    record.append(date)

                    records[i]=tuple(record)

                break

            except: # error detect

                check_error(record_str,"Please enter correct format, try again !")

        # balance calculation
        diff = 0 

        for record in records:

            diff+=record[1]

        #update members
        self.money += diff
        self.records.extend(records)

        print("Add completed !")

        return 
    
    def view(self)->None:
        """Print table of records and current money"""

        print("Here's your expense and income records:")

        Headers = ("Index","Description","Amount","Time")

        max_len=[len(i) for i in Headers] #IN_SPACES,DES_SPACES,DIFF_SPACES,TIME_SPACES

        #Print Headers
        for i in range(len(self.records)):

            record = self.records[i]

            index, description, diff ,time = i+1 , record[0] , record[1], record[2]

            tmp = (index, description, diff, time)

            for i in range(len(tmp)):
                if len(str(tmp[i])) > max_len[i]:
                    max_len[i] = len(str(tmp[i]))
        

        for i in range(len(Headers)):
            print(f'{Headers[i]:^{(max_len[i]+3)}}',end='')
        
        print()

        for i in range(len(tmp)):
            print("="*(max_len[i]+3),end='')
        print()
        
        #Print records
        for i in range(len(self.records)):

            record = self.records[i]

            index, description, diff ,time = i+1 , record[0] , record[1], record[2]

            tmp = (index, description, diff, time)

            for i in range(len(tmp)):
                print(f'{tmp[i]:<{(max_len[i]+3)}}',end='')
            print()

        for i in range(len(tmp)):
            print("="*(max_len[i]+3),end='')
        print()
        
        #Print current money 
        print(f"Now you have {self.money} dollars.")

        return 

    def delete_record(self)->None: #future thoughts : make delete fomr a-b or delete a time
        """Delete income or expense record"""

        self.view()
        
        while 1: # delete input
            
            delete_str = input("Which record do you want to delete ? (Enter index number)")

            try: #data process

                delete_num = int(delete_str)

                delete_diff = int(self.records[delete_num-1][1])

                del self.records[delete_num-1]

                self.money-=delete_diff #update member

                print('Delete completed !, deleted index "%d"' % delete_num)

                break 

            except: # error detect

                check_error(delete_str,"Please enter correct format and valid index !")

        return 

    def run(self)->None:

        self.input_money()

        while(1):

            cmd = input("What do you want to do (add / view / delete / exit)?")

            if cmd == "exit": break

            elif cmd == "add":
                self.add_record()

            elif cmd=="view":
                self.view()
            
            elif cmd == "delete":
                self.delete_record()
            else:
                print("Invalid option !")

        print("Program terminated") 

        return

if __name__ == '__main__' :
    mymoney=pymoney()
    mymoney.run()

        

        
        





