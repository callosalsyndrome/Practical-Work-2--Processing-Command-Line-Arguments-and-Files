import re
import sys
import os
from typing import List, Tuple, Union

class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"


class Line:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return f"Line({self.start}, {self.end})"


class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def __repr__(self):
        return f"Circle({self.center}, {self.radius})"


NUMBER = r'-?\d+(?:\.\d+)?'
POINT_PATTERN  = rf'Point\(\s*({NUMBER})\s*,\s*({NUMBER})\s*\)'
LINE_PATTERN   = rf'Line\(\s*Point\(\s*({NUMBER})\s*,\s*({NUMBER})\s*\)\s*,\s*Point\(\s*({NUMBER})\s*,\s*({NUMBER})\s*\)\s*\)'
CIRCLE_PATTERN = rf'Circle\(\s*Point\(\s*({NUMBER})\s*,\s*({NUMBER})\s*\)\s*,\s*({NUMBER})\s*\)'

RE_POINT  = re.compile(rf'^{POINT_PATTERN}$')
RE_LINE   = re.compile(rf'^{LINE_PATTERN}$')
RE_CIRCLE = re.compile(rf'^{CIRCLE_PATTERN}$')


def parse_point(s: str) -> Union[Point, None]:
    m = RE_POINT.match(s.strip())
    if not m:
        return None
    return Point(float(m.group(1)), float(m.group(2)))


def parse_line(s: str) -> Union[Line, None]:
    m = RE_LINE.match(s.strip())
    if not m:
        return None
    start = Point(float(m.group(1)), float(m.group(2)))
    end = Point(float(m.group(3)), float(m.group(4)))
    return Line(start, end)


def parse_circle(s: str) -> Union[Circle, None]:
    m = RE_CIRCLE.match(s.strip())
    if not m:
        return None
    center = Point(float(m.group(1)), float(m.group(2)))
    radius = float(m.group(3))
    return Circle(center, radius)


def parse_object(line: str) -> Union[Point, Line, Circle, None]:
    line = line.strip()
    if not line:
        return None
    if line.startswith("Point"):
        return parse_point(line)
    if line.startswith("Line"):
        return parse_line(line)
    if line.startswith("Circle"):
        return parse_circle(line)
    return None


def load_objects(filename: str) -> Tuple[List, List[str]]:
    objects = []
    bad_lines: List[str] = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                obj = parse_object(stripped)
                if obj is not None:
                    objects.append(obj)
                else:
                    bad_lines.append(stripped)
                    continue
                    
                    # print(f"Некорректная строка пропущена: {stripped}",
                    #       file=sys.stderr)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден", file=sys.stderr)
        sys.exit(1)
    return objects, bad_lines


def print_objects(objects: List):
    for obj in objects:
        print(obj)


def report_errors(bad_lines: List[str], log_path: str = "log.txt"):
    if os.path.exists(log_path):
        with open(log_path, "a", encoding="utf-8") as log:
            for line in bad_lines:
                log.write(line + "\n")
        print(f"Ошибки добавлены в существующий {log_path}",
              file=sys.stderr)
    else:
        print("Лог-файл не найден. Ошибки выводятся на экран, создаётся новый log.txt", file=sys.stderr)
        for line in bad_lines:
            print(line)
        with open(log_path, "w", encoding="utf-8") as log:
            for line in bad_lines:
                log.write(line + "\n")
        print(f"Создан новый {log_path}", file=sys.stderr)

def main():
    if len(sys.argv) < 3:
        print("python program.py <файл> <операция>")
        print("Операции: print, count, log")
        sys.exit(1)

    filename = sys.argv[1]
    operation = sys.argv[2].lower()

    objects, bad_lines = load_objects(filename)

    if operation == "--print":
        print_objects(objects)
    elif operation == "--count":
        print(len(objects))
    elif operation == "--log":
        log_path = "log.txt"
        report_errors(bad_lines, log_path)
    else:
        print(f"Неизвестная операция: {operation}", file=sys.stderr)
        print("Доступные операции: --print, --count, --log", file=sys.stderr)
        sys.exit(1)
        
main()