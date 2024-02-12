from classes_functions import *
import json,datetime,readline
from rlcompleter import Completer
class Shell:
    """Class that represents the shell of the system.
    It contains the main loop of the program, as well as the commands and
    users in the system.
    It's important to note that:
    * the shell is the only class that has access to the commands, users and units.
    * the shell not only executes the prompts, but validates the user's role."""

    def __init__(self):
        self.currentUser: User = None
        self.path: str = "C:/"
        
        # List of commands in the system
        Command(
            "help",
            "any",
            "help - muestra los comandos disponibles y una breve descripción de los mismos",
            """help

                Proporciona una lista de los comandos disponibles en el sistema.""",
            help,
        )

        Command(
            "man",
            "any",
            "man - muestra la descripción del comando especificado",
            """man [comando] 
                Describe el comando especificado y su uso.""",
            man,
        )

        Command(
            "login",
            "any",
            "login - inicia sesión en el sistema",
            """login 
                Inicia prompt para ingresar usuario y contraseña.""",
            login,
        )

        Command(
            "exit",
            "any",
            "exit - cierra la sesión actual",
            """exit
                
                Cierra la sesión actual y regresa al prompt de login.""",
            exit)

        Command(
            "dir",
            "any",
            "dir - lista los archivos y carpetas en la ubicación dada",
            """dir [unidad:ubicación]

                Lista los archivos y carpetas en la unidad y ubicación dadas.

                También es posible especificar los siguientes argumentos:

                * [criterio]: -LastUpdate, -creation, -range
                  Crea la lista según el criterio especificado.

                  -LastUpdate: lista los archivos y carpetas según la fecha de última modificación.
                  -creation: lista los archivos y carpetas según la fecha de creación.
                  -range: lista los archivos y carpetas según un rango de tamaño.
                          posterior a él, se especifica el rango como:
                          * min-max: intervalo de tamaño en bytes de la forma min-max.
                          * tamaño=|>|<: tamaño exacto, mayor o menor al especificado.

                          al listar con range, es posible especificar el argumento -ext para filtrar por extensión.

                * [orden]: asc o desc
                  Ordena los resultados de la lista de forma ascendente o descendente.""",
            dir,
        )
        
        Command("shu",
                "any",
                "shu - lista las unidades",
                """shu [unidad]

                Lista las unidades disponibles en el sistema""",
                shu)
        
        Command("cd",
                "any",
                "cd - cambia el directorio de trabajo",
                """ cd [path]

                Cambia el directorio de acuerdo al path indicado.

                Admite:
                 * Path absoluto - C:/a/b/...
                 * Path relativo - /a/b/...
                 * Vuelta a raíz - ..""",
                 self.cd)
        
        Command("mkdir",
                "any",
                "mkdir - crea un directorio",
                """ mkdir[nombre]

                Crea un directorio en el path actual, o de especificarse, en el path dado.

                También admite:
                 * Path relativo - /a/b/...
                 """,
                 self.mkdir)
        
        Command("rmdir",
                "any",
                "rmdir - borra un directorio",
                """ mkdir [path] [nombre]

                Borra un directorio en el path actual, o de especificarse, en el path dado.

                También admite:
                 * Path relativo - /a/b/...
                 """,
                 self.mkdir)
        
        Command("type",
                "any",
                "type - crea un archivo",
                """ type [nombre] [contenido]
                
                Crea el archivo con la extensión dada en el path actual, o de especificare,
                en el path actual.
                
                También admite:
                 * Path relativo - /a/b/...""",
                self.type)

        # User for testing purposes
        User("admin", "admin", "admin")
        
        Command("log",
                "any",
                "log - muestra el log del sistema",
                """log 
                Muestra el log del sistema""",
                Logs.print_logs)
        
        Command("clear-log",
                "any",
                "clear-log - limpia el log del sistema",
                "clear-log limpia el log del sistema y elimina su copia del sistema",
                Logs.clear_logs
                )
        Command("ls",
                "any",
                "ls - lista los archivos y carpetas en la ubicación dada",
                """ls [unidad:ubicación]

                Lista los archivos y carpetas en la unidad y ubicación dadas""",
                self.ls)


    def loop(self):
        
        readline.parse_and_bind("tab: complete")
        readline.set_completer(completation)
        # make complete with commands
        prompt = ""
        print(
            "Bienvenido a la MFShell",
            "para ver los comandos disponibles escriba help",
            sep="\n",
        )

        while True:
            # User setup
            name = ""
            if self.currentUser != None:
                name = self.currentUser.name
            else:
                name = "guest"

            # Prompt loop
            prompt = ""
            try:
                prompt = input(name + "@" + name + f":~ {self.path}$ ")
            except KeyboardInterrupt:
                exit(0)
            prompt = prompt.split(" ")

            if (
                self.currentUser == None
                and prompt[0] not in ["login", "help", "exit"]
            ):
                Logs.append(Log(" ".join(prompt),prompt[0],"no hay usuario logueado, por favor utilizar comando login"))
                print("no hay usuario logueado, por favor utilizar comando login")
                continue

            # Command role validation and execution
            if prompt[0] in Command.commands:
                command = Command.commands[prompt[0]]

                # Validate role
                if command.role != "any":
                    if self.currentUser == None:
                        print("must login to access command")
                        continue
                    elif self.currentUser.role != command.role:
                        print("user doesn't have access to command")
                        continue
                
                # Command execution if it hasn't been invalidated
                if len(prompt) > 1:
                    try:
                        command(prompt[1:])
                    except TypeError:
                        print("function doesn't take arguments")
                else:
                    # Check for login command to update current user
                    if command != Command.commands["login"]:
                        try:
                            command()
                        except TypeError:
                            print("function needs arguments")
                    else:
                        self.currentUser = login()
            else:
                Logs.append(Log(" ".join(prompt),prompt[0],"comando no encontrado"))
                print("comando no encontrado")
                            
    
