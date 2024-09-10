# CPPinator

CPPinator is a Python automation script designed for compiling and running multiple C++ files in a specified directory. It simplifies the process of handling multiple C++ programs and provides a clear and organized output for each program's execution along with the execution time for each program.

## CPPinator on PyPI

View the CPPinator package on PyPI [here](https://pypi.org/project/CPPinator/).

## Demonstration Video

[![CPPinator Demonstration](./video/thumbnail2.png)](https://youtu.be/qgBa7JOgGF4)

## How it works

1. The script allows you to specify a directory path where your C++ source code files are located.

2. It changes the current working directory to the specified path.

3. CPPinator lists all the C++ source code files with the `.cpp` extension in the directory.

4. For each `.cpp` file found, it compiles the code using `g++` and runs the resulting executable.

5. The script captures and displays the output and any errors produced by each program.

6. Upon successful execution of all C++ files, it provides a summary message.

7. Finally, the compiled executable file (`a.exe`) is deleted to keep your directory clean.

## Usage

1. Ensure you have Python and a C++ compiler (e.g., g++) installed on your system.

2. Install the `CPPinator` package from PyPI using pip:

   ```bash
   pip install CPPinator
   ```

   OR

   Clone or download the `CPPinator.py` script to your local machine.

   ```bash
   git clone https://github.com/Hardvan/CPPinator
   cd CPPinator
   pip install .
   ```

3. Call the `compile_and_run_cpp_files` function from the `CPPinator` package with the directory path as an argument.

   ```python
   from CPPinator import compile_and_run_cpp_files

   compile_and_run_cpp_files("path/to/your/directory")
   ```

   View the `run.py` file for an example of how to use the `CPPinator` package.

## Example Output

Here's an example of the script's output when run with a list of C++ files in the `Basic Problems` directory.

Changing working directory...
Current working directory: F:\CPPinator\Basic Problems

List of .cpp files:

1. `count_digits.cpp`
2. `divisors.cpp`
3. `gcd.cpp`
4. `palindrome_number.cpp`
5. `prime.cpp`
6. `reverse_array.cpp`
7. `reverse_number.cpp`

Running .cpp files:

1. `count_digits.cpp` (1.07s)

   No. of digits in 123456789 is:  
   9  
   9  
   9  
   Expected: 9

2. `divisors.cpp` (1.14s)

   Divisors of 100 are:  
   1 100 2 50 4 25 5 20 10  
   Divisors of 100 are:  
   1 2 4 5 10 20 25 50 100  
   Expected: 1 2 4 5 10 20 25 50 100

3. `gcd.cpp` (1.16s)

   GCD of 12 and 15 is:  
   3  
   3  
   Expected: 3

4. `palindrome_number.cpp` (1.07s)

   12321 is palindrome: true  
   Expected: true

5. `prime.cpp` (1.11s)

   100 is not prime  
   100 is not prime  
   Expected: not prime

6. `reverse_array.cpp` (1.05s)

   Original array:  
   1 2 3 4 5  
   Reversed array using two pointers:  
   5 4 3 2 1  
   Reversed array using recursion:  
   5 4 3 2 1  
   Reversed array using temporary array:  
   5 4 3 2 1  
   Expected: 5 4 3 2 1

7. `reverse_number.cpp` (1.24s)

   Reverse of 123456789 is: 987654321  
   Expected: 987654321

✅ Ran all C++ files successfully. (7.84s)

## Run the following commands to update the package (for maintainers)

1. Change version in `setup.py`
2. Run the following commands

   ```bash
   python setup.py bdist_wheel sdist
   twine check dist/*
   twine upload dist/*
   ```
