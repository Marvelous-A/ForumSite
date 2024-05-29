import os

ignore_pattern = ['pytest', 'pycache', 'vscode', 'block_schemas', 'data', '__init__', "test", 'get_code_from_files_to_txt']
all_py_files: os.path = []


for root, dirs, files in os.walk('.'):
    # Удаляем из списка директорий те, которые нужно игнорировать
    dirs[:] = [d for d in dirs if not any(ignore in d for ignore in ignore_pattern)]
    
    # Фильтруем файлы с расширением .py, которые не содержат паттерны для игнорирования
    for file in files:
        if file.endswith('.py') and not any(ignore in file for ignore in ignore_pattern):
            all_py_files.append(os.path.join(root, file))

all_code_project = ""
for i,file in enumerate(all_py_files):
    with open(file,'r',encoding='utf-8') as fl:
        file_name = file.split('\\')[-1] 
        all_code_project += f"Листинг Б.{i+1} - Модуль {file_name}\n{fl.read()}\n"

with open('all_code_in_txt.txt', 'w', encoding='utf-8') as fl:
    fl.write(all_code_project)