import re, json, inspect

OKBLUE = '\033[94m'
DEFAULT = '\033[0m'
RED = '\033[91m'

class linketList:
    def __init__(self) -> None:
        self.head = None
        pass
    
class Node:
    def __init__(self, data) -> None:
        self.data = data
        self.next = None

class Logs:
    head = None 
   
    @staticmethod
    def append(log):
        if Logs.head == None:
                Logs.head = Node(log)
        else:
            current = Logs.head
            Logs.head = Node(log)
            Logs.head.next = current
        Logs.save_logs()
            
    @staticmethod
    def print_logs():
        current = Logs.head
        while current != None:
            print(current.data)
            current = current.next
            
    @staticmethod
    def clear_logs():
        Logs.head = None
        # clear json file
        with open("logs.json", "w") as file:
            file.write("")
        
        
    @staticmethod
    def save_logs():
        # save logs in json file
        current = Logs.head
        logs = []
        while current != None:
            logs.append(current.data.__dict__)
            current = current.next
        with open("logs.json", "w") as file:
            json.dump(logs, file)
            
    @staticmethod
    def load_logs():
        # load logs from json file
        
        with open("logs.json", "r") as file:
            try:
                logs = json.load(file)
            except json.decoder.JSONDecodeError:
                return
            for log in logs:
                Logs.append(Log(log["promp"], log["command"], log["result"]))
        
            
class Log:
    def __init__(self,promp,command,result) -> None:
            self.promp = promp;
            self.command = command
            self.result = result
            
    def __str__(self):
            return f"[{self.command}] Running '{self.promp}' -> {  RED + self.result + DEFAULT}"
         
 
class File:
    """Class that represents a file in the system, including its metadata and content
    for listing and indexing purposes."""

    def __init__(self, name, size, creationDate, modifyDate, extension, content):
        self.name = name
        self.size = size  # bytes
        self.creationDate = creationDate  # timestamp
        self.modifyDate = modifyDate  # timestamp
        self.extension = extension  # txt, pdf, etc.
        self.content = content  # text, binary, etc.


class Folder:
    """Class that represents a folder in the system, including its metadata and content
    for listing and indexing purposes."""

    def __init__(self, name, creationDate, modifyDate):
        self.name = name
        self.creationDate = creationDate  # timestamp
        self.modifyDate = modifyDate  # timestamp
        self.childrens = linketList()
        self.size = 0  # bytes
   
    #  append function for files and folders
    #this function is used to add files and folders to the folder and add size to the folder
    def append(self, Element):
        if self.childrens.head == None:
            self.childrens.head = Node(Element)
            self.size += Element.size
        else:
            current = self.childrens.head
            while current.next != None:
                current = current.next
            current.next = Node(Element)
            self.size += Element.size
    
    def remove(self, name):
        current = self.childrens.head
        previous = None
        while current != None:
            if current.data.name == name:
                if previous == None:
                    self.childrens.head = current.next
                else:
                    previous.next = current.next
                self.size -= current.data.size
                return
            previous = current
            current = current.next
        print("archivo no encontrado")
    
    def to_list(self):
        current = self.childrens.head
        files = []
        folders = []
        while current != None:
            if isinstance(current.data, Folder):
                files_rec,folder_rec = current.data.to_list()
                folders.append({"name":current.data.name,"creationDate":current.data.creationDate,"modifyDate":current.data.modifyDate,"files":files_rec,"folders":folder_rec})
            else:
                files.append({"name":current.data.name,"size":current.data.size,"creationDate":current.data.creationDate,"modifyDate":current.data.modifyDate,"extension":current.data.extension,"content":current.data.content})
            current = current.next
        return files,folders


        
        


class Unit:
    """Class that represents a storage unit in the system, including its
    metadata and content for indexing purposes."""

    # Dictionary that contains all the units in the system
    units = dict()

    def __init__(self, name, totalSize,type):
        self.name = name
        self.totalSize = totalSize  # bytes
        self.freeSize = totalSize  # bytes
        self.type = type  # HDD,SSD,USB,etc.
        self.childrens = linketList()

        # Add unit to the units dictionary
        if self.name not in Unit.units:
            Unit.units[self.name] = self
            
    def append(self, Element):
        if self.childrens.head == None:
            self.childrens.head = Node(Element)
            self.freeSize -= Element.size
        else:
            current = self.childrens.head
            while current.next != None:
                current = current.next
            current.next = Node(Element)
            self.freeSize -= Element.size
            
    def remove(self, name):
        current = self.childrens.head
        previous = None
        while current != None:
            if current.data.name == name:
                if previous == None:
                    self.childrens.head = current.next
                else:
                    previous.next = current.next
                self.freeSize += current.data.size
                return
            previous = current
            current = current.next
        print("archivo no encontrado")


class Command:
    """Class that represents a command in the system, including methods to 
    explain and execute it."""

    # Dictionary that contains all the commands in the system
    commands = dict()

    def __init__(self, name, role, description, manual, call):
        self.name = name
        self.description = description  # Command's short description
        self.role = role  # Command's role restriction
        self.call = call  # Command's function
        self.manual = manual  # Command's usage explanation

        # Add command to the commands dictionary
        if self.name not in Command.commands:
            Command.commands[self.name] = self

    def __str__(self):
        return self.description

    def __call__(self, *arg):
        self.call(*arg)


