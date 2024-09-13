"""
Package : Pysimxrd
This package implements the physically-based simulation of Powder X-ray diffraction patterns.
It is a submodule of the WPEM package: https://github.com/WPEM
Author :
Mr. Cao Bin
Email: bcao686@connect.hkust-gz.edu.cn
"""

import importlib.util
import sys
import os
import datetime

# Display package information
now = datetime.datetime.now()
formatted_date_time = now.strftime('%Y-%m-%d %H:%M:%S')
print('='*80)
print(f"Pysimxrd: Physical Simulation of Powder X-ray Diffraction Patterns")
print(f"Author: Cao Bin, HKUST(GZ) | www.caobin.asia")
print(f"Executed on: {formatted_date_time} | Have a great day.")
print('='*80)

# Determine the base path of the Pysimxrd package
base_path = os.path.dirname(os.path.abspath(__file__))

# Construct the path of the compiled module
compiled_module_path = os.path.join(base_path, '__pycache__', 'generator.cpython-39.pyc')

# Check if the compiled module exists
if not os.path.exists(compiled_module_path):
    raise FileNotFoundError(f"The compiled module '{compiled_module_path}' was not found.")

# Load the compiled parse module
spec = importlib.util.spec_from_file_location("Pysimxrd.generator", compiled_module_path)
generator = importlib.util.module_from_spec(spec)
sys.modules["Pysimxrd.generator"] = generator
spec.loader.exec_module(generator)
