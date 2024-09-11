import platform
import os

system = platform.uname()

def createfile(filenamewithextension, content):
    with open(filenamewithextension, 'w') as f:
        f.write(content)
        f.close()

def appendfile(filenamewithextension, content):
    with open(filenamewithextension, 'a') as f1:
        f1.write(content)
        f1.close()

def readfile(filenamewithextension):
    with open(filenamewithextension, 'r') as f2:
        x = f2.read()
        f2.close()
        return x

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
    y = f'''System = {system.system}
    Machine = {system.machine}
    Processor = {system.processor}
    Node = {system.node}
    Release = {system.release}
    Version = {system.version}'''
    print(y)


def renamefile(filename_with_extension, newname_with_extension):
    os.rename(filename_with_extension, newname_with_extension)

def replacefile(current_path_to_file, new_destination_for_file):
    os.replace(current_path_to_file, new_destination_for_file)

def removefile(filename_with_extension):
    os.remove(filename_with_extension)