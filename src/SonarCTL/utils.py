from os import path

base_path = path.dirname(path.abspath(__file__))
base_path = path.abspath(path.join(base_path, "../.."))
print('base path', base_path)
