PyDLL
=====

PyDLL is a Python package for compiling and packaging Python code and its dependencies into a single distributable archive. This package supports dynamically loading Python modules from those packages.

Table of Contents
-----------------

*   [Installation](#installation)
*   [Usage](#usage)
*   [License](#license)

Installation
------------

To install the `pydll` package, use the command:

    pip install pydynamiclib

or

    pip3 install pydynamiclib

Usage
-----

### Compiling and Packaging

To compile and package your Python source code into a `.pydll` file, use the following command:

    pydll /path/to/your/source_directory output_package.pydll

This command will:

1.  Compile all `.py` files in the specified source directory.
2.  Create a ZIP archive containing the compiled files and required dependencies.
NOTE: when packaging a library make all the import statments reroute to the Lib dir

### Loading a PyDLL Package

You can load a PyDLL package using the `LoadPyDLL` function:

    import pydll
    
    # Load the default __init__.py module
    module = pydll.LoadPyDLL('path_to_your_package.pydll')
    
    # Load a specific module (e.g., 'QtWidget')
    module = pydll.LoadPyDLL('path_to_your_package.pydll', specific_module='QtWidget')


### Example Usage

After installing the `pydll` package, you can run it from the command line:

    pydll /path/to/your/source_directory output_package.pydll

This will compile the Python files and package them into a `.pydll` archive.

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.