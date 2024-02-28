import re, json, inspect

OKBLUE = "\033[94m"
DEFAULT = "\033[0m"
RED = "\033[91m"


class Node:
    def __init__(self, data):
        self.data: File | Folder = data
        self.right: Node | None = None
        self.left: Node | None = None


class NodeL:
    def __init__(self, data):
        self.data: Folder = data
        self.next: NodeL | None = None


class Tree:
    def __init__(self) -> None:
        self.root: Node | None = None
        pass

    def append(self, Element):
        root = self.root
        if root == None:
            self.root = Node(Element)
        else:
            self.appendsub(Element, root)

    def appendsub(self, Element, parent):
        if parent.data.size < Element.size:
            if parent.right == None:
                parent.right = Node(Element)
            else:
                self.appendsub(Element, parent.right)

        else:
            if parent.left == None:
                parent.left = Node(Element)
            else:
                self.appendsub(Element, parent.left)

    def remove(self, name):
        self.root = self.removeNode(self.root, name)

    def removeNode(self, root: Node | None, name):
        if root == None:
            return None
        if root.left == None and root.right == None:
            if root.data.name == name:
                return None
            else:
                return root

        key_node = None
        temp = None
        last = None
        q = []
        q.append(root)
        while len(q):
            temp = q.pop(0)
            if temp.data.name == name:
                key_node = temp
            if temp.left:
                last = temp
                q.append(temp.left)
            if temp.right:
                last = temp
                q.append(temp.right)
        if key_node != None:
            x = last.data if last else None
            if last and last.left:
                if last.left.data.name == name:
                    last.left = None
                else:
                    last.right = None
            else:
                if last and last.right and last.right.data.name == name:
                    last.right = None
                else:
                    if last != None:
                        last.left = None
            key_node.data = x
        return root

    def get_list(self) -> tuple[list, list]:
        root = self.root
        folders = []
        files = []
        if root != None:
            if isinstance(root.data, Folder):
                sub_folders, sub_files = root.data.to_list()
                folders.append(
                    {
                        "name": root.data.name,
                        "size": root.data.size,
                        "creationDate": root.data.creationDate,
                        "modifyDate": root.data.modifyDate,
                        "folders": sub_folders,
                        "files": sub_files,
                    }
                )
            else:
                files.append(
                    {
                        "name": root.data.name,
                        "size": root.data.size,
                        "creationDate": root.data.creationDate,
                        "modifyDate": root.data.modifyDate,
                        "extension": root.data.extension,
                        "content": root.data.content,
                    }
                )
            if root.left != None:
                self.get_aux(root.left, folders, files)
            if root.right != None:
                self.get_aux(root.right, folders, files)

        return folders, files

    def get_aux(self, root: Node, folders, files):
        if root != None:
            if isinstance(root.data, Folder):
                sub_folders, sub_files = root.data.to_list()
                folders.append(
                    {
                        "name": root.data.name,
                        "size": root.data.size,
                        "creationDate": root.data.creationDate,
                        "modifyDate": root.data.modifyDate,
                        "folders": sub_folders,
                        "files": sub_files,
                    }
                )
            else:
                files.append(
                    {
                        "name": root.data.name,
                        "size": root.data.size,
                        "creationDate": root.data.creationDate,
                        "modifyDate": root.data.modifyDate,
                        "extension": root.data.extension,
                        "content": root.data.content,
                    }
                )
            if root.left != None:
                self.get_aux(root.left, folders, files)
            if root.right != None:
                self.get_aux(root.right, folders, files)

        return folders, files

    def search(self, data):
        return self.searchNode(self.root, data)

    def searchNode(self, root, data) -> Node | None:
        if root is None or root.data.name == data:
            return root
        result = None
        if root.left != None and data == root.left.data.name:
            return root.left
        if root.right and data == root.right.data.name:
            return root.right

        nodo = self.searchNode(root.right, data)
        if nodo != None:
            result = nodo

        nodo = self.searchNode(root.left, data)
        if nodo != None:
            result = nodo
        return result


