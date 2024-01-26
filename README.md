# MFS (Memory File System)

MFS is a lightweight file system implemented in memory. It provides a simple and efficient way to manage files in memory without the need to write or read  a physical disk.

## Features

- **In-memory storage**: All files and directories are stored in memory, allowing for fast read and write operations.
- **File management**: MFS supports indexing and listing files and directories.
- **Directory navigation**: Users can navigate through directories and access files using a familiar file path syntax.
- **Permissions**: MFS supports basic file permissions, allowing users to control access to their files.
- **Data save**: MFS supports saving the file system data to a file, allowing users to persist their data across sessions.

## Getting Started

To get started with MFS, follow these steps:

1. Clone the MFS repository: `git clone https://github.com/your-username/mfs.git`
2. run "python mfs.py"

## Usage

MFS supports the following commands:

- `dir`: List the contents of the current directory.
- `login`: To allow a user access to files based on his/her permission.
- `exit`: Exit the program.
- `help`: Show the help message.
