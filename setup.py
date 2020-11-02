import cx_Freeze

import sys
import os. path
PYTHON_INSTALL_DIR = os.path.dirname(os.path.dirname(os.__file__))
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

executables = [cx_Freeze.Executable("REL-Imp.py", base = "Win32GUI", icon="icono.ico")]

cx_Freeze.setup(
	name="REL-Imp",
	options={"build_exe": {"packages":["pygame", "numpy", "sympy", "matplotlib", "scipy", "webbrowser"],
							"include_files":["pics", "icons"]}},
	executables = executables
	)
