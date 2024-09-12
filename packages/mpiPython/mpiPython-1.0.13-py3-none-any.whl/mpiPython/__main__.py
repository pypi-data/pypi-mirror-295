"""
File: __main__.py
Modification Date: 8/12/24
Time Modified: 1:37pm CT
Created by: Judah Nava
Last Modified By: Judah Nava
Organization: Parallel Solvit LLC and MSUM CSIS Department
"""
import os, subprocess, sys

# def find_mpich_arg(argv: list[str]):
#     for i, arg in enumerate(argv):
#         if arg.find("mpich=") != -1:
#             return i
#     return None


# # This is getting the libcode file directory
# cache = __file__[:]
# callingDirectory = os.getcwd()
# if cache.find("__main__.py") == -1:
#     print(cache)
#     print("Issue")
#     exit(-1)
# cache = cache.replace("__main__.py", "lib/libcode.c")

# if cache.find("__main__.py") != -1:
#     exit(-1)

# # this pulls the bin directory for mpich
# index = find_mpich_arg(sys.argv)
# if index is not None:
#     mpich_value = sys.argv[index].split('=')[1]
# else:
#     print("Issue3")
#     exit(-1)


# try:
#     subprocess.run([mpich_value+"mpicc", cache, "-shared", "-fPIC", "-o",callingDirectory+"/libcode.so"])
#     print("sucess")
# except PermissionError as e:
#     print("Does not have permission to access "+mpich_value+", please use sudo or root call")

def has_libcode_so(directory_path):
    file_path = os.path.join(directory_path, "libcode.so")
    if os.path.exists(file_path):
        print(f"Directory '{directory_path}' contains 'libcode.so'")
    else:
        print(f"Directory '{directory_path}' does not contain 'libcode.so'")
        load_c_libcode()

def find_mpich_arg(argv: list[str]):
    for i, arg in enumerate(argv):
        if arg.find("mpich=") != -1:
            return i
    return None

def load_c_libcode():
    cache = __file__[:]
    callingDirectory = os.getcwd()
    if cache.find("check.py") == -1:
        print(cache)
        print("Issue")
        exit(-1)
    cache = cache.replace("check.py", "lib/libcode.c")
    if cache.find("mpiPython.py") != -1:
        print("Issue2")
        exit(-1)
    index = find_mpich_arg(sys.argv)
    if index is not None:
        mpich_value = sys.argv[index].split('=')[1]
    else:
        mpich_value=""
    try:
        subprocess.run([mpich_value+"mpicc", cache, "-shared", "-fPIC", "-o",callingDirectory+"/libcode.so"])
        print("sucess")
    except PermissionError as e:
        print("Does not have permission to access "+mpich_value+", please use sudo or root call")
    except FileNotFoundError as e:
        print("It seems that mpicc was not found.")
        print("foo is not present thus needs to be compiled")
        print("please this this again with this argument: mpich=/path/to/mpich/bin/")
        print("example: python program.py mpich=~/mpich-4.2.2/bin/")
        print("example: python program.py mpich=$HOME/mpich-4.2.2/bin/")
        exit(-1)

print(os.getcwd())
has_libcode_so(os.getcwd())