class User:
    """Class that represents a user in the system for login and command access
    purposes."""

    # Dictionary that contains all the users in the system
    users = dict()

    def __init__(self, name, password, role):
        self.name = name
        self.password = password
        self.role = role

        if self.name not in User.users:
            User.users[self.name] = self

def help():
    for name in Command.commands:
        print(Command.commands[name])
    


def man(arg:list):
    # Argument validation
    if len(arg) == 1:
        if arg[0] in Command.commands:
            # Command process
            print(Command.commands[arg[0]].manual)
        else:
            print("Ninguna entrada del manual para " + arg[0])
    else:
        print("argumentos incorrectos")

def login() -> User:
    name = input("user: ")
    password = input("password: ")
    if name in User.users:
        if User.users[name].password == password:
            print("Bienvenido " + name)
            return User.users[name]
        else:
            print("password incorrecto")
    else:
        print("usuario no encontrado")

    return None

def shu():
    print("Unidad  Tipo   Total  Libre")
    for unit in Unit.units:
        # print with format
        print("{:7} {:6} {:5} {:5}".format(Unit.units[unit].name, Unit.units[unit].type, Unit.units[unit].totalSize, Unit.units[unit].freeSize))
    

def dir(arg:list) -> None:
    unidad = path = ""
    folders = list()
    files = list()

    # Get path from first argument
    try:
        unidad,path = arg[0].split(":")
    except ValueError:
        Logs.append(Log("dir " + arg[0]  ,"dir","argumentos invalidos"))
        print("argumentos invalidos")
        return
    
    # Listing files and folders
    if unidad in Unit.units:
        if path == "/" or path == "":
            currentFolder = Unit.units[unidad].childrens.head
            while currentFolder != None:
                folders.append(currentFolder.data)
                currentFolder = currentFolder.next  
        else:
            
            names = path.split("/")[1:]

            current_folder = Unit.units[unidad].childrens.head
            Numbers_or_correct_folders = 0
            for name in names:
            
                while  current_folder != None and current_folder.data.name != name:
                        current_folder = current_folder.next
                
                if(current_folder == None):
                    break
                
                
                
                if  Numbers_or_correct_folders < len(names)-1:
        
                    current_folder = current_folder.data.childrens.head
                    Numbers_or_correct_folders += 1
                    
                    
                    
            
            if current_folder == None:
                print("directorio no encontrado")
                Logs.append(Log("dir " + unidad + ":" + path  ,"dir","directorio no encontrado"))
                return
            
            current_folder = current_folder.data.childrens.head
            while current_folder != None:
                folders.append(current_folder.data)
                current_folder = current_folder.next
   
    else:
         Logs.append(Log("dir " + arg[0]  ,"dir","unidad no encontrada"))
         print("unidad no encontrada")

    # Addressing listing criteria
    # Standard listing
    if len(arg) == 1:
        # print folders
       print_childrens(folders)

    # Argument listing
    else:
        # Size sorting ascendently or descendently
        if len(arg) == 2 and arg[-1] in ["asc", "desc"]:
            # Sorting
            folders = size_sort(folders, arg[-1])
            files = size_sort(files, arg[-1])

            # Printing results
            print_childrens(folders,True)

        # Date sorting
        elif len(arg) ==2 or len(arg) == 3 and arg[-1] in ["asc", "desc"]:
            match arg[1]:
                case "-lastUpdate":
                    # order arg validation
                    if len(arg) == 3 and arg[-1] in ["asc", "desc"]:
                        folders = last_update_sort(folders, arg[-1])
                        files = last_update_sort(files, arg[-1])
                    elif len(arg) == 2:
                        folders = last_update_sort(folders, "desc")
                        files = last_update_sort(files, "desc")
                    else:
                        Logs.append(Log("dir " + unidad + ":" +  path + "-lastUpdate " + arg[-1]  ,"dir","argumentos invalidos"))
                        print("invalid arguments")
                        return

                    # print folders with modification date
                    print_childrens(folders,True)

                case "-creation":
                    # order arg validation
                    if len(arg) == 3 and arg[-1] in ["asc", "desc"]:
                        folders = creation_sort(folders, arg[-1])
                        files = creation_sort(files, arg[-1])
                    elif len(arg) == 2:
                        folders = creation_sort(folders, "desc")
                        files = creation_sort(files, "desc")
                    else:
                        print("invalid arguments")
                        return

                    # Print result with creation date
                    print_childrens(folders,True)
                case _:
                    print("invalid arguments")

        # Range sorting
        
        elif 3 <= len(arg) <= 6 and arg[1] == "-range" : 
            ext = ""            
            if len(arg) > 4:
                ext = arg[4]
                new_files = []
                for file in files:
                    if file.extension == ext:
                        new_files.append(file)
                files = new_files
            
            if len(arg) == 4 and (arg[3] == "-ext" or not( arg[3] in ["asc", "desc"])) :
                print("invalid arguments")
                return
            
                
            
            
            if re.match("^\d+-\d+$", arg[2]):
                min, max = arg[2].split("-")
                min = int(min)
                max = int(max)
                      
                # order arg validation
                if (len(arg) == 4 or len(arg) == 6) and arg[-1] in ["asc", "desc"]:
                    folders = range_sort(folders, min, max, arg[-1])
                    files = range_sort(files, min, max, arg[-1])
                else:
                    folders = range_sort(folders, min, max, "desc")
                    files = range_sort(files, min, max, "desc")

                # Printing results
                print_childrens(folders,True)

            elif re.match("^\d+(?:>|<|=)$",arg[2]):
                criteria = arg[2][-1]
                value = int(arg[2][:-1])

                # order arg validation
                if (len(arg) == 4 or len(arg)==6) and arg[-1] in ["asc", "desc"]:
                    folders = value_sort(folders, value, criteria, arg[-1])
                    files = value_sort(files, value, criteria, arg[-1])
                else:
                    folders = value_sort(folders, value, criteria, "desc")
                    files = value_sort(files, value, criteria, "desc")

                # Printing results
                print_childrens(folders,True)

            else:
                print("invalid arguments")

        else:
            print("invalid arguments")


