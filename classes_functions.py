import re

OKBLUE = '\033[94m'
DEFAULT = '\033[0m'

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
        self.files = []
        self.folders = []
        self.size = 0  # bytes
   
    #  append function for files and folders
    #this function is used to add files and folders to the folder and add size to the folder
    def append(self, Element):
        if isinstance(Element, File):
            self.files.append(Element)
            self.size += Element.size
        elif isinstance(Element, Folder):
            self.folders.append(Element)
            self.size += Element.size

        
        


class Unit:
    """Class that represents a storage unit in the system, including its
    metadata and content for indexing purposes."""

    # Dictionary that contains all the units in the system
    units = dict()

    def __init__(self, name, totalSize, freeSize, type):
        self.name = name
        self.totalSize = totalSize  # bytes
        self.freeSize = freeSize  # bytes
        self.type = type  # HDD,SSD,USB,etc.
        self.folders = []

        # Add unit to the units dictionary
        if self.name not in Unit.units:
            Unit.units[self.name] = self


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
    for unit in Unit.units:
        print(unit)
    

def dir(arg:list) -> None:
    unidad = path = ""
    folders = list()
    files = list()

    # Get path from first argument
    try:
        unidad,path = arg[0].split(":")
    except ValueError:
        print("argumentos invalidos")
        return
    
    # Listing files and folders
    if unidad in Unit.units:
        if path == "/":
            for folder in Unit.units[unidad].folders:
                folders.append(folder)
        else:
            names = path.split("/")
            actual_folders = Unit.units[unidad].folders
            actual_folder = None
            Numbers_or_correct_folders = 0

            for i in range(len(names)):
                for j in range(len(actual_folders)):
                    if actual_folders[j].name == names[i]:
                        actual_folder = actual_folders[j]
                        actual_folders = actual_folder.folders
                        Numbers_or_correct_folders += 1
                        break

            if actual_folder == None or Numbers_or_correct_folders != len(names) -1:
                print("directorio no encontrado")
                return
            
            for folder in actual_folders:
                folders.append(folder)
                
            if actual_folder != None and actual_folder.files != None:
                for file in actual_folder.files:
                    files.append(file)                
    else:
         print("unidad no encontrada")

    # Addressing listing criteria
    # Standard listing
    if len(arg) == 1:
        # print folders
        for folder in folders:
            print(OKBLUE + folder.name + "/")
        # print files
        for file in files:
            print(DEFAULT+file.name + "." + file.extension)
        # delete print color
        print(DEFAULT,end="")

    # Argument listing
    else:
        # Size sorting ascendently or descendently
        if len(arg) == 2 and arg[-1] in ["asc", "desc"]:
            # Sorting
            print(arg[-1])
            folders = size_sort(folders, arg[-1])
            files = size_sort(files, arg[-1])

            # Printing results
            for folder in folders:
                print(OKBLUE + folder.name + "/: " + str(folder.size) )
            # print files
            for file in files:
                print(DEFAULT+file.name + "." + file.extension + ": " + str(file.size))
            # delete print color
            print(DEFAULT,end="")

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
                        print("invalid arguments")
                        return

                    # print folders with modification date
                    for folder in folders:
                        print(OKBLUE + folder.name + "/: " + folder.modifyDate)
                    # print files
                    for file in files:
                        print(DEFAULT+file.name + "." + file.extension + ": " + folder.modifyDate)
                    # delete print color
                    print(DEFAULT,end="")

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
                    for folder in folders:
                        print(OKBLUE + folder.name + "/: " + folder.creationDate)
                    # print files
                    for file in files:
                        print(DEFAULT+file.name + "." + file.extension + ": " + file.creationDate)
                    # delete print color
                    print(DEFAULT,end="")
                case _:
                    print("invalid arguments")

        # Range sorting
        elif 3 <= len(arg) <= 4 and arg[1] == "-range":
            # Interval sorting
            if re.match("^\d+-\d+$", arg[2]):
                min, max = arg[2].split("-")
                min = int(min)
                max = int(max)

                # order arg validation
                if len(arg) == 4 and arg[-1] in ["asc", "desc"]:
                    folders = range_sort(folders, min, max, arg[-1])
                    files = range_sort(files, min, max, arg[-1])
                else:
                    folders = range_sort(folders, min, max, "desc")
                    files = range_sort(files, min, max, "desc")

                # Printing results
                for folder in folders:
                    print(OKBLUE + folder.name + "/: " + str(folder.size) )
                # print files
                for file in files:
                    print(DEFAULT+file.name + "." + file.extension + ": " + str(file.size))
                # delete print color
                print(DEFAULT,end="")

            elif re.match("^\d+(?:>|<|=)$",arg[2]):
                criteria = arg[2][-1]
                value = int(arg[2][:-1])

                # order arg validation
                if len(arg) == 4 and arg[-1] in ["asc", "desc"]:
                    folders = value_sort(folders, value, criteria, arg[-1])
                    files = value_sort(files, value, criteria, arg[-1])
                else:
                    folders = value_sort(folders, value, criteria, "desc")
                    files = value_sort(files, value, criteria, "desc")

                # Printing results
                for folder in folders:
                    print(OKBLUE + folder.name + "/: " + str(folder.size) )
                # print files
                for file in files:
                    print(DEFAULT+file.name + "." + file.extension + ": " + str(file.size))
                # delete print color
                print(DEFAULT,end="")

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
    #TODO
    # Parse file or folder.modifyDate into timestamp
    print("validation works here too!")
    return ls

def creation_sort(ls: list, order:str) -> list:
    """Sorts folders and filed based on creation date using mergesort"""
    #TODO
    # Parse file or folder.creationDate into timestamp
    print("validation also works here!")
    return ls

def range_sort(ls: list, min: int, max: int, order:str) -> list:
    """Filters folders and files in given size range, then sorts using shellsort"""
    #TODO
    print("validation is working here too!")
    return ls


def value_sort(ls: list, value:int, criteria: str, order:str) -> list:
    """Filters folders and files based on size value, then sorts using heapsort"""
    #TODO
    print("validation is working here too yayayayay!")
    return ls