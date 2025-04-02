import os
import sys

def get_path_dirs():
    path_dirs = os.environ.get("PATH", "").split(os.pathsep)
    return path_dirs

def get_exe_in_path():
    dir_exe = {}
    path_dirs = get_path_dirs()

    for directory in path_dirs:
        if os.path.isdir(directory):
            files = os.listdir(directory)
            dir_exe[directory]  = [file for file in files if os.access(os.path.join(directory, file), os.X_OK)]

    return dir_exe

def print_path_dirs():
    dirs = get_path_dirs()
    for dir in dirs:
        print(dir)

def print_exe():
    exe_dict = get_exe_in_path()
    for directory, executables in sorted(exe_dict.items()):
        print(f"{directory}:")
        print(f"\t{executables}\n")

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "dir":
            print_path_dirs()
        elif sys.argv[1] == "exe":
            print_exe()
        else:
            print("not an option use 'dir' or 'exe' ")
    else:
        print("choose: 'dir' (list directories) or 'exe' (list executables in PATH)")

if __name__ == "__main__":
    main()
