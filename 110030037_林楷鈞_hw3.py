# -*- coding: UTF-8 -*-
from typing import List,TypeVar,Tuple
from datetime import datetime
import sys
import os
import ast

RECORD_TYPE_FORMAT = (str(''),str(''),int(0),str('')) # CATEGORY,DESCRIPTION, AMOUNT ,TIME 

def check_error(string:str = '',error_message:str= '')->None: #check exceptions
    """check exceptions"""
    
    if not error_message:
        error_message = "Unknown error occurred !"

    if len(string)==0:
    
        sys.stderr.write("Emty input, try again !")

    else:

        sys.stderr.write(error_message)
    
    sys.stderr.write('\n')

    return 

class Record:#
    """Represent a record."""
    def __init__(self,cat:str,des:str,val:int,time:str):
       
        self._cat = cat
        self._des = des
        self._val = val
        self._time= time

        return 

    @property
    def category(self)->str:
        return self._cat
    @property
    def description(self)->str:
        return self._des
    @property
    def amount(self)->str:
        return self._val
    @property
    def time(self)->str:
        return self._time
    
        

   
class Records:#
    """Maintain a list of all the 'Record's and the initial amount of money."""
    def __init__(self):#
        """Constructor of Records"""
    
        def input_money()->int:
            """Input the amount of money"""
            
            while 1: # money input
                
                money_str = input("How much money do you have ?")

                try: #data process

                    if money_str == "cancel" : # cancel function

                        print("Canceled option, set to 0 by default")

                        self._init_money=0

                        return 

                    self._init_money = int(money_str) 

                    break 

                except ValueError: # error detect

                    check_error(money_str,"Invalid value for money. Try again!")
                
                except : check_error("Unknown error")
                
            return 
        
        #Initialize the attributes (self._records and self._initial_money) from the file or user input.

        def load()->bool:
            """load previous contents"""
    
            def read_record(record_str:str)->Record:
                """process read data of a single record """

                record = record_str.split('|')

                for i,info in enumerate(record):

                    record[i] = type(RECORD_TYPE_FORMAT[i])(info)
                
                #check if amount of element in a line fits the reading format, if not then return value error
                if len(record)!=len(RECORD_TYPE_FORMAT):int('invalid amount of record')

                return Record(*record)

            try:

                with open('records.txt',"r") as r:
                    
                    lines = r.readlines()

                    lines= list(map(lambda x:x.strip(),lines))

                    self._init_money = int(lines.pop(0))

                    categories = lines.pop()

                    for record_str in lines:

                        self._lis.append(read_record(record_str))

                        

            except FileNotFoundError:
                
                print('No previous record detected')

                return False
            
            except (ValueError,IndexError):

                while (1):
                        inp=input("Previous data content invalid, delete previous data ? (Y/N) ")

                        if inp == 'Y':
                            try:
                                os.remove('records.txt')

                                print('Previous data deleted')
                                
                            except:
                                sys.stderr.write('Error occured on deleting process.\n')

                            return False
                        
                        
                        elif inp == 'N':

                            sys.stderr.write("Program terminated, please fix error contents in 'records.txt'.\n")
            
                            exit(0)
                        
                        else:
                            sys.stderr.write("Invalid option, try again\n")
                    
            except : 

                check_error('Unknown error')

                return False
    
    
            print("Previous data loaded ! ")
            

            return True
        

        self._init_money=0
        self._lis=[]

        print("Detecting Records")
    
        if not load(): # 1. Read from 'records.txt' or prompt for initial amount of money.

            input_money()
        else:
            print("Welcome back!")

        return
    
    def add(self,categories):#
        """Add income or expense record"""
        
        while 1:  #record input
            record_str = input('Add some expense or income records with category, description, and amount (separate by spaces):\ncat1 desc1 amt1, cat2 desc2 amt2, cat3 desc3 amt3, ...\n')
            
            try:  #data process
                if record_str == "cancel" : # cancel function

                    print("Canceled option")

                    return

                now = datetime.now()

                date = now.strftime("%Y-%m-%d %H:%M:%S")

                records = record_str.split(",")

                for i,v in enumerate(records):

                    record = records[i].split()
                    
                    record[2] = int(record[2])

                    record.append(date)

                    r = Record(*record)
                    
                    if categories.is_category_valid(r.category):

                        self._lis.append(r)
                    else:

                        sys.stderr.write("No category :",r.category,". Add record failed.\n")

                        return

                break

            except IndexError: # error detect

                check_error(record_str,"The format of a record should be like this: meal breakfast -50. Try again !")

            except ValueError:
            
                check_error(record_str,"Invalid value for money. Try again !")

            except Exception as e:
                check_error('Unknown error')


        print("Add completed !")

        return


    def view(self,cat=[]):#
        """Print table of records and current money"""

        view_lis = cat if cat else self._lis

       
        if view_lis:
            
            if cat:

                print(f"Here's your expense and income records under category \"{cat[0].category}\":")
    
            else:

                print("Here's your expense and income records:")

            Headers = ("Index","Category","Description","Amount","Time")

            max_len=[len(i) for i in Headers] #IN_SPACES,CAT_SPACES,DES_SPACES,DIFF_SPACES,TIME_SPACES

            #Print Headers
            for i,v in enumerate(view_lis):

                tmp = (i+1,v.category,v.description,v.amount,v.time)

                for i,v in enumerate(tmp):
                    
                    if len(str(v)) > max_len[i]:

                        max_len[i] = len(str(v))
            

            for i,v in enumerate(Headers):
                print(f'{v:^{(max_len[i]+3)}}',end='')
            
            print()

            for i,v in enumerate(tmp):
                print("="*(max_len[i]+3),end='')
            print()
            
            #Print records
            for i,v in enumerate(view_lis):

                tmp = (i+1,v.category,v.description,v.amount,v.time)

                for i,v in enumerate(tmp):
                    print(f'{v:<{(max_len[i]+3)}}',end='')
                print()

            for i,v in enumerate(tmp):
                print("="*(max_len[i]+3),end='')
            print()

        else:

            print ("*--No records !--*")


        #Print current money 
        if cat:

            print(f"The total amount above is {sum([i.amount for i in cat])}.")

        else:

            print(f"Now you have { self._init_money + sum([r.amount for r in self.lis])} dollars.")
        

        return bool(view_lis)
       


    def delete(self):#
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

                if delete_num-1 < 0 : raise IndexError # prevent list by changing negative 

                del self._lis[delete_num-1]

                print('Delete completed !, deleted index "%d"' % delete_num)

                break 

            except ValueError: # error detect

                check_error(delete_str,"Invalid format. Fail to delete a record. Try again")
            
            except IndexError:

                check_error(delete_str,"Please enter valid index ! Try again")
            
            except: check_error("Unknown error")
            

        return


    def find(self,categories):
        """find categories in record that is or under category"""

        category = input('Which category do you want to find? ')

        target_categories = categories.find_subcategories(category)

        target_categories_set = set(target_categories)

        to_print= list(filter(lambda x:x.category in target_categories_set,self._lis))

        if to_print:
            self.view(cat=to_print)
        else:
            print("Category record unfound")

    def save(self):
        """save values"""

        try:
            with open('records.txt',"w") as w:

                w.write(str(self._init_money)+'\n')

                for r in self._lis:

                    record=list(map(str,[r.category,r.description,r.amount,r.time]))

                    to_save = ('|'.join(record))+'\n'

                    w.writelines(to_save)

        except : 
                check_error("Unknown error")

                while (1):

                    inp=input("Record unsaved, continue exit program ? (Y/N) ")

                    if inp == 'Y':

                        sys.stderr.write("Record lost\n")

                        return True
                    
                    elif inp == 'N':

                        sys.stderr.write("Exit canceled, please fix error contents in 'records.txt'.\n")
        
                        return False
                    
                    
                    else:
                        sys.stderr.write("Invalid option, try again\n")

        print("Records saved !")
            
        return True
    
