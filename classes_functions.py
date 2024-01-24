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

    def get_size(self):
        # Add up size of contained files in current folder and contained folders
        size = 0
        for file in self.files:
         size += file.size
        for folder in self.folders:
            size += folder.get_size()
        return  size


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

            ### TODO WARNING: Lists path even when repeated Folder1/FOlder1/Folder1/
            for i in range(len(names)):
                for j in range(len(actual_folders)):
                    if actual_folders[j].name == names[i]:
                        actual_folder = actual_folders[j]
                        actual_folders = actual_folder.folders
                        break

            if actual_folder == None:
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
            size_sort(arg[-1])
            size_sort(arg[-1])

            # Printing results
            # TODO print folders need to add folder.size
            for folder in folders:
                print(OKBLUE + folder.name + "/: " + str(folder.get_size()) )
            # print files
            for file in files:
                print(DEFAULT+file.name + "." + file.extension + ": " + file.size)
            # delete print color
            print(DEFAULT,end="")
        else:
            print("invalid arguments")


def size_sort(order):
    """Sorts folders and files based on size"""
    # Quicksort folders by size
    # Quicksort
    print("validation works")

