from Robot import Robot
from MapInfo import MapInfo

class Sim():
    __robot: Robot = None
    
    def __init__(self, robot_pos: tuple) -> None:
        self.__robot = Robot(robot_pos)

    def detect_hazard(self, map_info: MapInfo):
        pos_list = []

        find_pos = self.__robot.get_forward_pos()
        if not map_info.is_valid_pos(find_pos):
            return pos_list
        if map_info.get_pos_info(find_pos) == 'h':
            pos_list.append(find_pos)
        
        return pos_list
    
    def detect_color_blob(self, map_info: MapInfo):
        pos_list = []

        find_pos_lst = self.__robot.get_all_direction_pos()
        for find_pos in find_pos_lst:
            map_info.is_valid_pos(find_pos)
            if not map_info.is_valid_pos(find_pos):
                continue
            if map_info.get_pos_info(find_pos) == 'c':
                pos_list.append(find_pos)
        
        return pos_list

    def move_robot(self, command: str):
        if command is None:
            return None
        if command == "forward":
            self.__robot.forword()
        elif command == "turn_right":
            self.__robot.turn_right()
        else :
            raise ValueError("Sim received invalid command")
        return self.get_robot_status()
        
    def get_robot_status(self):
        return self.__robot.get_status()
