import platform
import os

system = platform.uname()

def createfile(filename, content, extension):
    f=open(filename+extension, 'w')
    f.write(content)
    f.close()

def appendfile(filename, content, extension):
    f=open(filename+extension, 'a')
    f.write(content)
    f.close()

def readfile(filename, extension):
    f=open(filename+extension, 'r')
    print(f.read())
    f.close()

def getsys_system():
    print(system.system)

def getsys_machine():
    print(system.machine)

def getsys_processor():
    print(system.processor)

def getsys_node():
    print(system.node)

def getsys_release():
    print(system.release)

def getsys_version():
    print(system.version)

def getsysdetails():
    print(system.system)
    print(system.machine)
    print(system.processor)
    print(system.node)
    print(system.release)
    print(system.version)

def renamefile(filename_with_extension, newname_with_extension):
    os.rename(filename_with_extension, newname_with_extension)

def replacefile(current_path_to_file, new_destination_for_file):
    os.replace(current_path_to_file, new_destination_for_file)

def removefile(filename_with_extension):
    os.remove(filename_with_extension)