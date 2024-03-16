"""
Відсортувати файли в папці.
"""

import argparse
from pathlib import Path
from shutil import copyfile
from threading import Thread
from time import time

from logger import logger

"""
python main.py teka [-o teka_sort]

"""

parser = argparse.ArgumentParser(description='Sorting folder')
parser.add_argument("source", help="Source folder")
parser.add_argument("--output", "-o", help="Output folder", default="sort")

args = vars(parser.parse_args())

source = args.get("source") # берем назву вхідної теки з першого аргумента
output = args.get("output") # берем назву вихідної теки з другого аргумента
output_2 =output+"2" # назва вихідної теки для перевірки часу виконання без потоків

folders = []


def grabs_folder(path: Path) -> None:
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path, thr: bool) -> None:
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix
            if thr:
                new_path = output_folder / ext
            else:
                new_path = output_folder_2 / ext
            try:
                new_path.mkdir(exist_ok=True, parents=True)
                copyfile(el, new_path / el.name)
            except OSError as err:
                logger.error(err)


if __name__ == '__main__':
    base_folder = Path(source)
    output_folder = Path(output)
    output_folder_2 = Path(output_2)

    folders.append(base_folder)
    grabs_folder(base_folder)

    threads = []
    timer = time()
    for folder in folders:
        th = Thread(target=copy_file, args=(folder, True))
        th.start()
        logger.debug(f'створений потік {th.name}')
        threads.append(th)

    [th.join() for th in threads]

    print(f'Time with using thread: {round(time() - timer, 4)}')



    timer2 = time()
    for folder in folders:
        copy_file(folder,False)
    print(f'Time without using thread: {round(time() - timer2, 4)}')

    print('Можно видаляти стару папку якщо треба')
