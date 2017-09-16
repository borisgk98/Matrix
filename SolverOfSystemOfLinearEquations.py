class RationalNumber:
    q, p = 1, 1

    @staticmethod
    def gcd(a, b):
        while b != 0:
            a %= b
            a, b = b, a
        return a

    @staticmethod
    def lcd(a, b):
        return a // RationalNumber.gcd(a, b) * b

    def __init__(self, a, b):
        self.q, self.p = a, b

    def __add__(self, a):
        k = self.gcd(self.q, a.q)
        return RationalNumber(self.q * a.p // k + a.q * self.p // k, self.p // k * a.p)



# def solveMatrix(matrix):
#     leny, lenx = len(matrix), len(matrix[0])
#     used = [False]*leny
#     queue = []
#
#     # first step of algorithm
#     for x in range(lenx - 1):  #
#         y = -1
#         for i in range(leny):
#             if matrix[i][x] != 0 and not used[i]:
#                 y = i
#                 break
#         if y == -1:
#             break
#         used[y] = True
#         queue.append(y)
#
#         conNum = matrix[y][x]
#         for i in range(lenx - 1):
#             if not used[i]:
#                 conNum = lcd(conNum, matrix[i][x])   #q
#
#         k = conNum // matrix[y][x]         #q
#         for i in range(lenx):
#             matrix[y][i] *= k
#
#         for i in range(lenx - 1):
#             if not used[i]:
#                 k = conNum // matrix[i][x]   #q
#                 matrix[i][x] = 0
#                 for j in range(x + 1, lenx):
#                     matrix[i][j] *= k
#                     matrix[i][j] -= matrix[y][j]
#
#     # second step of algorithm
#     for i in range(leny):
#         if not used[i] and matrix[i][-1] != 0:
#             return "No solutions"
#     solution = []
#     for c in range(len(queue)):
#         y, x = queue[-(c+1)], len(queue) - c - 1
#         sum = matrix[y][-1]
#         for i in range(len(queue) - c, lenx - 1):
#             sum -= matrix[y][i] * solution[-(i - len(queue) + c + 1)]
#         elem = sum // matrix[y][x]
#         solution.append(elem)
#     return solution


matrix = []
matrix.append(list(map(int, input().split())))
for i in range(1, len(matrix[0])):
    nextStr = list(map(int, input().split()))
    if len(nextStr) == 0:
        break
    matrix.append(nextStr)

solution = solveMatrix(matrix)
print(matrix)
solution.reverse()
print(solution)


