import numpy as np

'''
4*4数字拼图，
'''


class Blank:
    def __init__(self, y, x):
        self.x = y
        self.y = x

    def adjacent(self):
        result = []
        temp = [[self.y - 1, self.x],
                [self.y + 1, self.x],
                [self.y, self.x - 1],
                [self.y, self.x + 1]]
        for m in temp:
            if (0 <= m[0] <= 3) and (0 <= m[1] <= 3):
                result.append(m)
        return result


matrix = np.linspace(1, 16, 16, dtype='int').reshape((4, 4))
print(matrix)
print('-------')
blank = Blank(3, 3)
for i in range(1000):
    # 随机取一个相邻的点
    adjacent = blank.adjacent()
    point = adjacent[np.random.choice(range(len(adjacent)))]

    # 将blank和这个点的数字进行交换
    temp = matrix[point[0], point[1]]
    matrix[point[0], point[1]] = matrix[blank.y, blank.x]
    matrix[blank.y, blank.x] = temp
    blank.y = point[0]
    blank.x = point[1]
print(matrix)
