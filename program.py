import re
import sys
from typing import List, Union

class Point:
    def __init__(self, x : float, y : float):
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
    def __init__(self, center : Point, radius: float):
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

def load_objects(filename: str) -> List:
    objects = []
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
                    print(f"Некорректная строка пропущена: {stripped}",
                          file=sys.stderr)
    except FileNotFoundError:
        print(f"Файл '{filename}' не найден", file=sys.stderr)
        sys.exit(1)
    return objects

def print_objects(objects: List):
    for obj in objects:
        print(obj)

def main():
    if len(sys.argv) < 3:
        print("python program.py <файл> <операция>")
        print("Операции: print, count")
        sys.exit(1)

    filename = sys.argv[1]
    operation = sys.argv[2].lower()

    objects = load_objects(filename)

    if operation == "print":
        print_objects(objects)
    elif operation == "count":
        print(len(objects))
    else:
        print(f"Неизвестная операция: {operation}", file=sys.stderr)
        print("Доступные операции: print, count", file=sys.stderr)
        sys.exit(1)
    
main()