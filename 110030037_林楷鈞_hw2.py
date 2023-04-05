# -*- coding: UTF-8 -*-
from typing import List,TypeVar,Tuple
from datetime import datetime
import sys
import os

RECORD_TYPE_FORMAT = (str(''),int(0),str('')) # DESCRIPTION, AMOUNT ,TIME 

def check_error(string:str = '',error_message:str= '')->None: #check exceptions
    
    if not error_message:
        error_message = "Unknown error occurred !"

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

                if money_str == "cancel" : # cancel function
                    print("Canceled option, set to 0 by default")
                    return 

                self.money = int(money_str) 
                break 

            except ValueError: # error detect

                check_error(money_str,"Invalid value for money. Try again!")
            
            except : check_error("Unknown error")
            
        return 

    def add_record(self)->None:
        """Add income or expense record"""
        
        while 1:  #record input
            
            record_str  = input("Add an expense or income record with description and amount:\n")
            
            try:  #data process
                if record_str == "cancel" : # cancel function

                    print("Canceled option")

                    return 

                now = datetime.now()

                date = now.strftime("%Y-%m-%d %H:%M:%S")

                records = record_str.split(",")

                for i in range(len(records)):

                    record = records[i].split()
                    
                    record[1] = int(record[1])

                    record.append(date)

                    records[i]=tuple(record)

                break

            except IndexError: # error detect

                check_error(record_str,"The format of a record should be like this: breakfast -50. Try again !")

            except ValueError:
            
                check_error(record_str,"Invalid value for money.")

            except:

                check_error('Unknown error')


        # balance calculation
        diff = 0 

        for record in records:

            diff+=record[1]

        #update members
        self.money += diff
        self.records.extend(records)

        print("Add completed !")

        return 
    
    def view(self)->bool:

        """Print table of records and current money"""
     

        print("Here's your expense and income records:")
       
        if self.records:

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

        else:

            print ("*--No records !--*")

            
        #Print current money 
        print(f"Now you have {self.money} dollars.")
       

        return bool(self.records)

    def delete_record(self)->None: #future thoughts : make delete fomr a-b or delete a time
        """Delete income or expense record"""

        if not self.view():

            print("Nothing to delete !")

            return 
        
        while 1: # delete input
            
            delete_str = input("Which record do you want to delete ? (Enter index number)")

            try: #data process

                if delete_str == "cancel" :# cancel function

                    print("Canceled option")

                    return 

                delete_num = int(delete_str)

                if delete_num-1 < 0 : RECORD_TYPE_FORMAT[len(RECORD_TYPE_FORMAT)] # prevent list by changing negative 

                delete_diff = int(self.records[delete_num-1][1])

                del self.records[delete_num-1]

                self.money-=delete_diff #update member

                print('Delete completed !, deleted index "%d"' % delete_num)

                break 

            except ValueError: # error detect

                check_error(delete_str,"Invalid format. Fail to delete a record. Try again")
            
            except IndexError:

                check_error(delete_str,"Please enter valid index ! Try again")
            
            except: check_error("Unknown error")
            

        return 
    
    def save(self)->None:

        """save values"""

        try:
            with open('records.txt',"w") as w:
                w.write(str(self.money)+'\n')
                for record in self.records:
                    record=list(record)
                    record=list(map(str,record))
                    to_save = ('|'.join(record))+'\n'
                    w.writelines(to_save)
                w.close()

        except : check_error("Unknown error")
        
        print("Data saved !")
        
        return 
    
    def load(self)->bool:

        def read_record(record_str:str)->tuple:
            """process read data of a single record """
            record = record_str.split('|')
            for i,info in enumerate(record):
                record[i] = type(RECORD_TYPE_FORMAT[i])(info)
            
            #check if amount of element in a line fits the reading format, if not then return value error
            if len(record)!=len(RECORD_TYPE_FORMAT):int('invalid amount of record') 
            

            return tuple(record)
        
        try:

            with open('records.txt',"r") as r:
                lines = r.readlines()
                lines= list(map(lambda x:x.strip(),lines))
                self.money = int(lines.pop(0))
                
                

                for record_str in lines:
 
                    self.records.append(read_record(record_str))
                   
                    


                r.close()


        except FileNotFoundError:
            
            print('No previous record detected')

            return False
        
        except ValueError:

            print('Content invalid, deleting all contents')

            try:
                os.remove('records.txt')
            except:
                print('Error occured on deleting process.')

            return False
                
        except : 
            check_error('Unknown error')

            return False
        
        
        print("Previous data loaded ! ")
       

        return True

    def run(self)->None:

        print("Program starts")
        
        if not self.load():

            self.input_money()
        else:
            print("Welcome back!")
        
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
                sys.stderr.write("Invalid command ! Try again.\n")

        self.save()
       
        print("Program terminated") 

        return

if __name__ == '__main__' :
    mymoney=pymoney()
    mymoney.run()

        

        
        





