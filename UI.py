import pygame
from MapInfo import MapInfo

BLACK = (0,0,0)
WHITE = (255,255,255)

class UI():
    imgs = {}
    def __init__(self, row, col) -> None:
        # TODO:셀 사이즈 맵 크기로 조정
        self.cell_size = 100
        self.row = row
        self.col = col
        pygame.init()
        pygame.display.set_caption("Image Display")

        # 스크린 생성
        screen_size = (self.col * self.cell_size, self.row * self.cell_size)
        self.screen = pygame.display.set_mode(screen_size)

        # 이미지 로드
        self.imgs['H'] = pygame.image.load('imgs/hazard.png')
        self.imgs['C'] = pygame.image.load('imgs/color_blob.png')
        self.imgs['R'] = pygame.image.load('imgs/robot.png')
        self.imgs['P'] = pygame.image.load('imgs/predefined_spot.png')
        self.imgs['.'] = pygame.image.load('imgs/none.png') # 필요 없을 듯

        # 이미지 스케일링
        self.imgs['H'] = pygame.transform.scale(self.imgs['H'], (self.cell_size, self.cell_size))
        self.imgs['C'] = pygame.transform.scale(self.imgs['C'], (self.cell_size, self.cell_size))
        self.imgs['R'] = pygame.transform.scale(self.imgs['R'], (self.cell_size, self.cell_size))
        self.imgs['P'] = pygame.transform.scale(self.imgs['P'], (self.cell_size, self.cell_size))
        self.imgs['.'] = pygame.transform.scale(self.imgs['.'], (self.cell_size, self.cell_size))

    
    def display(self, map_info:MapInfo):
        # 초기 맵 출력
        self.ui_print(map_info)
        # 이벤트 처리
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                # 마우스 클릭하면 해당 코드 동작
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.ui_print(map_info)
                    pygame.display.flip()
        # Pygame 종료
        pygame.quit()

    def ui_print(self, map_info:MapInfo):
        # 격자 출력
        self.ui_reset(map_info)
        # map_info를 이용해 이미지를 해당 위치에 출력
        for row_idx in range(map_info.get_row()):
            for col_idx in range(map_info.get_col()):
                # key : h, c, r, p, i
                key = map_info.get_info()[row_idx][col_idx]
                if key in ['.','h','c']:
                    continue
                self.screen.blit(self.imgs[key], (col_idx * self.cell_size, row_idx * self.cell_size))
        pygame.display.flip()

    def ui_reset(self, map_info:MapInfo):
        # 흰색으로 전부 채움.
        self.screen.fill(WHITE)
        # 열 격자 출력
        for row in range(map_info.get_row()):
            pygame.draw.line(self.screen, BLACK, \
                             (0 + self.cell_size / 2, row * self.cell_size + self.cell_size / 2), \
                                (map_info.get_col() * self.cell_size - self.cell_size / 2, row * self.cell_size + self.cell_size / 2))
        # 행 격자 출력
        for col in range(map_info.get_col()):
            pygame.draw.line(self.screen, BLACK, \
                             (col * self.cell_size + self.cell_size / 2, 0 + self.cell_size / 2), \
                                (col * self.cell_size + self.cell_size / 2, map_info.get_row() * self.cell_size - self.cell_size / 2))

# TODO:이벤트 들어오면 새롭게 동작해야함.
# TODO:맨 아래 추가 버튼? 필요할 수도.
# TODO:이미지 사이즈 조정 필요함.
# TODO:로봇 방향 설정 - map에 로봇 방향도 들어가 있어야 하는 듯