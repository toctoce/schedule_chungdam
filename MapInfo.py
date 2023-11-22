class MapInfo():
    __row: int = None
    __col: int = None
    __info: list = None
    def __init__(self, row:int, col:int, info:list):
        self.__row = row
        self.__col = col
        # h : hidden hazard, c : hidden color blob, R : robot, P : predefined spot, . : nothing
        # H : found hazard, C : found color blob
        # info는 처음에 h, c, R, P, .으로 세팅됨.
        self.__info = info
        # self.set_pos_info((3,2),'H')
        # self.set_pos_info((3,3),'C')
        # print(self.__row, self.__col)
        # print(self.__info)
    
    def __str__(self):
        ret = ""
        for line in self.__info:
            for element in line:
                ret += element + " "
            ret += "\n"
        ret += f"row : {self.__row}, col : {self.__col}"
        return ret
    
    def get_pos_info(self, pos: tuple):
        return self.__info[pos[0]][pos[1]]
    
    def set_pos_info(self, pos: tuple, new_info: str):
        self.__info[pos[0]][pos[1]] = new_info
    
    def is_valid_pos(self, pos: tuple) -> bool:
        if 0 <= pos[0] <= self.__row and 0 <= pos[1] <= self.__col:
            return True
        return False

    def get_row(self):
        return self.__row
    def get_col(self):
        return self.__col
    def get_info(self):
        return self.__info