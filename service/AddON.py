from domain import MapInfo

from collections import deque
import copy

class AddON():
    map_info: MapInfo = None
    spot_list: list = None
    __path: list = None

    def __init__(self):
        pass

    # 로봇 위치 반환
    def handle_map(self) -> tuple:
        # 사용자 입력
        # map_input = input("Map: ")
        # start_input = input("Start: ")
        # spot_input = input("Spot: ")
        # color_input = input("Color: ")
        # hazard_input = input("Hazard: ")
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
        self.spot_list = [tuple(map(int, pos.strip('()').split())) for pos in spot_input.split(')') if pos]
        color_list = [tuple(map(int, pos.strip('()').split())) for pos in color_input.split(')') if pos]
        hazard_list = [tuple(map(int, pos.strip('()').split())) for pos in hazard_input.split(')') if pos]

        # 2차원 배열 초기화
        map_info = [['.' for _ in range(col + 1)] for _ in range(row + 1)]
        # map_info[robot_row][robot_col] = 'R'

        # 각 문자에 해당하는 좌표에 해당 문자 표시
        for pos in self.spot_list:
            map_info[pos[0]][pos[1]] = 'P'
        for pos in color_list:
            map_info[pos[0]][pos[1]] = 'c'
        for pos in hazard_list:
            map_info[pos[0]][pos[1]] = 'h'
        
        # 맵 생성
        self.map_info = MapInfo(row, col, map_info)
        

        # 로봇 위치 반환
        return (robot_row, robot_col)

    def plan_path(self, robot_pos: tuple, spot_list: list):
        total_path = [robot_pos]
        for spot in self.spot_list:
            # robot pos, 경로
            q = deque([(total_path.pop(), [])])
            # 방문처리용 지도
            visit = copy.deepcopy(self.map_info.get_info())
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
                        if self.map_info.is_valid_pos(next_pos) and self.map_info.get_pos_info(next_pos) != 'H':
                            q.append((next_pos, path + [cur_pos]))
            # break 안 되었을 때 - 목적지에 도착할 수 없을 때
            else :
                raise ValueError("The robot can't reach all the spots.")
        
        self.__path = total_path

        return total_path

    def mark_hazard(self, pos_list: list):
        for pos in pos_list:
            self.map_info.set_pos_info(pos, 'H')

    def mark_color_blob(self, pos_list: list):
        for pos in pos_list:
            self.map_info.set_pos_info(pos, 'C')
    
    def follow_path(self, robot_status: dict, next_pos: tuple):
        next_pos = self.__path[0]
        r_pos = robot_status["pos"]
        r_direction = robot_status["direction"]
        if r_pos == next_pos:
            return None
        gap = (next_pos[0] - r_pos[0], next_pos[1] - r_pos[1])
        if gap == [(-1, 0), (0, 1), (1, 0), (0, -1)][r_direction]:
            return "forward"
        elif gap in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            return "turn_right"
        else :
            raise ValueError("Invalid Path")
    
    def map_set_pos_info(self, pos: tuple, new_info: str):
        self.map_info.set_pos_info(pos, new_info)
    def compensating_imperfact_motion():
        pass
    def get_robot_position():
        pass
