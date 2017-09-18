class RationalNumber:
    p, q = 1, 1  # p/q

    @staticmethod
    def gcd(a, b):
        if a * b == 0:
            return 1
        while b != 0:
            a %= b
            a, b = b, a
        return a

    @staticmethod
    def lcd(a, b):
        return a // RationalNumber.gcd(a, b) * b

    def __init__(self, a = 1, b = 1):
        self.p, self.q = a, b

    def __add__(self, a):  # +
        k = self.gcd(self.q, a.q)
        return RationalNumber(self.p * a.q // k + a.p * self.q // k, self.q // k * a.q)

    def __sub__(self, a):  # -
        k = self.gcd(self.q, a.q)
        return RationalNumber(self.p * a.q // k - a.p * self.q // k, self.q // k * a.q)

    def __isub__(self, a):   # -=
        k = self.gcd(self.q, a.q)
        self.p, self.q = self.p * a.q // k - a.p * self.q // k, self.q // k * a.q

    def __mul__(self, a):
        rez = RationalNumber(self.p * a.p, a.q * self.q)
        rez.normalize()
        return rez

    def __truediv__(self, a):
        rez = RationalNumber(self.p * a.q, a.p * self.q)
        rez.normalize()
        return rez

    def normalize(self):
        if self.p * self.q != 0:
            k = RationalNumber.gcd(self.p, self.q)
            self.q //= k
            self.p //= k

    def input(self):
        self.p, self.q = map(int, input().split())


def printMatrix(matrix):
    for mstr in matrix:
        for i in mstr:
            print(i.p, end = "", sep = "")
            if i.q != 1:
                print("/", i.q, sep = "", end = "")
            print(" ", end = "", sep = "")
        print()
    print()


def solveMatrix(matrix):
    leny, lenx = len(matrix), len(matrix[0])
    used = [False]*leny
    queue = []

    # first step of algorithm
    for x in range(lenx - 1):  #
        y = -1
        for i in range(leny):
            if matrix[i][x].p != 0 and not used[i]:
                y = i
                break
        if y == -1:
            continue
        used[y] = True
        queue.append(y)

        # normalize
        for i in range(leny):
            if not used[i]:
                conNum = 1
                for j in range(lenx):
                    conNum = RationalNumber.lcd(matrix[i][j].q, conNum)
                for j in range(lenx):
                    matrix[i][j] = RationalNumber(matrix[i][j].p * (conNum // matrix[i][j].q))

        conNum = matrix[y][x].p
        for i in range(leny):
            if not used[i] and matrix[i][x].p != 0:
                conNum = RationalNumber.lcd(conNum, matrix[i][x].p)

        k = conNum // matrix[y][x].p
        for i in range(lenx):
            matrix[y][i].p *= k

        for i in range(leny):
            if not used[i] and matrix[i][x].p != 0:
                k = conNum // matrix[i][x].p
                matrix[i][x].p = 0
                for j in range(x + 1, lenx):
                    matrix[i][j].p *= k
                    matrix[i][j].p -= matrix[y][j].p

        printMatrix(matrix)

    # second step of algorithm
    for i in range(leny):
        if not used[i] and matrix[i][-1] != 0:
            return "No solutions"
    solution = []
    for c in range(len(queue)):
        y, x = queue[-(c+1)], len(queue) - c - 1
        sum = matrix[y][-1]
        for i in range(len(queue) - c, lenx - 1):
            sum = sum - matrix[y][i] * solution[-(i - len(queue) + c + 1)]
        elem = sum / matrix[y][x]    # q
        solution.append(elem)
    return solution

while True:
    exercise = input()
    if exercise == "end":
        break
    print(exercise)

    matrix = []
    matrix.append(list(map(int, input().split())))
    for i in range(1, len(matrix[0])):
        nextStr = list(map(int, input().split()))
        if len(nextStr) == 0:
            break
        matrix.append(nextStr)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = RationalNumber(matrix[i][j])

    printMatrix(matrix)

    solution = solveMatrix(matrix)
    print("Answer: ", end="", sep="")
    if solution == "No solutions" or solution == "Infinity of solutions":
        print(solution)
    else:
        solution.reverse()
        for i in range(len(solution)):
            print("x", i + 1, " = ", solution[i].p, " / ", solution[i].q, sep = "")
    print()