class linketList:
    def __init__(self) -> None:
        self.head: NodeL | None = None
        pass


class Logs:
    head = None

    @staticmethod
    def append(log):
        if Logs.head == None:
            Logs.head = NodeL(log)
        else:
            current = Logs.head
            Logs.head = NodeL(log)
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
        try:
            with open("logs.json", "r") as file:
                try:
                    logs = json.load(file)
                except json.decoder.JSONDecodeError:
                    return
                for log in logs:
                    Logs.append(Log(log["promp"], log["command"], log["result"]))
        except FileNotFoundError:
            # make a logs file
            with open("logs.json", "w") as file:
                file.write("")
            return None


class Log:
    def __init__(self, promp, command, result) -> None:
        self.promp = promp
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
        self.childrens = Tree()
        self.size = 0  # bytes

    #  append function for files and folders
    # this function is used to add files and folders to the folder and add size to the folder
    def append(self, Element):
        self.childrens.append(Element)
        self.size += Element.size

    def remove(self, name):
        self.childrens.remove(name)

    def to_list(self) -> tuple[list, list]:
        return self.childrens.get_list()
        ...

    def search(self, name) -> Node | None:
        return self.childrens.search(name)


class Unit:
    """Class that represents a storage unit in the system, including its
    metadata and content for indexing purposes."""

    # Dictionary that contains all the units in the system
    units = dict()

    def __init__(self, name, totalSize, type):
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
            self.childrens.head = NodeL(Element)
            self.freeSize -= Element.size
        else:
            current = self.childrens.head
            while current.next != None:
                current = current.next
            current.next = NodeL(Element)
            self.freeSize -= Element.size

    def remove(self, name):
        current = self.childrens.head
        previous = None
        while current != None:
            if current.data != None and current.data.name == name:
                if previous == None:
                    self.childrens.head = current.next
                else:
                    previous.next = current.next
                self.freeSize += current.data.size
                return
            previous = current
            current = current.next
        print("archivo no encontrado")

    @classmethod
    def search(cls, unit, name) -> NodeL | None:
        root = Unit.units[unit].childrens.head

        # Iterate over list to find folder with given name
        while root.data.name != name:
            # Get next root as long as it exists
            if root.next != None:
                root = root.next
            # Otherwise, None
            else:
                root = None
                break

        return root


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


def man(arg: list):
    # Argument validation
    if len(arg) == 1:
        if arg[0] in Command.commands:
            # Command process
            print(Command.commands[arg[0]].manual)
        else:
            print("Ninguna entrada del manual para " + arg[0])
    else:
        print("argumentos incorrectos")


def login() -> User | None:
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
        print(
            "{:7} {:6} {:5} {:5}".format(
                Unit.units[unit].name,
                Unit.units[unit].type,
                Unit.units[unit].totalSize,
                Unit.units[unit].freeSize,
            )
        )


