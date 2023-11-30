from service import AddON
from service import Sim
from service import VoiceRecognizer

class Controller():
    add_on: AddON = None
    sim: Sim = None

    def __init__(self) -> None:
        self.add_on = AddON()
        self.sim = Sim()
        
    def operator_input(self, map_input, start_input, spot_input, color_input, hazard_input):
        robot_pos = self.add_on.handle_map(map_input, start_input, spot_input, color_input, hazard_input)
        self.sim.set_robot_status(robot_pos, 1)
        process = self.__run()
        return process
    
    def voice_recognization(self, id, api_key, file_stream, robot_status):
        vr = VoiceRecognizer()
        # voice_info = vr.voice_to_info(id, api_key, file_stream)
        voice_info = {
            "type": 'c',
            "pos": (1,2)
        }
        self.add_on.set_map_one_pos(voice_info["pos"], voice_info['type'])

        r_pos = (robot_status["row"], robot_status["col"])
        r_direction = robot_status["direction"]
        self.sim.set_robot_status(r_pos, r_direction)

        process = self.__run()
        return process
    
    def __run(self):
        process = []
        
        color_blob_list = self.sim.detect_color_blob(self.add_on.get_map_info())
        self.add_on.mark_color_blob(color_blob_list)

        hazard_list = self.sim.detect_hazard(self.add_on.get_map_info())
        self.add_on.mark_hazard(hazard_list)

        robot_status = self.sim.get_robot_status()
        self.add_on.plan_path(robot_status["pos"])

        process.append({
            "map_info": self.add_on.get_map_info_str(),
            "robot": self.sim.get_robot_status_dict(),
            "status": 0
        })

        while self.add_on.get_path():
            prev_r_status = self.sim.get_robot_status()
            command = self.add_on.follow_path(prev_r_status)
            if command is None:
                continue
            if command == "forward":
                print(self.add_on.get_map_info())
                print(self.sim.get_robot_status())
                print(self.add_on.get_path())
                # print(self.add_on.__spot_list)
            self.sim.move_robot(command)
            cur_r_status = self.sim.get_robot_status()
            self.add_on.check_reach_spot(cur_r_status["pos"])
            try :
                is_mulfunction = self.add_on.compensating_imperfact_motion(command, prev_r_status, cur_r_status)
            except Exception as e:
                process.append({
                    "err": str(e),
                    "status": -1
                })
                break
            color_blob_list = self.sim.detect_color_blob(self.add_on.get_map_info())
            self.add_on.mark_color_blob(color_blob_list)

            hazard_list = self.sim.detect_hazard(self.add_on.get_map_info())
            self.add_on.mark_hazard(hazard_list)
            if hazard_list:
                self.add_on.plan_path(self.sim.get_robot_status()["pos"])
            
            process.append({
                "map_info": self.add_on.get_map_info_str(),
                "robot": self.sim.get_robot_status_dict(),
                "status": 0 if not is_mulfunction else 1
            })

        print("마지막 상태")
        print(self.add_on.get_map_info())
        print(self.sim.get_robot_status())
        # print(self.add_on.__spot_list)
        return process