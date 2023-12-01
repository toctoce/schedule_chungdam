import requests
import json

class VoiceRecognizer():
    __dic = {
        "일": 1, "이": 2, "삼": 3, "사": 4, "오": 5,
        "육": 6, "칠": 7, "팔": 8, "구": 9, "십": 10,
        "십일": 11, "십이": 12, "십삼": 13, "십사": 14, "십오": 15,
        "십육": 16, "십칠": 17, "십팔": 18, "십구": 19, "이십": 10,
        "이십일": 21, "이십이": 22, "이십삼": 23, "이십사": 24, "이십오": 25,
        "이십육": 26, "이십칠": 27, "이십팔": 28, "이십구": 29, "삼십": 30,
        "삼십일": 31, "삼십이": 32, "삼십삼": 33, "삼십사": 34, "삼십오": 35,
        "삼십육": 36, "삼십칠": 37, "삼십팔": 38, "삼십구": 39, "사십": 40,
        "사십일": 41, "사십이": 42, "사십삼": 43, "사십사": 44, "사십오": 45,
        "사십육": 46, "사십칠": 47, "사십팔": 48, "사십구": 49, "오십": 50,
        "컬러블롭": 'c', "컬러": 'c', "블록": 'c', "컬러블록": 'c', "칼라": 'c',
        "컬리": 'c', "컬루": 'c', "컬로": 'c', "컬라": 'c', "콜로": 'c',
        "콜록": 'c', "": 'c', "컨너": 'c', "컨나": 'c', "컬너": 'c',
        "컬나": 'c', "코노": 'c', "커너": 'c', "칸나": 'c',
        "해저드": 'h', "해저브": 'h', "해저그": 'h', "해더드": 'h', "해더브": 'h',
        "해더그": 'h', "해처드": 'h', "해처그": 'h', "해처브": 'h', "헤이그": 'h',
        "헤어": 'h', "해접": 'h', "허접": 'h', "하자드": 'h', "하저드": 'h',
        "하자그": 'h', "하자브": 'h', "해자드": 'h', "해저": 'h', "해젓": 'h'
        }
    def __init__(self) -> None:
        pass
    def __voice_to_text(self, id, api_key, file_stream):
        url = "https://naveropenapi.apigw.ntruss.com/recog/v1/stt?=lang=Kor"
        
        headers = {
            "Content-Type": "application/octet-stream",
            "X-NCP-APIGW-API-KEY-ID": id,
            "X-NCP-APIGW-API-KEY": api_key,
        }

        audio_data = file_stream.read()
        response = requests.post(url, headers=headers, data=audio_data)
        print(response.text)
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            raise Exception("Voice recognization : Failed")
    
    def __handle_word(self, word: str) -> str:
        if word.isdigit():
            return int(word)
        if word in self.__dic.keys():
            return self.__dic[word]
        return None
    
    def __text_to_data(self, text: str):
        words = text.split()
        data = list(map(self.__handle_word, words))
        return data
    
    def __data_to_info(self, data: list):
        processed_data = []
        for i in range(len(data)-1, -1, -1):
            if isinstance(data[i], int):
                processed_data.append(data[i])
            if len(processed_data) == 2:
                break
        for i in range(len(data)):
            if type(data[i]) == str:
                processed_data.append(data[i])
                break
        if len(processed_data) != 3:
            raise Exception("Voice recognization : Invalid Word")
        # processed_data 예시 - [2, 1, 'c']
        info = {
            "type": processed_data[2],
            "pos": (processed_data[0], processed_data[1])
        }
        return info
    
    def voice_to_info(self, id, api_key, file_stream):
        text = self.__voice_to_text(id, api_key, file_stream)
        data = self.__text_to_data(text["text"])
        info = self.__data_to_info(data)
        return info