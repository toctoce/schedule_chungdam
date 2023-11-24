from service import AddON
from service import Sim

class Controller():
    
    @classmethod
    def operator_input(cls, map_input, start_input, spot_input, color_input, hazard_input):
        add_on = AddON()
        robot_pos = add_on.handle_map(map_input, start_input, spot_input, color_input, hazard_input)
        sim = Sim(robot_pos)
        process = cls.__run(add_on, sim)
        return process
    
    @classmethod
    def voice_recognization(cls):
        pass
    
    @staticmethod
    def __run(add_on: AddON, sim: Sim):
        process = []
        
        robot_status = sim.get_robot_status()
        add_on.plan_path(robot_status["pos"])

        process.append({
            "map_info": add_on.get_map_info_dict(),
            "robot": sim.get_robot_status_dict()
        })

        while add_on.get_path():
            prev_r_status = sim.get_robot_status()
            command = add_on.follow_path(prev_r_status)
            if command is None:
                continue
            if command == "forward":
                print(add_on.get_map_info())
                print(sim.get_robot_status())
                print(add_on.get_path())
                # print(add_on.__spot_list)
            sim.move_robot(command)
            cur_r_status = sim.get_robot_status()
            add_on.check_reach_spot(cur_r_status["pos"])
            add_on.compensating_imperfact_motion(command, prev_r_status, cur_r_status)

            color_blob_list = sim.detect_color_blob(add_on.get_map_info())
            add_on.mark_color_blob(color_blob_list)

            hazard_list = sim.detect_hazard(add_on.get_map_info())
            add_on.mark_hazard(hazard_list)
            if hazard_list:
                add_on.plan_path(sim.get_robot_status()["pos"])
            
            process.append({
                "map_info": add_on.get_map_info_dict(),
                "robot": sim.get_robot_status_dict()
            })

        print("마지막 상태")
        print(add_on.get_map_info())
        print(sim.get_robot_status())
        # print(add_on.__spot_list)
        return process