import os
import json
OKBLUE = '\033[94m'
DEFAULT = '\033[0m'

class File:
    def __init__(self, id,name,size,creationDate,modifyDate,extension,content):
        self.id = id
        self.name = name
        self.size = size
        self.creationDate = creationDate
        self.modifyDate = modifyDate
        self.extension = extension
        self.content = content



class Folder:
    def __init__(self, id,name,creationDate,modifyDate):
        self.id = id
        self.name = name
        self.creationDate = creationDate
        self.modifyDate = modifyDate
        self.files = []
        self.folders = []
        self.size = 0


class Unit:
    units = dict()
    def __init__(self,id,name,totalSize,freeSize,type):
        self.id =id
        self.name = name
        self.totalSize = totalSize
        self.freeSize = freeSize
        self.type = type
        self.folders = []
        Unit.units[self.name] = self

class Command:
    commands = dict()
    def __init__(self,id,name,description,role,call):
        self.id = id
        self.name = name
        self.description = description
        self.role = role
        self.call = call
        Command.commands[self.name] = self
        
        
    def execute(self,arg,state=None):
        self.call(arg,state)


class User:
    users = dict()
    def __init__(self,id,name,password,role):
        self.id = id
        self.name = name
        self.password = password
        self.role = role
        self.currentFolder = None
        self.currentUnit = None
        User.users[self.name] = self
        
        

def help(arg,status):
    for command in Command.commands:
        print(command)
        
def man(arg,status):

    if len(arg) == 1:
        if arg[0] in Command.commands:
            print(Command.commands[arg[0]].description)
        else:
            print("Ninguna entrada del manual para " + arg[0])
    else:
        print("argumentos incorrectos")



def ls (arg,status):
    if  arg == None:
        print("el comando ls necesita al menos un argumento: ls [unidad]:[directorio]  ")
        return
    unidad = path = ""
    try:
        unidad,path = arg[0].split(":")
    except ValueError:
        print("argumentos invalidos")
        return
    
    
    if unidad in Unit.units:
        if path == "/":
            for folder in Unit.units[unidad].folders:
                print(OKBLUE + folder.name + "/")
        else:
            names = path.split("/")
            actual_folders = Unit.units[unidad].folders
            actual_folder = None
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
                print(OKBLUE + folder.name + "/")
                
            if actual_folder != None and actual_folder.files != None:
                for file in actual_folder.files:
                    print(DEFAULT+file.name + "." + file.extension)
    
    else:
         print("unidad no encontrada")
    # delete color of print
    print(DEFAULT,end="")
   

def cd (arg,state):
    unit_name,ubication = arg[0].split(":")
    if unit_name in Unit.units:
        unit = Unit.units[unit_name]
        if ubication == "/":
            state.currentFolder = None
            state.currentUnit = unit
        else:
            if state.currentFolder == None:
                for folder in unit.folders:
                    if folder.name == ubication:
                        state.currentFolder = folder
                        state.currentUnit = unit
                        break
            else:
                for folder in state.currentFolder.folders:
                    if folder.name == ubication:
                        state.currentFolder = folder
                        state.currentUnit = unit
                        break
    else:
        print("unidad no encontrada")
        
def mkdir(arg,state):
    if state.currentFolder == None:
        state.currentUnit.folders.append(Folder(1,arg[0],None,None))
    else:
        state.currentFolder.folders.append(Folder(1,arg[0],None,None))
    
def login(arg,state):
    user = input("user: ")
    password = input("password: ")
    if user in User.users:
        if User.users[user].password == password:
            state.currentUser = User.users[user]
            print("Bienvenido " + user)
        else:
            print("password incorrecto")
    
def exits(arg,state):
    if arg != None:
        exit(int(arg[0]))
    else:
        exit(0)
    

def ps(arg,state):
    os.system("ps")
    
    
