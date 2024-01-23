import os

class File:
    def __init__(self, id,name,size,creationDate,modifyDate,extension,content):
        self.id = id
        self.name = name
        self.size = size
        self.creationDate = creationDate
        self.modifyDate = modifyDate
        self.extension = extension



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
        self.currentFolder = "/"
        self.currentUnit = None
        User.users[self.name] = self
        
        

def help(arg,status):
    for command in Command.commands:
        print(command)
        
def man(arg,status):

    if len(arg) == 1:
        if arg[0] in Command.commands:
            print(arg[0]  + " " + Command.commands[arg[0]].description)
        else:
            print("Ninguna entrada del manual para " + arg[0])
    else:
        print("argumentos incorrectos")



def ls (arg,status):
    unidad = arg[0]
    ubication = arg[1]
    if unidad in Unit.units:
         print("unidad encontrada")
         if ubication == "/":
              print("raiz")
         else:
              print("no raiz")
    else:
         print("unidad no encontrada")
   

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
    exit(0)
    

def ps(arg,state):
    os.system("ps")
    
    

    
class Shell:
    def __init__(self):
        self.currentUser = None
        Command(1,"help","muestra los comandos disponibles","all",help)
        Command(2,"man","muestra la descripcion del comando","all",man)
        Command(3,"login","inicia sesion en el sistema","all",login)
        Command(4,"exit","cierra la sesion actual","all",exits)
        Command(5,"ps","muestra los procesos en ejecucion","all",ps)
        User(1,"admin","admin","admin")
        
        
    
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


def main():
    shell = Shell()
    shell.loop()   
          

    
    ...
    
    
if __name__ == '__main__':
    main()