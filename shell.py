from classes_functions import *

class Shell:
    """Class that represents the shell of the system.
    It contains the main loop of the program, as well as the commands and
    users in the system.
    It's important to note that:
    * the shell is the only class that has access to the commands, users and units.
    * the shell not only executes the prompts, but validates the user's role."""

    def __init__(self):
        self.currentUser: User = None

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
            """dir [unidad] [ubicación]

                Lista los archivos y carpetas en la unidad y ubicación dadas.
                Al no usar argumentos, lista las unidades disponibles.
                Al especificar [unidad], pero no [ubicación], lista las carpetas y archivos en la raíz de la unidad.

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

        # User for testing purposes
        User("admin", "admin", "admin")

    def loop(self):
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
                prompt = input(name + "@" + name + ":~ /$ ")
            except KeyboardInterrupt:
                exit(0)
            prompt = prompt.split(" ")

            if (
                self.currentUser == None
                and prompt[0] not in ["login", "help", "exit"]
            ):
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
                print("command not found")
