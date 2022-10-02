import copy

class MatrixInversion:

    def __init__(self, matrix):
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Error! Matrix dimensions are different!")
        self.matrix = matrix
        self.matrix = self.matrix.T
        self.flag = False

    def _inv(self):
        A = list(list(a) for a in self.matrix)
        result = [[0 for i in range(len(A[0]))] for j in range(len(A))]
        result_2 = [[0 for i in range(len(A[0]))] for j in range(len(A))]

        for i in range(len(A)):
            for j in range(len(A[0])):
                tmp = self._minor(A, i, j)
                division = 1 / self._det(A)

                if isinstance(division, list):
                    self.flag = True
                    if i + j % 2 == 1:
                        result[i][j] = -1 * self._det(tmp) * division[0]
                        result_2[i][j] = -1 * self._det(tmp) * division[1]
                    else:
                        result[i][j] = 1 * self._det(tmp) * division[0]
                        result_2[i][j] = 1 * self._det(tmp) * division[1]
                else:
                    if i + j % 2 == 1:
                        result[i][j] = -1 * self._det(tmp) * division
                    else:
                        result[i][j] = 1 * self._det(tmp) * division
        return [result, result_2]

    def __call__(self):
        result = self._inv()
        if self.flag:
            return result
        return result[0]

    def _minor(self, A, i, j):
        M = copy.deepcopy(A)
        del M[i]
        for i in range(len(A[0]) - 1):
            del M[i][j]
        return M

    def _det(self, A):
        m = len(A)
        n = len(A[0])
        if m != n:
            return None
        if n == 1:
            return A[0][0]
        signum = 1
        determinant = 0

        for j in range(n):
            determinant += A[0][j] * signum * self._det(self._minor(A, 0, j))
            signum *= -1
        return determinant
