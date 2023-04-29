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
        


    
def input_money(self_money)->int:
    """Input the amount of money"""
    
    while 1: # money input
        
        money_str = input("How much money do you have ?")

        try: #data process

            if money_str == "cancel" : # cancel function
                print("Canceled option, set to 0 by default")
                return 0

            self_money = int(money_str) 
            break 

        except ValueError: # error detect

            check_error(money_str,"Invalid value for money. Try again!")
        
        except : check_error("Unknown error")
        
    return self_money

def add(self_money,self_records)->Tuple[int,List[Tuple[str,int]]]:
    """Add income or expense record"""
    
    while 1:  #record input
        
        record_str  = input("""Add some expense or income records with description and amount:
desc1 amt1, desc2 amt2, desc3 amt3, ...
""")
        
        try:  #data process
            if record_str == "cancel" : # cancel function

                print("Canceled option")

                return self_money,self_records

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
        
            check_error(record_str,"Invalid value for money. Try again !")

        except:

            check_error('Unknown error')


    # balance calculation
    diff = 0 

    for record in records:

        diff+=record[1]

    #update members
    self_money += diff
    self_records.extend(records)

    print("Add completed !")

    return self_money,self_records

def view(self_money,self_records)->bool:

    """Print table of records and current money"""
    

    print("Here's your expense and income records:")
    
    if self_records:

        Headers = ("Index","Description","Amount","Time")

        max_len=[len(i) for i in Headers] #IN_SPACES,DES_SPACES,DIFF_SPACES,TIME_SPACES

        #Print Headers
        for i in range(len(self_records)):

            record = self_records[i]

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
        for i in range(len(self_records)):

            record = self_records[i]

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
    print(f"Now you have {self_money} dollars.")
    

    return bool(self_records)

def delete(self_money,self_records)->Tuple[int,List[Tuple[str,int]]]: #future thoughts : make delete fomr a-b or delete a time
    """Delete income or expense record"""

    if not view(self_money,self_records):

        print("Nothing to delete !")

        return self_money,self_records
    
    while 1: # delete input
        
        delete_str = input("Which record do you want to delete ? (Enter index number)")

        try: #data process

            if delete_str == "cancel" :# cancel function

                print("Canceled option")

                return self_money,self_records

            delete_num = int(delete_str)

            if delete_num-1 < 0 : RECORD_TYPE_FORMAT[len(RECORD_TYPE_FORMAT)] # prevent list by changing negative 

            delete_diff = int(self_records[delete_num-1][1])

            del self_records[delete_num-1]

            self_money-=delete_diff #update member

            print('Delete completed !, deleted index "%d"' % delete_num)

            break 

        except ValueError: # error detect

            check_error(delete_str,"Invalid format. Fail to delete a record. Try again")
        
        except IndexError:

            check_error(delete_str,"Please enter valid index ! Try again")
        
        except: check_error("Unknown error")
        

    return self_money,self_records

def save(self_money,self_records)->bool:

    """save values"""

    try:
        with open('records.txt',"w") as w:
            w.write(str(self_money)+'\n')
            for record in self_records:
                record=list(record)
                record=list(map(str,record))
                to_save = ('|'.join(record))+'\n'
                w.writelines(to_save)
            w.close()

    except : 
            check_error("Unknown error")

            while (1):
                inp=input("Data unsaved, continue exit program ? (Y/N) ")

                if inp == 'Y':

                    sys.stderr.write("Data lost\n")

                    return True
                
                elif inp == 'N':

                    sys.stderr.write("Exit canceled, please fix error contents in 'records.txt'.\n")
    
                    return False
                
                
                else:
                    sys.stderr.write("Invalid option, try again\n")

    print("Data saved !")
        
    return True

def load()->Tuple[bool,int,Tuple[str,int,str]]:
    
    def read_record(record_str:str)->tuple:
        """process read data of a single record """
        record = record_str.split('|')
        for i,info in enumerate(record):
            record[i] = type(RECORD_TYPE_FORMAT[i])(info)
        
        #check if amount of element in a line fits the reading format, if not then return value error
        if len(record)!=len(RECORD_TYPE_FORMAT):int('invalid amount of record') 
        

        return tuple(record)
    
    self_money,self_records = 0,[]

    try:

        with open('records.txt',"r") as r:
            lines = r.readlines()
            lines= list(map(lambda x:x.strip(),lines))
            self_money = int(lines.pop(0))
            
            

            for record_str in lines:

                self_records.append(read_record(record_str))
                
            r.close()


    except FileNotFoundError:
        
        print('No previous record detected')

        return False,self_money,self_records
    
    except (ValueError,IndexError):

        while (1):
                inp=input("Previous data content invalid, delete previous data ? (Y/N) ")

                if inp == 'Y':
                    try:
                        os.remove('records.txt')

                        print('Previous data deleted')
                        
                    except:
                        sys.stderr.write('Error occured on deleting process.\n')

                    return False,self_money,self_records
                 
                
                elif inp == 'N':

                    sys.stderr.write("Program terminated, please fix error contents in 'records.txt'.\n")
    
                    exit(0)
                
                else:
                    sys.stderr.write("Invalid option, try again\n")
            
    except : 

        check_error('Unknown error')

        return False,self_money,self_records
    
    
    print("Previous data loaded ! ")
    

    return True,self_money,self_records

def initialize()->Tuple[int,list]:

    print("Program starts")

    loaded,self_money,self_records=load()

    if not loaded:

        self_money=input_money(self_money)
    else:
        print("Welcome back!")

    return self_money,self_records



self_money,self_records=initialize()

while(1):

    cmd = input("What do you want to do (add / view / delete / exit)?")

    if cmd == "exit": 
        if save(self_money,self_records) : break

    elif cmd == "add":
        self_money,self_records=add(self_money,self_records)

    elif cmd=="view":
        view(self_money,self_records)
    
    elif cmd == "delete":
        self_money,self_records=delete(self_money,self_records)
    else:
        sys.stderr.write("Invalid command ! Try again.\n")

print("Program terminated") 



        

        
        





