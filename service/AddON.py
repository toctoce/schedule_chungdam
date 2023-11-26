from domain import MapInfo

from collections import deque
import copy

class AddON():
    __map_info: MapInfo = None
    __spot_list: list = None
    __path: list = None

    def __init__(self):
        pass

    # 로봇 위치 반환
    def handle_map(self, map_input, start_input, spot_input, color_input, hazard_input) -> tuple:
        map_input = "(4 5)"
        start_input = "(1 2)"
        spot_input = "((4 2)(0 5)(1 3))"
        color_input = "((2 2)(4 4))"
        hazard_input = "((1 0)(3 2)(0 2)(0 4))"

        # map 크기
        row, col = map(int, map_input.strip('()').split())
        # 로봇 위치
        robot_row, robot_col = map(int, start_input.strip('()').split())

        # 각 문자로 표시할 좌표 추출
        spot_list = [tuple(map(int, pos.strip('()').split())) for pos in spot_input.split(')') if pos]
        color_list = [tuple(map(int, pos.strip('()').split())) for pos in color_input.split(')') if pos]
        hazard_list = [tuple(map(int, pos.strip('()').split())) for pos in hazard_input.split(')') if pos]

        # 2차원 배열 초기화
        map_info = [['.' for _ in range(col + 1)] for _ in range(row + 1)]
        # map_info[robot_row][robot_col] = 'R'

        # 각 문자에 해당하는 좌표에 해당 문자 표시
        for pos in spot_list:
            map_info[row - pos[0]][pos[1]] = 'P'
        for pos in color_list:
            map_info[row - pos[0]][pos[1]] = 'c'
        for pos in hazard_list:
            map_info[row - pos[0]][pos[1]] = 'h'
        
        # spot list 저장
        self.__spot_list = [(row - spot[0], spot[1]) for spot in spot_list]
        # 맵 생성
        self.__map_info = MapInfo(row, col, map_info)
        # 로봇 위치 반환
        return (row - robot_row, robot_col)

    def plan_path(self, robot_pos: tuple):
        print(self.__map_info)
        total_path = [robot_pos]
        for spot in self.__spot_list:
            # robot pos, 경로
            q = deque([(total_path.pop(), [])])
            # 방문처리용 지도
            visit = copy.deepcopy(self.__map_info.get_info())
            while q:
                cur_pos, path = q.popleft()
                if cur_pos == spot:
                    # 목적지에 도착하면 경로를 반환
                    total_path = total_path + path + [cur_pos]
                    break
                # 방문처리
                if visit[cur_pos[0]][cur_pos[1]] != 'x':
                    visit[cur_pos[0]][cur_pos[1]] = 'x'

                    # 인접한 좌표를 큐에 추가
                    for d_row, d_col in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                        next_pos = (cur_pos[0] + d_row, cur_pos[1] + d_col)
                        if self.__map_info.is_valid_pos(next_pos) and self.__map_info.get_pos_info(next_pos) != 'H':
                            q.append((next_pos, path + [cur_pos]))
            # break 안 되었을 때 - 목적지에 도착할 수 없을 때
            else :
                raise Exception("The robot can't reach all the spots.")
        
        self.__path = total_path

    def mark_hazard(self, pos_list: list):
        for pos in pos_list:
            self.__map_info.set_pos_info(pos, 'H')

    def mark_color_blob(self, pos_list: list):
        for pos in pos_list:
            self.__map_info.set_pos_info(pos, 'C')
    
    def follow_path(self, robot_status: dict):
        next_pos = self.__path[0]
        r_pos = robot_status["pos"]
        r_direction = robot_status["direction"]
        if r_pos == next_pos:
            self.__path.pop(0)
            return None
        gap = (next_pos[0] - r_pos[0], next_pos[1] - r_pos[1])
        if gap == [(-1, 0), (0, 1), (1, 0), (0, -1)][r_direction]:
            self.__path.pop(0)
            return "forward"
        elif gap in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            return "turn_right"
        else :
            raise Exception("Invalid Path")

    def check_mulfunction(self, command, prev_status, cur_status) -> bool:
        prev_pos = prev_status["pos"]
        prev_direction = prev_status["direction"]
        cur_pos = cur_status["pos"]
        cur_direction = cur_status["direction"]
        if command is None:
            if prev_direction == cur_direction and prev_pos == cur_pos:
                return False
            else :
                return True
        if command == "forward":
            if prev_direction != cur_direction:
                return True
            if (prev_direction == 0) and \
                (cur_pos[0] - prev_pos[0] != -1 or cur_pos[1] - prev_pos[1] != 0):
                    return True
            elif (prev_direction == 1) and \
                (cur_pos[0] - prev_pos[0] != 0 or cur_pos[1] - prev_pos[1] != 1):
                    return True
            elif (prev_direction == 2) and \
                (cur_pos[0] - prev_pos[0] != 1 or cur_pos[1] - prev_pos[1] != 0):
                    return True
            elif (prev_direction == 3) and \
                (cur_pos[0] - prev_pos[0] != 0 or cur_pos[1] - prev_pos[1] != -1):
                    return True
        elif command == "turn_right":
            if prev_pos != cur_pos:
                return True
            if (prev_direction + 1) % 4 != cur_direction:
                return True
        return False

    def compensating_imperfact_motion(self, command: str, prev_status: dict, cur_status: dict) -> None:
        if self.check_mulfunction(command, prev_status, cur_status):
            cur_pos = cur_status["pos"]
            if self.__map_info.is_valid_pos(cur_pos) == False:
                raise Exception("Out of the map")
            if self.__map_info.get_pos_info(cur_pos) in ['H', 'h']:
                raise Exception("Reached the hazard")
            self.plan_path(cur_status["pos"])

    def check_reach_spot(self, robot_pos: tuple):
        if self.__map_info.is_valid_pos(robot_pos) == False:
            return
        if self.__map_info.get_pos_info(robot_pos) == 'P':
            try:
                idx = self.__spot_list.index(robot_pos)
                self.__spot_list.pop(idx)
            except ValueError:
                pass

    def get_path(self) -> list:
        return self.__path
    
    def get_map_info(self) -> MapInfo:
        return self.__map_info

    def get_map_info_dict(self) -> dict:
        return {
            "row": self.__map_info.get_row(),
            "col": self.__map_info.get_col(),
            "info": self.__map_info.get_info()
        }

    def set_map_one_pos(self, pos: tuple, new_info: str):
        coord_sys_pos = (self.get_map_info().get_row() - pos[0], pos[1])
        self.__map_info.set_pos_info(coord_sys_pos, new_info)