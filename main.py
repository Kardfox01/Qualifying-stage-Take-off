import os
import cv2
from colorama import Fore, Style, init
from numpy import fromfile, uint8


def error(text):
    print(f"{Fore.RED}{Style.BRIGHT}{text}")

def success(result):
    if result:
        print(f"Результат: {Fore.GREEN}{Style.BRIGHT}{result}")


def get_color_name(color):
    color_type = list(color).index(max(color))
    if color_type == 0:
        return "B"
    elif color_type == 1:
        return "G"
    else:
        return "R"
    

def recognize_tags(image, thresholded_image, filter_funtion, image_center_x, image_center_y):
    contours, _ = cv2.findContours(thresholded_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = list(filter(filter_funtion, contours))
    image = cv2.drawContours(image, contours, -1, (255, 255, 0), 3)

    for contour in contours:
        M = cv2.moments(contour)
        tag_center_x = int(M["m10"] / M["m00"])
        tag_center_y = int(M["m01"] / M["m00"])
        tag_name = f"{get_color_name(image[tag_center_y, tag_center_x])} ({tag_center_x - image_center_x}, {image_center_y - tag_center_y})"

        cv2.circle(image, (tag_center_x, tag_center_y), 6, (255, 255, 255), -1)
        cv2.putText(
            image,
            tag_name,
            (tag_center_x - 20, tag_center_y + 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )


def center(image):
    center_x, center_y = image.shape[1] // 2, image.shape[0] // 2
    cv2.circle(image, (center_x, center_y), 5, (100, 0, 255), -1)

    return (center_x, center_y)


def task3():
    def filter_contours(contour):
        area = cv2.contourArea(contour)
        return area > 1000 and area <= 90000

    assets_path = "Task 3/"
    asset = os.listdir(assets_path)[0]

    capture = cv2.VideoCapture(f"{assets_path}\\{asset}")
    if not capture.isOpened():
        error("Ошибка открытия видео!")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(
        f"{assets_path}\\SUCCESS_{asset}",
        fourcc,
        20.0,
        (1280, 720)
    )

    while capture.isOpened() and cv2.waitKey(25) & 0xFF != ord('q'):
        success, frame = capture.read()
        if success:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            _, thresholded_frame = cv2.threshold(gray_frame, 100, 255, 0)
            contours, _ = cv2.findContours(thresholded_frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = list(filter(filter_contours, contours))

            recognize_tags(
                frame,
                thresholded_frame,
                filter_contours,
                *center(frame)
            )

            writer.write(frame)
            cv2.imshow(asset, frame)
            continue
        break

    capture.release()
    writer.release()


def task2():
    def filter_contours(contour):
        area = cv2.contourArea(contour)
        return area > 1000 and area <= 1000000

    assets_path = "Task 2/"
    asset = os.listdir(assets_path)[0]

    image = cv2.imread(f"{assets_path}\\{asset}")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded_image = cv2.threshold(gray_image, 110, 255, 0)

    recognize_tags(
        image,
        thresholded_image,
        filter_contours,
        *center(image)
    )

    # cv2.imshow(asset, image)
    # cv2.waitKey(0)
    cv2.imwrite(f"{assets_path}\\SUCCESS_{asset}", image)


def task1():
    assets_path = input(f"Введите путь до папки: ")

    if not os.path.isabs(assets_path):
        assets_path = os.path.join(os.getcwd(), assets_path)

    if not os.path.isdir(assets_path):
        error("Путь не является папкой!")
        return

    assets = os.listdir(assets_path)
    colors = []
    for asset in assets:
        image = cv2.imdecode(fromfile(f"{assets_path}\\{asset}", dtype=uint8), cv2.IMREAD_UNCHANGED)
        colors.append(get_color_name(image[0, 0]))

    return "".join(colors)


if __name__ == "__main__":
    init(autoreset=True)
    scope = globals()

    task = "task" + input(f"Какое задание выполнить? ")

    if task in scope:
        success(scope[task]())
    else:
        error("Такого задания нет!")
