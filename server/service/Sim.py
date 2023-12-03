from domain import Robot
from domain import MapInfo

class Sim():
    __robot: Robot = None
    
    def __init__(self, robot_pos: tuple) -> None:
        self.__robot = Robot(robot_pos)
    
    def __init__(self) -> None:
        self.__robot = Robot((0, 0))
        pass

    def create_robot(self, robot_pos: tuple) -> None:
        if self.__robot is not None:
            self.__robot = Robot(robot_pos)

    def detect_hazard(self, map_info: MapInfo) -> list:
        pos_list = []

        find_pos = self.__robot.get_forward_pos()
        if not map_info.is_valid_pos(find_pos):
            return pos_list
        if map_info.get_pos_info(find_pos) == 'h':
            pos_list.append(find_pos)
        
        return pos_list
    
    def detect_color_blob(self, map_info: MapInfo) -> list:
        pos_list = []
        
        find_pos_list = self.__robot.get_all_direction_pos()
        for find_pos in find_pos_list:
            map_info.is_valid_pos(find_pos)
            if not map_info.is_valid_pos(find_pos):
                continue
            if map_info.get_pos_info(find_pos) == 'c':
                pos_list.append(find_pos)
        
        return pos_list

    def move_robot(self, command: str) -> dict:
        if command is None:
            return None
        if command == "forward":
            self.__robot.forword()
        elif command == "turn_right":
            self.__robot.turn_right()
        else :
            raise Exception("잘못된 명령어가 입력되었습니다.")
        return self.get_robot_status()

    def get_robot_status(self) -> dict:
        return self.__robot.get_status()
    def get_robot_status_dict(self) -> dict:
        return self.__robot.get_status_dict()
    def set_robot_status(self, pos, direction) -> None:
        self.__robot.set_status(pos, direction)