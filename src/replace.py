import re

main = open("main.py").readlines()
new_main = ""

for line in main:
    name_module = re.findall(r'^from (\.[\.\w]+) import', line)
    if len(name_module) != 0:
        name_file = name_module[0][1:]
        with open(f"{name_file}.py", 'r') as f:
            new_main += f.read()
    else:
        new_main += line


with open("main.py", 'w') as f:
    f.write(new_main)
