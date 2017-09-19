#!/usr/bin/python
import os

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
    files[1].write("\\begin{bmatrix}\n")
    for e in range(len(matrix)):
        mstr = matrix[e]
        for el in range(len(mstr)):
            i = mstr[el]
            if i.q == 1 or i.p == 0:
                files[1].write(str(i.p))
            else:
                files[1].write("\\frac{" + str(i.p) + "}{" + str(i.q) + "}")
            if el != len(mstr) - 1:
                files[1].write(" & ")
        if e != len(matrix) - 1:
            files[1].write(str("\\\\ \n"))
    files[1].write(str("\\end{bmatrix}"))


def solveMatrix(matrix):
    leny, lenx = len(matrix), len(matrix[0])
    used = [False]*leny
    queue = []

    # first step of algorithm
    ifPrinted = False
    for x in range(lenx - 1):
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

        if ifPrinted:
            files[1].write("\\Rightarrow\n")
        printMatrix(matrix)
        ifPrinted = True

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
        elem = sum / matrix[y][x]
        solution.append(elem)
    return solution



# main section

# file read/write
files = [open("input.txt", "r"), open("rez.tex", "w")]

# generate TeX
texStr = "\\documentclass[14pt]{article}\n" \
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
    texStr = "\\item\n" + exercise + "\n"
    files[1].write(texStr)

    matrix = []
    matrix.append(list(map(int, files[0].readline().split())))
    for i in range(1, len(matrix[0])):
        nextStr = list(map(int, files[0].readline().split()))
        if len(nextStr) == 0:
            break
        matrix.append(nextStr)

    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = RationalNumber(matrix[i][j])

    files[1].write("\n$\n")
    printMatrix(matrix)
    files[1].write("\\Rightarrow\n")
    solution = solveMatrix(matrix)
    files[1].write("$\n")

    files[1].write(str("\n\nAnswers: ", ))
    if solution == "No solutions" or solution == "Infinity of solutions":
        files[1].write(str(solution + "\n"))
    else:
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
#os.system("pdflatex rez.tex")
