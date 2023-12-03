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
    
    def voice_recognization(self, id, api_key, file_stream, status_data):
        map_info_data = status_data["map_info"]
        map_info = list(map(list,(map_info_data.split())))
        self.add_on.set_map_info(map_info)

        spot_list = status_data["spot_list"]
        spot_list = list(map(tuple, spot_list))
        self.add_on.set_spot_list(spot_list)

        robot_status = status_data["robot"]
        r_pos = (robot_status["row"], robot_status["col"])
        r_direction = robot_status["direction"]
        self.sim.set_robot_status(r_pos, r_direction)

        vr = VoiceRecognizer()
        err = None
        try:
            voice_info = vr.voice_to_info(id, api_key, file_stream)
            self.add_on.set_map_one_pos(voice_info["pos"], voice_info['type'])
        except Exception as e:
            err = str(e)

        process = self.__run()
        return process, err
    
    def __run(self):
        def return_dict(is_mulfunction=False, err=None):
            if err is None:
                ret = {
                    "map_info": self.add_on.get_map_info_str(),
                    "robot": self.sim.get_robot_status_dict(),
                    "spot_list": self.add_on.get_copy_spot_list(),
                    "status": 0 if not is_mulfunction else 1
                }
            else :
                ret = {
                    "map_info": self.add_on.get_map_info_str(),
                    "robot": self.sim.get_robot_status_dict(),
                    "spot_list": self.add_on.get_copy_spot_list(),
                    "err": err,
                    "status": -1
                }
            return ret
        
        process = []
        
        color_blob_list = self.sim.detect_color_blob(self.add_on.get_map_info())
        self.add_on.mark_color_blob(color_blob_list)

        hazard_list = self.sim.detect_hazard(self.add_on.get_map_info())
        self.add_on.mark_hazard(hazard_list)

        robot_status = self.sim.get_robot_status()
        try :
            self.add_on.plan_path(robot_status["pos"])
        except Exception as e:
            process.append(return_dict(err=str(e)))
            return process

        process.append(return_dict())

        while self.add_on.get_path():
            prev_r_status = self.sim.get_robot_status()
            command = self.add_on.follow_path(prev_r_status)
            if command is None:
                continue
            self.sim.move_robot(command)
            cur_r_status = self.sim.get_robot_status()
            self.add_on.check_reach_spot(cur_r_status["pos"])
            try :
                is_mulfunction = self.add_on.compensating_imperfact_motion(command, prev_r_status, cur_r_status)
            except Exception as e:
                process.append(return_dict(err=str(e)))
                break
            color_blob_list = self.sim.detect_color_blob(self.add_on.get_map_info())
            self.add_on.mark_color_blob(color_blob_list)

            hazard_list = self.sim.detect_hazard(self.add_on.get_map_info())
            self.add_on.mark_hazard(hazard_list)
            if hazard_list:
                try :
                    self.add_on.plan_path(self.sim.get_robot_status()["pos"])
                except Exception as e:
                    process.append(return_dict(err=str(e)))
                    return process
            
            process.append(return_dict(is_mulfunction=is_mulfunction))

        return process
        