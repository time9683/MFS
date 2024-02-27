from classes_functions import *
import json, datetime


class Shell:
    """Class that represents the shell of the system.
    It contains the main loop of the program, as well as the commands and
    users in the system.
    It's important to note that:
    * the shell is the only class that has access to the commands, users and units.
    * the shell not only executes the prompts, but validates the user's role."""

    def __init__(self):
        self.currentUser: User | None = None
        self.path: str = "C:/"
        self.backup_file = ""
        self.disables = []

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
            exit,
        )

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

        Command(
            "shu",
            "any",
            "shu - lista las unidades",
            """shu [unidad]

                Lista las unidades disponibles en el sistema""",
            shu,
        )

        Command(
            "cd",
            "any",
            "cd - cambia el directorio de trabajo",
            """ cd [path]

                Cambia el directorio de acuerdo al path indicado.

                Admite:
                 * Path absoluto - C:/a/b/...
                 * Path relativo - /a/b/...
                 * Vuelta a raíz - ..""",
            self.cd,
        )

        Command(
            "mkdir",
            "any",
            "mkdir - crea un directorio",
            """ mkdir [nombre]

                Crea un directorio en el path actual, o de especificarse, en el path dado.

                También admite:
                 * Path relativo - /a/b/nombre
                 """,
            self.mkdir,
        )

        Command(
            "rmdir",
            "any",
            "rmdir - borra un directorio",
            """ rmdir [nombre]

                Borra un directorio en el path actual, o de especificarse, en el path dado.

                También admite:
                 * Path relativo - /a/b/nombre
                 """,
            self.rmdir,
        )

        Command(
            "type",
            "any",
            "type - crea un archivo",
            """ type [nombre] [contenido]
                
                Crea el archivo con la extensión dada en el path actual, o de especificare,
                en el path actual.
                
                También admite:
                 * Path relativo - /a/b/nombre""",
            self.type,
        )

        # User for testing purposes
        User("admin", "admin", "admin")

        Command(
            "log",
            "any",
            "log - muestra el log del sistema",
            """log 
                Muestra el log del sistema""",
            Logs.print_logs,
        )

        Command(
            "clear-log",
            "any",
            "clear-log - limpia el log del sistema",
            "clear-log limpia el log del sistema y elimina su copia del sistema",
            Logs.clear_logs,
        )
        Command(
            "ls",
            "any",
            "ls - lista los archivos y carpetas en la ubicación dada",
            """ls [unidad:ubicación]

                Lista los archivos y carpetas en la unidad y ubicación dadas""",
            self.ls,
        )

    def loop(self):
        try:
            import readline

            readline.parse_and_bind("tab: complete")
            readline.set_completer(completation)
        except ImportError:
            print(
                "readline no esta dispobible en el sistema, no se podra usar el autocompletado"
            )
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

            if self.currentUser == None and prompt[0] not in ["login", "help", "exit"]:
                Logs.append(
                    Log(
                        " ".join(prompt),
                        prompt[0],
                        "no hay usuario logueado, por favor utilizar comando login",
                    )
                )
                print("no hay usuario logueado, por favor utilizar comando login")
                continue

            # Command role validation and execution
            if prompt[0] in Command.commands and prompt[0] not in self.disables:
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
                    command(prompt[1:])
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
                Logs.append(Log(" ".join(prompt), prompt[0], "comando no encontrado"))
                print("comando no encontrado")

    # load the data from the json file and create the objects in memory
    # Henry: No entiendo nada de esto, pero yo confío
    def load(self):
        Logs.load_logs()
        config_data = {}
        try:
            with open("config.json", "r") as configs:
                config_data = json.load(configs)
                self.backup_file = config_data["backup"]
                self.disables = config_data["disables"]
        except FileNotFoundError:
            print(
                RED,
                "no se encontro el archivo de configuracion",
                DEFAULT,
                "\nCree un archivo de configuracion con el nombre config.json y las siguientes llaves: backup, disables",
            )
            exit(1)

        try:
            with open(self.backup_file, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print(
                RED + "no se encontro el archivo de backup",
                DEFAULT,
                "\nse iniciara con un sistema vacio y se creara el archivo de backup",
            )
            unit = Unit("C", 500, "ssd")
            with open(self.backup_file, "w") as file:
                json.dump(
                    {
                        "Units": [
                            {
                                "name": "C",
                                "folders": [],
                                "type": "ssd",
                                "totalSize": 500,
                            }
                        ],
                        "Users": [],
                    },
                    file,
                )

            return

        for unit in data["Units"]:
            unidad = Unit(unit["name"], unit["totalSize"], unit["type"])
            for folder in unit["folders"]:
                fold = Folder(
                    folder["name"], folder["creationDate"], folder["modifyDate"]
                )
                fol_folders, fol_files = self.loadFolder(folder)

                for fol in fol_folders:
                    fold.append(fol)
                for fil in fol_files:
                    fold.append(fil)
                unidad.append(fold)
        for user in data["Users"]:
            User(user["name"], user["password"], user["role"])

    # load the folders and files from the json file
    def loadFolder(self, folder):
        folders = []
        files = []
        for file in folder["files"]:
            files.append(
                File(
                    file["name"],
                    file["size"],
                    file["creationDate"],
                    file["modifyDate"],
                    file["extension"],
                    file["content"],
                )
            )
        for folder in folder["folders"]:
            fold = Folder(folder["name"], folder["creationDate"], folder["modifyDate"])
            folders_iter, files_iter = self.loadFolder(folder)
            for fol in folders_iter:
                fold.append(fol)
            for fil in files_iter:
                fold.append(fil)
            folders.append(fold)
        return folders, files

    # Functions that interact directly with the shell and its files
    def cd(self, args: list):
        # Validate args
        if len(args) == 1:
            path = args[0]
            # Check for paths and change shell current path
            if path == "..":
                if self.path not in ["C:/", "D:/", "F:/"]:
                    self.path = self.path.rstrip("/")
                    self.path = "/".join(self.path.split("/")[:-1]) + "/"
                else:
                    print("ya estas en la raiz")
                    Logs.append(Log("cd " + args[0], "cd", "ya estas en la raiz"))
            # Check valid path (both absolute and relative)
            elif self.valid_path(path):
                # Absolute path
                if path[1] == ":":
                    self.path = path
                    if path[-1] != "/":
                        self.path += "/"
                # Relative path
                else:
                    self.path = join(self.path, path) + "/"
        else:
            print("argumentos invalidos")
            Logs.append(Log("cd " + args[0], "cd", "argumentos invalidos"))


    def mkdir(self, args: list):
        #  validate the arguments
        if len(args) == 1:
            #  get the path
            path = args[0]
            #  validate if the path is absolute or relative
            if path[1] != ":":
                #  join the relative path with the current path
                path = join(self.path, path.strip("/"))

            #  get the name of the folder
            names = path.split("/")
            name = names[-1]
            #  get the path without the name
            path = "/".join(names[:-1]) + "/"

            #  validate if the path is valid
            if self.valid_path(path):
                # validate if file already exists
                if self.valid_path(path + name):
                    print("el directorio ya existe")
                    Logs.append(
                        Log("mkdir " + args[0], "mkdir", "el directorio ya existe")
                    )
                    return
                
                # Create data for dir
                date = datetime.datetime.now().strftime("%Y-%m-%d")

                # Check if the path is the root
                if path == "C:/":
                    #  append the folder to the unit
                    Unit.units[path[0]].append(Folder(name, date, date))
                    #  save the current state of the system
                    self.backup()
                    return
                else:
                    folder = self.get_dir(path)
                    folder.append(Folder(name, date, date))
                    self.backup()
            else:
                print("path invalido")
                Logs.append(Log("mkdir " + args[0], "mkdir", "path invalido"))
        else:
            print("argumentos invalidos")
            Logs.append(Log("mkdir " + args[0], "mkdir", "argumentos invalidos"))


    def rmdir(self, args: list):
        #  validate the arguments
        if len(args) == 1:
            #  get the path
            path = args[0]
            #  validate if the path is absolute or relative
            if path[1] != ":":
                #  join the relative path with the current path
                path = join(self.path, path.strip("/"))

            #  get the name of the folder
            names = path.split("/")
            name = names[-1]
            #  get the path without the name
            path = "/".join(names[:-1]) + "/"

            #  validate if a path is the root
            if path == "C:/":
                # get the unit
                current_unit = Unit.units[path[0]]
                #  remove the folder from the unit
                current_unit.remove(name)
                # save the current state of the system
                self.backup()
                return

            # validate path
            if self.valid_path(path):
                current_folder = self.get_dir(path)

                #  validate if the dir is actually a folder
                if not isinstance(current_folder.data, Folder):
                    print("no es un directorio")
                    Logs.append(Log("rmdir " + args[0], "rmdir", "no es un directorio"))
                    return

                # remove the folder from the folder
                current_folder.remove(name)
                # save the current state of the system
                self.backup()
        else:
            print("argumentos invalidos")
            Logs.append(Log("rmdir " + " ".join(args), "rmdir", "argumentos invalidos"))


    def type(self, args: list):
        # validate the arguments
        if len(args) < 2:
            print("faltan argumentos")
            Logs.append(Log("type " + " ".join(args), "type", "faltan argumentos"))
            return
        #  get the path and the text
        path = args[0]
        text = " ".join(args[1:])

        #  validate if the path is absolute or relative
        if not ":" in path:
            path = join(self.path, path)

        # get the name of the file
        name = path.rstrip("/").split("/")[-1]

        # validate if a name have a extension
        if not "." in name:
            print("el archivo debe tener una extension")
            Logs.append(
                Log("type " + args[0], "type", "el archivo debe tener una extension")
            )
            return

        path = "/".join(path.split("/")[:-1]) + "/"
        name, extension = name.split(".")

        # only txt files are allowed
        if extension != "txt":
            print("solo se permiten archivos txt")
            Logs.append(Log("type " + args[0], "type", "solo se permiten archivos txt"))
            return

        if self.valid_path(path):
            # validate if file already exists
            if self.valid_path(path + "/" + name):
                print("el archivo ya existe")
                Logs.append(Log("type " + args[0], "type", "el archivo ya existe"))
                return

            # if the path is the root ,dont create the file
            if path == "C:/":
                print("no se puede crear un archivo en la raiz")
                Logs.append(
                    Log(
                        "type " + args[0],
                        "type",
                        "no se puede crear un archivo en la raiz",
                    )
                )
                return

            #  get the dir
            folder = self.get_dir(path)
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            file = File(name, len(text), date, date, extension, text)
            # append the file to the folder
            folder.data.append(file)
            #  save the current state of the system
            self.backup()


    def ls(self, args: list | None = None):
        # if the args are none, list the current path
        if args == None:
            dir([self.path])
        else:
            # list the path given
            dir([self.path] + args)


    def valid_path(self, path: str) -> bool:
        # Get caller function
        caller = inspect.stack()[1].function

        # Relative path: Add shell's path to path for validation
        if path == ".." and caller == "cd":
            return True
        elif path[1] != ":":
            path = self.path + path.strip("/")

        # Validate path
        # Separate unit and actual path
        try:
            unidad, path = path.split(":")
        except ValueError:
            Logs.append(Log(caller + " " + path, caller, "path invalido"))
            print("path invalido")
            return False

        # Validate root folder or given path
        if path == "/":
            return True
        else:
            # Get every folder name involved in path
            # /F1/F2 -> [F1, F2]
            names = path.rstrip("/").split("/")[1:]
            if len(names) < 1:
                Logs.append(
                    Log(caller + " " + path, caller, "path inválido")
                )
                return False
            
            # Iterate over the names and check for its existence over the current tree
            for i in range(len(names)):
                if i == 0:
                    current_folder = Unit.search(unidad, names[i])
                else:
                    current_folder = current_folder.data.search(names[i])

                # Checking wether the folder was found or not
                if current_folder == None:
                    break

            # Log error if path was not found, return True otherwise
            return current_folder != None


    def get_dir(self, path:str) -> Folder | File:
        """Given a path, searches every node involved along the data tree.
        This function is used after the path has been validated, so the dir
        we're looking for actually exists.

        Args:
            path (str): Node name descriptor

        Returns:
            Folder: Search result
        """
        # Getting unit and names to search per directory
        unidad, path = path.split(":")
        names = path.split("/")[1:]

        current_folder = Unit.search(unidad, names[0])

        for i in range(1, len(names)):
            current_folder = current_folder.search(names[i])

        return current_folder


    def backup(self):
        # data object to save
        data = {"Units": [], "Users": []}

        for unit in Unit.units:
            # get the unit
            unit_var: Unit = Unit.units[unit]
            #  get the folders and files
            unit_child = unit_var.childrens.head
            root = list()

            while (
                unit_child != None
                and unit_child.data != None
                and isinstance(unit_child, NodeL)
            ):
                #  get the files and folders
                folders, files = unit_child.data.to_list()
                # create the root folder
                root_fol = {
                    "name": unit_child.data.name,
                    "folders": folders,
                    "files": files,
                    "creationDate": unit_child.data.creationDate,
                    "modifyDate": unit_child.data.modifyDate,
                }
                root.append(root_fol)
                #  go to the next folder
                unit_child = unit_child.next
            # create the unit
            root_unit = {
                "name": unit_var.name,
                "folders": root,
                "type": unit_var.type,
                "totalSize": unit_var.totalSize,
            }
            #  append the unit to the data
            data["Units"].append(root_unit)
        #  get the users
        for user in User.users:
            data["Users"].append(User.users[user].__dict__)
        #  save the data
        with open(self.backup_file, "w") as file:
            json.dump(data, file)


def completation(text, state):
    options = [i for i in Command.commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None
