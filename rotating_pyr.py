import time
import math
point_array = [
    # pyramid
    #[[-2, -2, 3], [2, -2, 3], [2, -2, 7], "!"],
    #[[-2, -2, 3], [2, -2, 7], [-2, -2, 7], "@"],

    # Sides
    [[-2, -2, 3], [2, -2, 3], [0, 2, 5], '#'],
    [[2, -2, 3], [2, -2, 7], [0, 2, 5], "%"],
    [[2, -2, 7], [-2, -2, 7], [0, 2, 5], "!"],
    [[-2, -2, 7], [-2, -2, 3], [0, 2, 5], "."],
]

SCREEN_X_MIN = -20
SCREEN_X_MAX = 20
SCREEN_Y_MIN = -20
SCREEN_Y_MAX = 20

CLEAR_SCREEN_RATE = float(input("Enter clear screen rate (seconds, e.g., 0.1 is a good value): "))
ROTATION_RATE = float(input("Enter rotation rate (1 is moderately fast): "))
FOCUS_DISTANCE = float(input("Enter the zoom: "))
start_time = time.time()
def clear():
    try:
        time.sleep(CLEAR_SCREEN_RATE)
    except KeyboardInterrupt:
        exit(1)
    print("\033[H", end="")


def print_points(points):
    clear()
    # remove material for comparison
    #print(points)
    checking_points = [[x[0], x[1]] for x in points]
    for y in range(SCREEN_Y_MAX, SCREEN_Y_MIN - 1, -1):
        for x in range(SCREEN_X_MIN, SCREEN_X_MAX + 1, 1):
            if [x,y] in checking_points:
                fill_char = [k for k in points if x == k[0] and y == k[1]]
                print('\033[91m'+ fill_char[0][2] * 2 + '\033[0m', end='') # add two of the material at the end
            else:
                print(',,', end='')
        print()

def project_points(points):
    projected_points = []
    for triangle in points:
        if triangle[0][2] <= 0 or triangle[1][2] <= 0 or triangle[2][2] <= 0:
            continue  # Skip points behind the camera
        x1, y1, z1 = triangle[0]
        first = [x1 * FOCUS_DISTANCE / z1, y1 * FOCUS_DISTANCE / z1]
        x2, y2, z2 = triangle[1]
        second = [x2 * FOCUS_DISTANCE / z2, y2 * FOCUS_DISTANCE / z2]
        x3, y3, z3 = triangle[2]
        third = [x3 * FOCUS_DISTANCE / z3, y3 * FOCUS_DISTANCE / z3]
        projected_points.append([first, second, third, (z1 + z2 + z3) / 3, triangle[3]]) # add the average and fill material
    painted = sorted(projected_points, key=lambda x: x[3]) # painter's algorithm
    return painted

def triangle(points):
    lerped_points = set()
    for triangle_to_raster in points:
        for y in range(SCREEN_Y_MAX, SCREEN_Y_MIN - 1, -1):
            for x in range(SCREEN_X_MIN, SCREEN_X_MAX + 1, 1):
                succeeded = True # don't loop if point already looped over
                for item in lerped_points:
                    if x == item[0] and y == item[1]:
                        succeeded = False
                        break
                if not succeeded:
                    continue
                x1, y1 = triangle_to_raster[0]
                x2, y2 = triangle_to_raster[1]
                x3, y3 = triangle_to_raster[2]
                if point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):
                    lerped_points.add((x, y, triangle_to_raster[4]))
    return list(lerped_points)

def point_in_triangle(x, y, x1, y1, x2, y2, x3, y3):
    condition1 = ((y2 - y1)*(x - x1)) - ((x2 - x1)*(y - y1))
    condition2 = ((y3 - y2)*(x - x2)) - ((x3 - x2)*(y - y2))
    condition3 = ((y1 - y3)*(x - x3)) - ((x1 - x3)*(y - y3))
    if (condition1 > 0 and condition2 > 0 and condition3 > 0) or (condition1 < 0 and condition2 < 0 and condition3 < 0):
        return True
    return False

def transform_points(points):
    current_time = time.time() - start_time
    current_time *= ROTATION_RATE
    new_points = []
    for triangle_to_project in points:
        new_triangle = []
        for point in triangle_to_project:
            if len(point) != 3:
                continue
            x, y, z = point
            # translate z 3 pts back so it isnt directly at the origin
            z -= 5
            # rotation matrix lol
            x_coord = math.cos(current_time) * x  + math.sin(current_time) * z
            y_coord = y
            z_coord = -math.sin(current_time) * x + math.cos(current_time) * z + 5 # put z back
            new_triangle.append([x_coord, y_coord, z_coord])
        new_triangle.append(triangle_to_project[3]) # keep the material
        new_points.append(new_triangle)
    return new_points

def square_wave(t):
    if t % 3 > 1.5:
        k = -(t % 1.5) + 1.5
    else:
        k = t % 1.5
    return math.exp(k - 1)

while True:
    transformed_points = transform_points(point_array)
    projected_points = project_points(transformed_points)
    rasterized_points = triangle(projected_points)
    floor_array = []
    for i in range(len(rasterized_points)):
        floor_array.append([round(rasterized_points[i][0]), round(rasterized_points[i][1]), rasterized_points[i][2]]) # keep the material
    #print(floor_array)
    print_points(floor_array)
