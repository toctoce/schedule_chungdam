import random

class Robot():
    __pos: tuple = None
    __direction: int = 0
    
    def __init__(self, pos: tuple, direction: int) -> None:
        self.__pos = pos
        self.__direction = direction

    def __init__(self, pos: tuple) -> None:
        self.__pos = pos

    def forword(self) -> dict:
        # 오작동
        if random.random() <= 0.1:
            # 아무 동작 안함.
            if random.random() <= 0.5:
                pass
            # 두 번 움직임.
            else :
                self.__pos = self.get_forward_pos()
                self.__pos = self.get_forward_pos()
        # 제대로 작동
        else :
            self.__pos = self.get_forward_pos()
        return self.get_status()

    
    def turn_right(self) -> dict:
        # 오작동
        if random.random() <= 0.1:
            # 아무 동작 안함.
            if random.random() <= 0.5:
                pass
            # 두 번 움직임.
            else :
                self.__direction = (self.__direction + 1) % 4
                self.__direction = (self.__direction + 1) % 4
        # 제대로 작동
        else :
            self.__direction = (self.__direction + 1) % 4
        return self.get_status()
    
    def get_status(self) -> dict:
        return {"pos": self.__pos, "direction": self.__direction}
    
    def get_forward_pos(self) -> tuple:
        r, c = self.__pos
        if self.__direction == 0:
            r -= 1
        elif self.__direction == 1:
            c += 1
        elif self.__direction == 2:
            r += 1
        elif self.__direction == 3:
            c -= 1
        return (r, c)
    
    def get_all_direction_pos(self) -> list:
        r, c = self.__pos
        ret = []
        for d_row, d_col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            ret.append((r + d_row, c + d_col))
        return ret
