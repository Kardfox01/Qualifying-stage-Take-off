import os
import cv2
from colorama import Fore, Style, init


def error(text):
    print(f"{Fore.RED}{Style.BRIGHT}{text}")

def success(result):
    print(f"Результат: {Fore.GREEN}{Style.BRIGHT}{result}")


def task1():
    assets_path = input(f"Введите путь до ассета: ")

    if not os.path.isabs(assets_path):
        assets_path = os.path.join(os.getcwd(), assets_path)

    if not os.path.exists(assets_path):
        error("Ассета не существует!")
        return

    if not os.path.isdir(assets_path):
        error("Ассет не является папкой!")
        return

    assets = os.listdir(assets_path)
    colors = []
    for asset in assets:
        image = cv2.imread(f"{assets_path}\\{asset}")

        if image[0, 0, 0] == 255:
            colors.append("B")
        elif image[0, 0, 1] == 255:
            colors.append("G")
        elif image[0, 0, 2] == 255:
            colors.append("R")

    return "".join(colors)


if __name__ == "__main__":
    init(autoreset=True)
    scope = globals()

    task = "task" + input(f"Какое задание выполнить? ")

    if task in scope:
        success(scope[task]())
    else:
        error("Такого задания нет!")