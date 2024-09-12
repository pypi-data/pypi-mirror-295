## Installing and Using mpiPython on Debian-based Systems

### Overview
This guide outlines the steps to install and use mpiPython on Debian-based systems.

### Prerequisites
* **Debian-based system** (e.g., Ubuntu, Debian)
* **`build-essential`** package installed (provides necessary compilers and tools)
* **'mpich'** the program is made to work with this, you can either have it installed by package manager or custom compiled with '--enable-shared'
* **Python >=3.10**

### Installation Steps
1. **Install required packages:**
   ```bash
   sudo apt install build-essential mpich
   ```
2. **Install mpiPython:**
   ```bash
   pip install mpiPython
   ```
3. **Compile Library**
   ```bash
   python -m mpiPython
   ```
The last step is not technically needed, but because mpiPython will self compile the library if it is not present, running a program with a lot of nodes will have every node compile the shared library.

### Additional Notes
* **Virtual Environments:** Consider using virtual environments to isolate Python environments and avoid conflicts.

### Using mpiPython
Once installed, you can import and use mpiPython in your Python scripts:

```python
from mpiPython import MPIpy

MPI = MPIpy()
rank = MPI.Rank()
size = MPI.Size()

print("Hello from process {} out of {}".format(rank, size))
```

To run program:
```python
$mpirun -n 2 python file.py
```