def shut (arg,state):
    print("unidad  tipo   total   libre")
    for unit in Unit.units:
        print("{:7} {:4} {:5}gb {:5}gb".format(unit,Unit.units[unit].type,Unit.units[unit].totalSize,Unit.units[unit].freeSize))
        

def pwd (arg,state):
    if state.currentUser.currentUnit == None or state.currentUser.currentFolder == None:
        print("no hay unidad seleccionada,por lo tanto no hay directorio actual")
        return
    print(state.currentUser.currentUnit.name + state.currentUser.currentFolder.name)
    
def clear(arg,state):
    os.system("clear")

    
class Shell:
    def __init__(self):
        self.currentUser = None
        Command(1,"help","Nombre \n     help - muestra los comandos disponibles \n Uso \n     help","all",help)
        Command(2,"man", "Nombre \n     man - muestra la descripcion del comando \n Uso \n     man [comando]","all",man)
        Command(3,"login","Nombre \n     login - Inicia session en el sistema \n Uso \n     login","all",login)
        Command(4,"exit","Nombre \n     exit - Cierra el shell \n Uso \n     exit [Codigo de salida]","all",exits)
        Command(5,"ps","Nombre \n     ps - lista los procesos en ejecucion \n Uso \n     ps -[options]","all",ps)
        Command(6,"shut","Nombre \n     shut - lista las unidades disponibles \n Uso \n     shut","all",shut)
        Command(7,"pwd","muestra el directorio actual","all",pwd)
        Command(8,"ls","Nombre \n     ls - lista el contennido de los directorios \n Uso \n     ls  [options]  [UNIDAD]:[DIRECTORIOS]  ","all",ls)
        Command(9,"clear","Nombre \n     clear - limpia la pantalla \n Uso \n     clear","all",clear)
        
    
    def loop(self):
        
        print("Bienvenido a la MFShell")
        print("para ver los comandos disponibles escriba help")
        
        
        
        promp = ''
        while True:
            name = ""
            if self.currentUser != None:
                name = self.currentUser.name
            else:
                name = "guest"
            promp = ''
            try:
                promp =  input(name + "@" + name +":~ /$ ")
            except KeyboardInterrupt:
                exit(0)
            promp = promp.split(" ")
            
            if self.currentUser == None and promp[0] != "login" and promp[0] != "exit": 
                print("no hay usuario logueado, por favor utilizar comando login")
                continue
            
            
            
            if promp[0] in Command.commands:
                if len(promp) > 1:
                    Command.commands[promp[0]].execute(promp[1:],self)
                else:
                    Command.commands[promp[0]].execute(None,self)
                
                
            else:
                print("command not found")

# load the data from the json file and create the objects in memory
    def load(self):
        file = open("data.json","r")
        data = json.load(file)
        file.close()
        for unit in data["Units"]:
            unidad = Unit(unit["id"],unit["name"],unit["totalSize"],unit["freeSize"],unit["type"])
            for folder in unit["folders"]:
                fold = Folder(folder["id"],folder["name"],folder["creationDate"],folder["modifyDate"])
                fol_folders,fol_files = self.loadFolder(folder)
                fold.folders = fol_folders
                fold.files = fol_files
                unidad.folders.append(fold)   
        for user in data["Users"]:
            User(user["id"],user["name"],user["password"],user["role"])
    
# load the folders and files from the json file
    def loadFolder(self,folder):
        folders = []
        files = []
        for file in folder["files"]:
                files.append(File(file["id"],file["name"],file["size"],file["creationDate"],file["modifyDate"],file["extension"],file["content"]))
        for folder in folder["folders"]:
                fold = Folder(folder["id"],folder["name"],folder["creationDate"],folder["modifyDate"])
                folders_iter,files_iter =  self.loadFolder(folder)
                fold.folders = folders_iter
                fold.files = files_iter
                folders.append(fold)
        return folders,files
                
       
        
        
         
        

def main():
    shell = Shell()
    shell.load()
    shell.currentUser = User.users["admin"]
    shell.loop()   
          

    
    ...
    
    
if __name__ == '__main__':
    main()