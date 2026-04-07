
import traceback

def faulty_function():
    return 1 / 0

try:
    faulty_function()
except ZeroDivisionError:
    traceback.print_exc()
