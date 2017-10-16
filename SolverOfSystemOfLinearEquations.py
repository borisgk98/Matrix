#!/usr/bin/python
import os

class RationalNumber:
    p, q = 1, 1  # p/q

    # str == a/b
    @staticmethod
    def stringToRationalNuber(str):
        a = list(map(int, str.split('/')))
        if len(a) != 2 and len(a) != 1:
            raise ValueError
        p = a[0]
        q = a[1] if len(a) == 2 else 1
        return RationalNumber(p, q)

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

    def __init__(self, a, b=1):
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

class Matrix:
    matrix = [[]]

    # изменяем матрицу как по методу Гаусса. Для квадратный получаем диагональную матрицу
    def toTriangularView(self, BySteps=False):
        leny, lenx = len(self.matrix), len(self.matrix[0])
        used = [False]*leny
        queue = []

        # ifPrinted = False
        for x in range(lenx - 1):
            y = -1
            for i in range(leny):
                if self.matrix[i][x].p != 0 and not used[i]:
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
                        conNum = RationalNumber.lcd(self.matrix[i][j].q, conNum)
                    for j in range(lenx):
                        self.matrix[i][j] = RationalNumber(self.matrix[i][j].p * (conNum // self.matrix[i][j].q))

            conNum = self.matrix[y][x].p
            for i in range(leny):
                if not used[i] and self.matrix[i][x].p != 0:
                    conNum = RationalNumber.lcd(conNum, self.matrix[i][x].p)

            k = conNum // self.matrix[y][x].p
            for i in range(lenx):
                self.matrix[y][i].p *= k

            for i in range(leny):
                if not used[i] and self.matrix[i][x].p != 0:
                    k = conNum // self.matrix[i][x].p
                    self.matrix[i][x].p = 0
                    for j in range(x + 1, lenx):
                        self.matrix[i][j].p *= k
                        self.matrix[i][j].p -= self.matrix[y][j].p

            # if ifPrinted:
            #     files[1].write("\\Rightarrow\\\\\\\\\\\\\n")
            # printMatrix(matrix)
            # ifPrinted = True

    # Так же как toTriangulsrView, только возвращает TeX строку решения по шагам
    def toTriangularView(self, BySteps=True):
        leny, lenx = len(self.matrix), len(self.matrix[0])
        used = [False]*leny
        queue = []

        strTexRez = ""
        ifPrinted = False
        for x in range(lenx - 1):
            y = -1
            for i in range(leny):
                if self.matrix[i][x].p != 0 and not used[i]:
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
                        conNum = RationalNumber.lcd(self.matrix[i][j].q, conNum)
                    for j in range(lenx):
                        self.matrix[i][j] = RationalNumber(self.matrix[i][j].p * (conNum // self.matrix[i][j].q))

            conNum = self.matrix[y][x].p
            for i in range(leny):
                if not used[i] and self.matrix[i][x].p != 0:
                    conNum = RationalNumber.lcd(conNum, self.matrix[i][x].p)

            k = conNum // self.matrix[y][x].p
            for i in range(lenx):
                self.matrix[y][i].p *= k

            for i in range(leny):
                if not used[i] and self.matrix[i][x].p != 0:
                    k = conNum // self.matrix[i][x].p
                    self.matrix[i][x].p = 0
                    for j in range(x + 1, lenx):
                        self.matrix[i][j].p *= k
                        self.matrix[i][j].p -= self.matrix[y][j].p

            if ifPrinted:
                strTexRez += ("\\Rightarrow\\\\\\\\\\\\\n")
            strTexRez += self.matrixToTex();
            ifPrinted = True
        return strTexRez

    # конструктор по матрице из RationalNumber
    def __init__(self, matrix):
        self.matrix = matrix

    # В TeX строку как матрицу
    def matrixToTex(self):
        rezStr = ""
        rezStr += "\\begin{bmatrix}\n"
        for e in range(len(self.matrix)):
            mstr = self.matrix[e]
            for el in range(len(mstr)):
                i = mstr[el]
                if i.q == 1 or i.p == 0:
                    rezStr += (str(i.p))
                else:
                    rezStr += ("\\frac{" + str(i.p) + "}{" + str(i.q) + "}")
                if el != len(mstr) - 1:
                    rezStr += (" & ")
            if e != len(self.matrix) - 1:
                rezStr += (str("\\\\ \n"))

        rezStr += (str("\\end{bmatrix}"))
        return rezStr

    # В TeX строку как систему
    def matrixToTexSystem(self):
        rezStr = ""
        rezStr += ("\\begin{cases}\n")
        for e in range(len(self.matrix)):
            mstr = self.matrix[e]
            for el in range(len(mstr) - 1):
                if el != 0:
                    if i.p >= 0:
                        rezStr += (" + ")
                    else:
                        rezStr += (" - ")
                i = mstr[el]
                if abs(i.p) != 1:
                    if i.q == 1 or i.p == 0:
                        rezStr += (str(abs(i.p)))
                    else:
                        rezStr += ("\\frac{" + str(abs(i.p)) + "}{" + str(i.q) + "}")
                rezStr += ("x_" + str(el + 1))
            rezStr += (" = ")
            if i.q == 1 or i.p == 0:
                rezStr += (str(mstr[-1].p))
            else:
                rezStr += ("\\frac{" + str(mstr[-1].p) + "}{" + str(mstr[-1].q) + "}")
            if e != len(self.matrix) - 1:
                rezStr += (str("\\\\ \n"))
        rezStr += (str("\\end{cases}"))
        return rezStr

    # Решить матрцу как систему по методу Гаусса
    def solveMatrixAsSystem(self, method="Gauss", BySteps=True):
        leny, lenx = len(self.matrix), len(self.matrix[0])
        used = [False]*leny
        queue = []

        # приводим в треугольный вид
        stepsStr = self.toTriangularView(BySteps)

        # second step of algorithm
        for i in range(leny):
            if not used[i] and self.matrix[i][-1].p != 0:
                return "No solutions"
        if len(queue) != len(self.matrix[0]) - 1:
            return "Infinity of solutions"
        solution = []
        for c in range(len(queue)):
            y, x = queue[-(c+1)], len(queue) - c - 1
            sum = self.matrix[y][-1]
            for i in range(len(queue) - c, lenx - 1):
                sum = sum - self.matrix[y][i] * solution[-(i - len(queue) + c + 1)]
            elem = sum / self.matrix[y][x]
            solution.append(elem)
        return solution, stepsStr

class InputError(Exception):
    pass

# main section

# file read/write
rezFileName = "solutionOfSystemOfLinearEquations"
files = [open("input.txt", "r"), open(rezFileName + ".tex", "w")]

# generate TeX
texStr = "\\documentclass[14pt]{article}\n" \
         "\\textwidth=175mm\n" \
         "\\textheight=260mm\n" \
        "\\oddsidemargin=-.4mm\n" \
        "\\headsep=5mm\n" \
        "\\topmargin=-1in\n" \
        "\\unitlength=1mm\n" \
         "\\usepackage{amsmath}\n" \
         "%opening\n" \
         "\\title{Solutions of systems of linear equations}\n" \
         "\\author{Boris Kozhukhovskiy, ITIS, group 704}\n" \
         "\\begin{document}\n" \
         "\\maketitle\n" \
         "\\begin{enumerate}\n"
files[1].write(texStr)

# solver
while True:
    exercise = files[0].readline()
    if exercise == "end":
        break

    # generate
    texStr = "\\item\n\\textbf{" + exercise + "}" + "\n"
    files[1].write(texStr)

    matrix = []
    matrix.append(list(map(RationalNumber.stringToRationalNuber, files[0].readline().split())))
    for i in range(1, len(matrix[0])):
        nextMatixStr = list(map(RationalNumber.stringToRationalNuber, files[0].readline().split()))
        if (len(nextMatixStr) != len(matrix[0])):
            raise InputError("Bad matrix string")
        if len(nextMatixStr) == 0:
            break
        matrix.append(nextMatixStr)

    matrix = Matrix(matrix)

    # print Data
    files[1].write("\\\\Data:\\\\\\\\\\\n$\n")
    files[1].write(matrix.matrixToTexSystem())
    files[1].write("$\\\\\n")

    # check for 0 matix
    sumOfAi, sumOfBi = True, True
    for i in range(len(matrix.matrix)):
        for j in range(len(matrix.matrix[i])):
            if j == len(matrix.matrix[i]) - 1 and matrix.matrix[i][j].p != 0:
                sumOfBi = False
            elif matrix.matrix[i][j].p != 0:
                sumOfAi = False
    if sumOfAi == sumOfBi == True:
        files[1].write("\n\nAnswers: Infinity of solution\n\n")
        continue
    if sumOfAi == True and sumOfBi != True:
        files[1].write("\n\nAnswers: No solution\n\n")
        continue


    files[1].write("\\\\Solution:\\\\\\\\\n$\n")
    files[1].write(matrix.matrixToTex())
    files[1].write("\\Rightarrow\\\\\\\\\\\\\n")
    solution = matrix.solveMatrixAsSystem("Gauss", True)
    files[1].write("$\n")

    files[1].write(str("\\\\\\\\\\\\\nAnswers: ", ))
    if type(solution) == str:
        files[1].write(str(solution + "\n"))
    else:
        solution, stepsStr = solution[0], solution[1]
        solution.reverse()
        for i in range(len(solution)):
            files[1].write("$")
            if solution[i].q == 1 or solution[i].p == 0:
                files[1].write(str("x" + str(i + 1) + " = " + str(solution[i].p)))
            else:
                files[1].write(str("x" + str(i + 1) + " = \\frac{" + str(solution[i].p)
                                   + "}{" + str(solution[i].q) + "}"))
            if i != len(solution) - 1:
                files[1].write(", \\quad")
            files[1].write("$\n")

    files[1].write(str("\n"))

# finish TeX generate
texStr = "\\end{enumerate}\n" \
         "\\end{document}"
files[1].write(texStr)
files[1].close()

# TeX compile
os.system("pdflatex " + rezFileName + ".tex")
