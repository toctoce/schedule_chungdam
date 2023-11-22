from AddON import AddON
from Sim import Sim
from Robot import Robot

from UI import UI
add_on = AddON()
robot_pos = add_on.handle_map()
print(add_on.map_info.get_row())
print(add_on.map_info.get_col())

ui = UI(add_on.map_info.get_row(), add_on.map_info.get_col())
ui.display(add_on.map_info)
# add_on = AddON()
# robot_pos = add_on.handle_map()
# sim = Sim(robot_pos)
# print(add_on.map_info)
# path = add_on.plan_path(sim.get_robot_status()["pos"], [])
# while path:
#     print("============================================")
#     print("map :")
#     print(add_on.map_info)
#     print("path :", path)
#     next_pos = path[0]
#     print("next_pos :", next_pos)
#     cur_robot_status = sim.get_robot_status()
#     print("cur_robot_status :", cur_robot_status)
#     # 경로 를 이용해 명령 저장
#     command = add_on.follow_path(cur_robot_status, next_pos)
#     if command == "forward" or command is None:
#         path.pop(0)
#     print("command :", command)
#     next_robot_status = sim.move_robot(command)
#     if next_robot_status is None:
#         continue
#     # 이동함. 지도 다시 세팅
#     add_on.map_set_pos_info(cur_robot_status["pos"], '.')
#     add_on.map_set_pos_info(next_robot_status["pos"], 'R')
#     # 주변 위치 탐색.
#     color_blob_list = sim.detect_color_blob(add_on.map_info)
#     hazard_list = sim.detect_hazard(add_on.map_info)
#     add_on.mark_color_blob(color_blob_list)
#     add_on.mark_hazard(hazard_list)
#     print()
#     if hazard_list:
#         path = add_on.plan_path(sim.get_robot_status()["pos"], [])
#         continue

# # print(path)
# # print(sim.get_robot_status())
# # command = add_on.follow_path(sim.get_robot_status(), path[1])
# # print(command)
# # sim.move_robot(command)
# # print(sim.get_robot_status())