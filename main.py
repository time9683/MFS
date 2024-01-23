

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
    def __init__(self,id,name,password,role):
        self.id = id
        self.name = name
        self.password = password
        self.role = role
        self.currentFolder = "/"
        self.currentUnit = Unit.units["C"]
        
        

def help(arg):
    for command in Command.commands:
        print(command)
        
def man(arg):
    print(arg  + " " + Command.commands[arg].description)



def ls (arg):
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
    


def main():
    
    Command(2,"help","list commands","user",help)
    Command(3,"man","manual","user",man)
    Command(4,"ls","list files a directorys","user",ls)
    Command(5,"cd","change directory","user",cd)
    
    Unit(1,"C",100,50,"HDD")
    Unit(2,"D",100,50,"SSF")
    default = User(1,"user","1234","user")
    
    promp = ''
    
    while promp != "exit":
        promp =  input("user@user:~ /" + str(default.currentUnit.name) + "/" + str(default.currentFolder) + "$ ")
        promp = promp.split(" ")
        
        if promp[0] in Command.commands:
            if len(promp) > 1:
                Command.commands[promp[0]].execute(promp[1:],default)
            else:
                Command.commands[promp[0]].execute(None)
            
            
        else:
            print("command not found")
          
          

    
    ...
    
    
if __name__ == '__main__':
    main()