# load the data from the json file and create the objects in memory
# Henry: No entiendo nada de esto, pero yo confío
    def load(self):
        Logs.load_logs()
        with open("data.json","r") as file:
            data = json.load(file)
        for unit in data["Units"]:
            unidad = Unit(unit["name"],unit["totalSize"],unit["type"])
            for folder in unit["folders"]:
                fold = Folder(folder["name"],folder["creationDate"],folder["modifyDate"])
                fol_folders,fol_files = self.loadFolder(folder)
                
                for fol in fol_folders:
                    fold.append(fol)
                for fil in fol_files:
                    fold.append(fil)                
                unidad.append(fold)   
        for user in data["Users"]:
            User(user["name"],user["password"],user["role"])
    
# load the folders and files from the json file
    def loadFolder(self,folder):
        folders = []
        files = []
        for file in folder["files"]:
                files.append(File(file["name"],file["size"],file["creationDate"],file["modifyDate"],file["extension"],file["content"]))
        for folder in folder["folders"]:
                fold = Folder(folder["name"],folder["creationDate"],folder["modifyDate"])
                folders_iter,files_iter =  self.loadFolder(folder)
                for fol in folders_iter:
                    fold.append(fol)                    
                for fil in files_iter:
                    fold.append(fil)
                folders.append(fold)
        return folders,files
    
# Functions that interact directly with the shell and its files
    def cd(self, args: list):
        # Validate args
        if len(args) == 1:
            path = args[0].lstrip("/").rstrip("/")
            # Check for paths and change shell current path
            # Check for absolute path
            if  ":" in path and self.valid_path(path):
                self.path = path
            # Check for relative path
            elif path == "..":
                if self.path != "C:/" and self.path != "C:":
                    self.path = "/".join(self.path.split("/")[:-1])
                else:
                    print("ya estas en la raiz")
                    Logs.append(Log("cd " + args[0]  ,"cd","ya estas en la raiz"))
            elif self.valid_path( join(self.path, path)):   
                self.path = join(self.path, path)

    def mkdir(self, args: list):
        if len(args) == 1:
            path = args[0]
            if not ":" in path:
                path = self.path.rstrip("/") + "/" + path.lstrip("/").rstrip("/")
            name = path.split("/")[-1]
            path = path.replace(name,"")
            
            

            if self.valid_path(path.rstrip("/")):
                                
                current_folder = Unit.units[path.split(":")[0]].childrens.head
                
                
                if path == "C:/":
                    date = datetime.datetime.now().strftime("%Y-%m-%d")
                    Unit.units[path.split(":")[0]].append(Folder(name,date,date))
                    return
                
                
                corrects = 0
                corrects_len = len(path.split("/")[1:-1]) -1
                
                for names in path.split("/")[1:-1]:
                

                    while current_folder.data.name != names:
                        current_folder = current_folder.next
                    if  corrects < corrects_len:
                        current_folder = current_folder.data.childrens.head
                        corrects += 1
                    
                
                
                date = datetime.datetime.now().strftime("%Y-%m-%d")
                fol = Folder(name,date,date)
                current_folder.data.append(fol)
            else:
                print("path invalido")
                Logs.append(Log("mkdir " + args[0]  ,"mkdir","path invalido"))
            
                
            
            


        

    def rmdir(self, args: list):
        # TODO
        ...

    def type(self, args:list):
        # TODO
        ...

    def ls(self, args:list=None):
        if args == None:
             dir([self.path])
        else:
            dir([self.path]+args)


    def valid_path(self, path:str) -> bool:
        # Get caller function
        caller = inspect.stack()[1].function

        # Add shell's path to path for validation
        if path == ".." and caller == "cd":
            return True
        elif path[1] != ":":
            path = self.path + path

        # Validate path
        # Separate unit and actual path
        try:
            unidad,path = path.split(":")
        except ValueError:
            Logs.append(Log(caller + " " + path  , caller,"path invalido"))
            print("path invalido")
            return False
        
        # Validate root folder or given path
        if path == "/":
            return True 
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
                Logs.append(Log(caller + " " + path  , caller,"directorio no encontrado"))
                return False
            else:
                return True
            
def completation(text,state):
    options = [i for i in Command.commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None