class Categories:
    """Maintain the category list and provide some methods."""
    def __init__(self):
        self._categories = []
       
        def check_category(category):
            """check if category list is valid"""
            if type(category) != list or category==[] :return False

            prev = category[0]

            if type(prev) != str : return  False
            
            for i,v in enumerate(category):

                if type(prev) == list and type(v)== list :
                    return False
                if type(v)!=str and type(v)!=list:
                    return False
                if type(v)==list:

                    if not check_category(v) : return False

                prev = v

            return True
                
        def load()->bool:
            """load previous contents"""
            try:

                with open('records.txt',"r") as r:
                    
                    lines = r.readlines()

                    lines= list(map(lambda x:x.strip(),lines))

                    category_list = lines.pop()
                
                
                
                self._categories = ast.literal_eval(category_list)
            
                if not check_category(self._categories) : raise ValueError
                    

            
            except (ValueError,SyntaxError):

                while (1):
                        inp=input("Previous category content invalid, use default category ? (Y/N) ")

                        if inp == 'Y':

                            print('Used default category')

                            return False
                        
                        
                        elif inp == 'N':

                            sys.stderr.write("Program terminated, please fix error contents in 'records.txt'.\n")
            
                            exit(0)
                        
                        else:
                            sys.stderr.write("Invalid option, try again\n")
                    
            except : 

                check_error('Unknown error, set to default')

                return False
    
    
            print("Previous category loaded ! ")
            

            return True

            
        print("Detecting Categories")
    
        if not load():

            self._categories = ['expense', ['food', ['meal', 'snack', 'drink'], 'transportation', ['bus', 'railway']], 'income', ['salary', 'bonus']]

        return
        

    def view(self,cat=[],ind=-1):
        """print out all categories in indent format"""

        if ind == -1 :
            cat = self._categories
            
            if not cat:

                print("No categories exist")

                return False

       

        if list != type(cat): print("   "*(ind+1)+"-"+cat)

        else: 

            for c in cat : self.view(c,ind+1)

        return True
    
    def add(self):
        """add new category command"""

        while 1:
            name = input("New category name :")
            if name == "cancel":

                print("Option canceled !")

                return 
            
            elif self.is_category_valid(name):

                sys.stderr.write("Category exists !, try again.\n")

            else:

                break

        while 1:
            under_category=input("Under which category ?")

            if under_category == "cancel":

                print("Option canceled !")

                return 
            
            elif under_category == "#":

                self._categories.append(name)

                break

            elif self.is_category_valid(under_category):

                self._insert(name,under_category)
                
                break

            else:
                sys.stderr.write("No such category !! Try again\n")

        print("Add completed")

        return 
    
    def delete(self):
        """Delete income or expense record"""
       
        if not self.view():

            print("Nothing to delete !")

            return
         
        while 1: # delete input
            
            delete_str = input("Which category do you want to delete ? (Enter name)")

            try: #data process

                if delete_str == "cancel" :# cancel function

                    print("Canceled option")

                    return 
                
                if not self.is_category_valid(delete_str): raise ValueError
                else:  self._prune(delete_str)

                print(f'Delete completed !, deleted category "{delete_str}"')

                break 

            except ValueError: # error detect

                check_error(delete_str,"Category doesn't exist. Try again")
            
            except: 

                check_error("Unknown error,delete failed")

                return 
        return 

                

    def _insert(self,name,under_category,cats=[]):
        """insert a new category in list"""

        if cats == []: cats = self._categories

        for i,cat in enumerate(cats) :
           
            if type(cat) == list:

                self._insert(name,under_category,cats[i])

            if cat == under_category:

                if self.find_subcategories(under_category) == [under_category]:

                    cats.insert(i+1,[name])

                else:

                    cats[i+1].append(name)
        return 
    
    def _prune(self,name,cats=[]):

        if cats == []: cats = self._categories

        for i,cat in enumerate(cats) :
           
            if type(cat) == list:

                self._prune(name,cats[i])

            if cat == name:

                if self.find_subcategories(name) == [name]:

                    del cats[i]

                else:
                    del cats[i:i+2]

        return 
    

    def is_category_valid(self,cat,cats=[])->bool:
        """is category in categories list"""
        
        if cats == []: cats = self._categories

        if type(cats) == list :

            for v in cats:
                if self.is_category_valid(cat,v) : return True

        else: return cat == cats
        

    def find_subcategories(self,cat,cats=[]):
        """return a flatten list of the category at first index , and it's subcategories """

        if cats == [] : cats = self._categories

        if type(cats) == list :

            for v in cats:
    
                p = self.find_subcategories(cat, v)

                if p == True:
        
                    index = cats.index(v)
                    
                    if index + 1 < len(cats) and type(cats[index + 1]) == list:

                        return self._flatten(cats[index:index + 2])
                    else:
                        # return only itself if no subcategories
                        return [v]
                    
                if p != []:
                    return p
        return True if cats == cat else []
    
    def _flatten(self,cats)->list:
        """flatten the nested category list"""

        total =[]

        for c in cats:

            if type(c) != list : total.append(c)

            else :  total.extend(self._flatten(c))

        return total
    
    
    def save(self):
        """save categories"""
         # 1. Write the initial money and all the records to 'records.txt'.

        try:
            with open('records.txt',"a") as a:

                a.write(str(self._categories)+'\n')

        except : 
                check_error("Unknown error")

                while (1):

                    inp=input("Categories unsaved, continue exit program ? (Y/N) ")

                    if inp == 'Y':

                        sys.stderr.write("Categories lost\n")

                        return True
                    
                    elif inp == 'N':

                        sys.stderr.write("Exit canceled, please fix error contents in 'records.txt'.\n")
        
                        return False
                    
                    
                    else:
                        sys.stderr.write("Invalid option, try again\n")

        print("Categories saved !")
            
        return True
        

    
    
    


categories = Categories()
records = Records()


while True:
    command = input('\nWhat do you want to do (add / view / delete / view categories / add categories / delete categories / find / exit)?')
    if command == 'add':
        records.add(categories)
    elif command == 'view':
        records.view()
    elif command == 'delete':
        records.delete()
    elif command == 'view categories':
        categories.view()
    elif command == "add categories":
        categories.add()
    elif command == "delete categories":
        categories.delete()
    elif command == 'find':
        records.find(categories)
    elif command == 'exit':
        if records.save() and categories.save() : break
    else:
        sys.stderr.write('Invalid command. Try again.\n')

