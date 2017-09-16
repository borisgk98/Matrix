def gcd(a, b):  # least common divisor
    while b != 0:
        a %= b
        a, b = b, a
    return a

def lcd(a, b):
    return a // gcd(a, b) * b


def solveMatrix(matrix, x, y):  # x, y - positions (x - column, y - string)
    if x == len(matrix[0]) - 1:
        for i in range(y, len(matrix)):
            if matrix[i][x] != 0:
                return False  # "No solution"
        return True  # "Have solution"
    comNum = matrix[y][x]
    for i in range(y + 1, len(matrix)):
        comNum = lcd(comNum, matrix[i][x])

    k = comNum // matrix[y][x]
    for j in range(x, len(matrix[0])):
        matrix[y][j] *= k
    for i in range(y + 1, len(matrix)):
        k = comNum // matrix[i][x]
        matrix[i][x] = 0
        for j in range(x + 1, len(matrix[0])):
            matrix[i][j] *= k
            matrix[i][j] -= matrix[y][j]

    solution = solveMatrix(matrix, x + 1, y + 1)
    if solution == False:
        return False
    if (y == len(matrix) - 1 and matrix[y][-2] == 0) or solution == "Infinite solutions":
        return "Infinite solutions"
    if solution == True:
        solution = []
    sum = matrix[y][-1]
    for i in range(x + 1, len(matrix[0]) - 1):
        sum -= matrix[y][i] * solution[-(i-x)]
    solution.append(sum / matrix[y][x])
    return solution


matrix = []
matrix.append(list(map(int, input().split())))
for i in range(1, len(matrix[0])):
    nextStr = list(map(int, input().split()))
    if len(nextStr) == 0:
        break
    matrix.append(nextStr)

solution = solveMatrix(matrix, 0, 0)
solution.reverse()
print(solution)


