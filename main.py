# -*- coding: utf-8 -*-

import importlib.util

# processing data and dividing it
spec = importlib.util.spec_from_file_location("module.name", "code/process.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


"""
  After processing the data for LDA processing data, 
during which you can add the relevant deactivated 
words, and then word embedding, after word embedding, 
you can run the file bert.ipynb, remember to change 
the file name.
"""







