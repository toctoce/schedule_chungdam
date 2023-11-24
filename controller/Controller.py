from service import AddON
from service import Sim

class Controller():
    def __init__(self):
        # self.add_on = AddON()
        # self.sim = Sim()

        # 임시.
        self.add_on = AddON()
        robot_pos = self.add_on.handle_map()
        self.sim = Sim(robot_pos)

    #TODO 미완성임.  
    def operator_input(self, inputs):
        robot_pos = self.add_on.handle_map()
        self.sim.create_robot(robot_pos)

    def run(self):
        robot_pos = self.sim.get_robot_status()["pos"]
        self.add_on.plan_path(robot_pos)

        while self.add_on.get_path():
            prev_r_status = self.sim.get_robot_status()
            command = self.add_on.follow_path(prev_r_status)
            if command is None:
                continue
            if command == "forward":
                print(self.add_on.map_info)
                print(self.sim.get_robot_status())
                print(self.add_on.get_path())
                print(self.add_on.spot_list)
            self.sim.move_robot(command)
            cur_r_status = self.sim.get_robot_status()
            self.add_on.check_reach_spot(cur_r_status["pos"])
            self.add_on.compensating_imperfact_motion(command, prev_r_status, cur_r_status)
            # 여기서 오작동 보상
            
            color_blob_list = self.sim.detect_color_blob(self.add_on.map_info)
            hazard_list = self.sim.detect_hazard(self.add_on.map_info)
            self.add_on.mark_color_blob(color_blob_list)
            self.add_on.mark_hazard(hazard_list)
            if hazard_list:
                self.add_on.plan_path(self.sim.get_robot_status()["pos"])

        print("마지막 상태")
        print(self.add_on.map_info)
        print(self.sim.get_robot_status())
        print(self.add_on.spot_list)