def size_sort(ls:list, order:str) -> list:
    """Sorts folders and files based on size using quicksort"""
    if len(ls) <= 1:
        return ls
    
    pivot = ls[0]
    smaller = [x for x in ls[1:] if x.size <= pivot.size]
    greater = [x for x in ls[1:] if x.size > pivot.size]
    
    if order == 'asc':
        return size_sort(smaller, order) + [pivot] + size_sort(greater, order)
    else:
        return size_sort(greater, order) + [pivot] + size_sort(smaller, order)


def last_update_sort(ls: list, order:str) -> list:
    """Sorts folders and files based on last update using mergesort"""
    if len(ls) <= 1:
        return ls

    mid = len(ls) // 2
    left = ls[:mid]
    right = ls[mid:]

    left = last_update_sort(left, order)
    right = last_update_sort(right, order)

    return merge(left, right, order)

def merge(left: list, right: list, order: str) -> list:
    """Merges two sorted lists of files and folders based on modified date"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if (order == 'asc' and left[i].modifyDate <= right[j].modifyDate) or \
           (order == 'desc' and left[i].modifyDate >= right[j].modifyDate):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def creation_sort(ls: list, order: str) -> list:
    """Sorts folders and files based on creation date using mergesort"""
    if len(ls) <= 1:
        return ls

    mid = len(ls) // 2
    left = ls[:mid]
    right = ls[mid:]

    left = creation_sort(left, order)
    right = creation_sort(right, order)

    return merge_c(left, right, order)

def merge_c(left: list, right: list, order: str) -> list:
    """Merges two sorted lists of files and folders based on creation date"""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if (order == 'asc' and left[i].creationDate < right[j].creationDate) or \
           (order == 'desc' and left[i].creationDate > right[j].creationDate):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result



def range_sort(ls: list  , min: int, max: int, order: str) -> list:
    """Filters folders and files in given size range, then sorts using shellsort"""
    filtered = []
    for item in ls:
        size = item.size
        if min <= size <= max:
            filtered.append(item)
    filtered.sort(key=lambda x: x.size, reverse=(order == "desc"))
    return filtered


def value_sort(ls: list, value: int, criteria: str, order: str) -> list:
    filtered = []
    for item in ls:
        size = item.size
        if criteria == ">" and size > value:
            filtered.append(item)
        elif criteria == "<" and size < value:
            filtered.append(item)
        elif criteria == "=" and size == value:
            filtered.append(item)
    
    heap_sort(filtered, order)
    return filtered

def heap_sort(arr: list, order: str):
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    
    if order == "desc":
        arr.reverse()

def heapify(arr: list, n: int, i: int):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left].size > arr[largest].size:
        largest = left
    
    if right < n and arr[right].size > arr[largest].size:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)
        
        
        
def print_childrens(childrens:list,advanced:bool = False) -> None:
    text =  '' 
    if advanced:
        text += "Nombre  Creacion  Modificacion  Tamaño\n"
        
    
    
    for child in childrens:
        if isinstance(child, Folder):
            if advanced:
                text += OKBLUE + child.name + "/" + DEFAULT + " " + child.creationDate + " "  + child.modifyDate  + " " + str(child.size)   + "\n"
            else:
                text += OKBLUE + child.name + "/" + "\n"
        else:
            if advanced:
                text += DEFAULT + child.name + "." + child.extension + " " + child.creationDate + " "  + child.modifyDate  + " " + str(child.size) + "\n"
            else:
                text += DEFAULT + child.name + "." + child.extension + "\n"
    Logs.append(Log("dir unidad:/path" ,"dir",text))
    print(text + DEFAULT, end="")
    
def join(path,arg2):
     path_current = path.lstrip("/").rstrip("/")
     path_add = arg2.lstrip("/").rstrip("/")
     return path_current + "/" + path_add
    