def dir(arg: list) -> None:
    unidad = path = ""
    folders = list()
    files = list()

    # Get path from first argument
    try:
        unidad, path = arg[0].split(":")
    except ValueError:
        Logs.append(Log("dir " + arg[0], "dir", "argumentos invalidos"))
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
            names = path.rstrip("/").split("/")[1:]

            current_folder = Unit.units[unidad].childrens.head

            while current_folder != None and current_folder.data.name != names[0]:
                current_folder = current_folder.next

            for name in names[1:]:
                current_folder = current_folder.data.search(name)

            if current_folder == None:
                print("directorio no encontrado")
                Logs.append(
                    Log("dir " + unidad + ":" + path, "dir", "directorio no encontrado")
                )
                return

            folders, files = current_folder.data.to_list()
            folders = folders + files

    else:
        Logs.append(Log("dir " + arg[0], "dir", "unidad no encontrada"))
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
            print_childrens(folders, True)

        # Date sorting
        elif len(arg) == 2 or len(arg) == 3 and arg[-1] in ["asc", "desc"]:
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
                        Logs.append(
                            Log(
                                "dir " + unidad + ":" + path + "-lastUpdate " + arg[-1],
                                "dir",
                                "argumentos invalidos",
                            )
                        )
                        print("invalid arguments")
                        return

                    # print folders with modification date
                    print_childrens(folders, True)

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
                    print_childrens(folders, True)
                case _:
                    print("invalid arguments")

        # Range sorting

        elif 3 <= len(arg) <= 6 and arg[1] == "-range":
            ext = ""
            if len(arg) > 4:
                ext = arg[4]
                new_files = []
                for file in files:
                    if file.extension == ext:
                        new_files.append(file)
                files = new_files

            if len(arg) == 4 and (arg[3] == "-ext" or not (arg[3] in ["asc", "desc"])):
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
                print_childrens(folders, True)

            elif re.match("^\d+(?:>|<|=)$", arg[2]):
                criteria = arg[2][-1]
                value = int(arg[2][:-1])

                # order arg validation
                if (len(arg) == 4 or len(arg) == 6) and arg[-1] in ["asc", "desc"]:
                    folders = value_sort(folders, value, criteria, arg[-1])
                    files = value_sort(files, value, criteria, arg[-1])
                else:
                    folders = value_sort(folders, value, criteria, "desc")
                    files = value_sort(files, value, criteria, "desc")

                # Printing results
                print_childrens(folders, True)

            else:
                print("invalid arguments")

        else:
            print("invalid arguments")


def size_sort(ls: list, order: str) -> list:
    """Sorts folders and files based on size using quicksort"""
    if len(ls) <= 1:
        return ls

    pivot = ls[0]
    smaller = [x for x in ls[1:] if x.size <= pivot.size]
    greater = [x for x in ls[1:] if x.size > pivot.size]

    if order == "asc":
        return size_sort(smaller, order) + [pivot] + size_sort(greater, order)
    else:
        return size_sort(greater, order) + [pivot] + size_sort(smaller, order)


def last_update_sort(ls: list, order: str) -> list:
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
        if (order == "asc" and left[i].modifyDate <= right[j].modifyDate) or (
            order == "desc" and left[i].modifyDate >= right[j].modifyDate
        ):
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
        if (order == "asc" and left[i].creationDate < right[j].creationDate) or (
            order == "desc" and left[i].creationDate > right[j].creationDate
        ):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def range_sort(ls: list, min: int, max: int, order: str) -> list:
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


def print_childrens(childrens: list, advanced: bool = False) -> None:
    text = ""
    if advanced:
        text += "Nombre  Creacion  Modificacion  Tamaño\n"
    for child in childrens:
        if isinstance(child, Folder):
            if advanced:
                text += (
                    OKBLUE
                    + child.name
                    + "/"
                    + DEFAULT
                    + " "
                    + child.creationDate
                    + " "
                    + child.modifyDate
                    + " "
                    + str(child.size)
                    + "\n"
                )
            else:
                text += OKBLUE + child.name + "/" + "\n"

        if not isinstance(child, Folder) and not "extension" in child:
            if advanced:
                text += (
                    OKBLUE
                    + child["name"]
                    + "/"
                    + DEFAULT
                    + " "
                    + child["creationDate"]
                    + " "
                    + child["modifyDate"]
                    + " "
                    + str(child["size"])
                    + "\n"
                )
            else:
                text += OKBLUE + child["name"] + "/" + "\n"
        elif not isinstance(child, Folder) and "extension" in child:
            if advanced:
                text += (
                    DEFAULT
                    + child["name"]
                    + "."
                    + child["extension"]
                    + " "
                    + child["creationDate"]
                    + " "
                    + child["modifyDate"]
                    + " "
                    + str(child["size"])
                    + "\n"
                )
            else:
                text += DEFAULT + child["name"] + "." + child["extension"] + "\n"
    Logs.append(Log("dir unidad:/path", "dir", text))
    print(text + DEFAULT, end="")


def join(path, arg2):
    path_current = path.strip("/")
    path_add = arg2.strip("/")
    return path_current + "/" + path_add
