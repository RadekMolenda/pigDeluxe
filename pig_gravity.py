def pigGravity(vector):
    rx, ry = vector
    changeY = - 0.05 * ry
    def change(x, y):
        return [x, y + changeY]
    return change

def pigDrag(vector):

    rx, ry = vector
    changeX = - 0.01 * rx
    def change(x, y):
        return [x + changeX, y]
    return change
