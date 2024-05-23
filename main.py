# -*- coding: utf-8 -*-

import importlib.util


spec = importlib.util.spec_from_file_location("module.name", "code/process.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)







