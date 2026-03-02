import circle
import square
import os

a = int(os.getenv("a"))
r = int(os.getenv("r"))

print(f"Square:\nArea: {square.area(a)}\nPerimeter: {square.perimeter(a)}\n")
print(f"Circle:\nArea: {circle.area(r)}\nPerimeter: {circle.perimeter(r)}\n")