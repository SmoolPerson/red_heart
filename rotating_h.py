import time
import math
point_array = [
  [0, -17], [0, -16], [-1, -15], [1, -15], [-2, -14], [-1, -14], [1, -14], [2, -14], [-2, -13], [2, -13],
  [-3, -12], [3, -12], [-5, -11], [-4, -11], [4, -11], [5, -11], [-6, -10], [-5, -10], [5, -10], [6, -10],
  [-7, -9], [-6, -9], [6, -9], [7, -9], [-8, -8], [-7, -8], [7, -8], [8, -8], [-9, -7], [-8, -7], [8, -7], [9, -7],
  [-10, -6], [10, -6], [-11, -5], [11, -5], [-12, -4], [12, -4], [-13, -3], [13, -3], [-14, -2], [-13, -2], [13, -2], [14, -2],
  [-15, -1], [-14, -1], [14, -1], [15, -1], [-15, 0], [15, 0], [-15, 1], [15, 1], [-16, 2], [16, 2], [-16, 3], [16, 3],
  [-16, 4], [16, 4], [-16, 5], [0, 5], [16, 5], [-16, 6], [0, 6], [16, 6], [-15, 7], [-1, 7], [0, 7], [1, 7], [15, 7],
  [-15, 8], [-1, 8], [1, 8], [15, 8], [-14, 9], [-2, 9], [-1, 9], [1, 9], [2, 9], [14, 9], [-13, 10], [-3, 10], [-2, 10],
  [2, 10], [3, 10], [13, 10], [-12, 11], [-11, 11], [-5, 11], [-4, 11], [4, 11], [5, 11], [11, 11], [12, 11], [-10, 12],
  [-9, 12], [-8, 12], [-7, 12], [-6, 12], [6, 12], [7, 12], [8, 12], [9, 12], [10, 12]


]

start_time = time.time()
def clear():
    try:
        time.sleep(0.05)
    except KeyboardInterrupt:
        exit(1)
    print("\033[2J\033[H", end="")


def print_points(points):
    clear()
    for y in range(20, -21, -1):
        for x in range(-20, 21, 1):
            if [x,y] in points:
                print('\033[91m@@\033[0m', end='')
            else:
                print(',,', end='')
        print()

def transform_points(points):
    current_time = time.time() - start_time
    new_points = []
    for i in range(len(points)):
        x, y = points[i]
        # rotation matrix lol
        x_coord = math.cos(current_time) * x  - math.sin(current_time) * y
        y_coord = math.sin(current_time) * x + math.cos(current_time) * y
        # scale matrix lol
        x_coord = ((square_wave(current_time)) * x_coord)
        y_coord = ((square_wave(current_time)) * y_coord)
        new_points.append([x_coord, y_coord])
    return new_points

def square_wave(t):
    if t % 3 > 1.5:
        k = -(t % 1.5) + 1.5
    else:
        k = t % 1.5
    return math.exp(k - 1)

while True:
    new_points = transform_points(point_array)
    floor_array = []
    for i in range(len(new_points)):
        floor_array.append([round(new_points[i][0]), round(new_points[i][1])])
    print_points(floor_array)
