from service import AddON
from service import Sim

class Facade():
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
        self.add_on.plan_path(self.sim.get_robot_status()["pos"])

        while self.add_on.get_path():
            command = self.add_on.follow_path(self.sim.get_robot_status())
            if command is None:
                continue
            self.sim.move_robot(command)
            
            color_blob_list = self.sim.detect_color_blob(self.add_on.map_info)
            hazard_list = self.sim.detect_hazard(self.add_on.map_info)
            self.add_on.mark_color_blob(color_blob_list)
            self.add_on.mark_hazard(hazard_list)
            if hazard_list:
                self.add_on.plan_path(self.sim.get_robot_status()["pos"])

        print("마지막 상태")
        print(self.add_on.map_info)
        print(self.sim.get_robot_status())