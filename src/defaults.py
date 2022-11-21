import os
from os.path import join

FPS = 60

WHITESMOKE = (245, 245, 245, 255)

DEF_WIN_W = 900
DEF_WIN_H = 400
DEF_WIN_SCALE = .6

DIR_ASSETS = os.path.abspath('src/assets')

LEFT = 1
RIGHT = 2

ACT_ATTACK = 1
ACT_JUMP = 2
ACT_RUN_RIGHT = 3
ACT_RUN_LEFT = 4

ATTACK_1 = 1
ATTACK_2 = 2
ATTACK_3 = 3
DEATH = 4
FALL = 5
GET_HIT = 6
IDLE = 7
JUMP = 8
RUN = 9

SCENE_SIZE = (288, 160)

SCENE_IMAGES= [
  join(DIR_ASSETS, 'scene', 'background_0.png'),
  join(DIR_ASSETS, 'scene', 'background_1.png'),
  join(DIR_ASSETS, 'scene', 'background_2.png'),
  join(DIR_ASSETS, 'scene', 'background_3.png'),
]

FRAMES_WARRIOR_1 = {
  ATTACK_1: join(DIR_ASSETS, 'warrior_1', 'Attack1.png'),
  ATTACK_2: join(DIR_ASSETS, 'warrior_1', 'Attack2.png'),
  ATTACK_3: join(DIR_ASSETS, 'warrior_1', 'Attack3.png'),
  DEATH: join(DIR_ASSETS, 'warrior_1', 'Death.png'),
  FALL: join(DIR_ASSETS, 'warrior_1', 'Fall.png'),
  GET_HIT: join(DIR_ASSETS, 'warrior_1', 'Get_Hit.png'),
  IDLE: join(DIR_ASSETS, 'warrior_1', 'Idle.png'),
  JUMP: join(DIR_ASSETS, 'warrior_1', 'Jump.png'),
  RUN: join(DIR_ASSETS, 'warrior_1', 'Run.png')
}

FRAMES_WARRIOR_2 = {
  ATTACK_1: join(DIR_ASSETS, 'warrior_2', 'Attack1.png'),
  ATTACK_2: join(DIR_ASSETS, 'warrior_2', 'Attack2.png'),
  ATTACK_3: join(DIR_ASSETS, 'warrior_2', 'Attack3.png'),
  DEATH: join(DIR_ASSETS, 'warrior_2', 'Death.png'),
  FALL: join(DIR_ASSETS, 'warrior_2', 'Fall.png'),
  GET_HIT: join(DIR_ASSETS, 'warrior_2', 'Get_Hit.png'),
  IDLE: join(DIR_ASSETS, 'warrior_2', 'Idle.png'),
  JUMP: join(DIR_ASSETS, 'warrior_2', 'Jump.png'),
  RUN: join(DIR_ASSETS, 'warrior_2', 'Run.png')
}

HITBOX_B_WARRIOR_1 = {
  ATTACK_1: [
    (27, 40, 55, 48), (25, 40, 57, 48), (27, 34, 48, 48), (27, 34, 48, 48)
  ],
  ATTACK_2: [
    (28, 33, 48, 48), (28, 33, 48, 48), (26, 40, 56, 48), (26, 40, 56, 48)
  ],
  ATTACK_3: [
    (28, 40, 56, 48), (28, 38, 57, 48), (28, 42, 57, 48), (26, 30, 49, 48), (26, 30, 49, 48)
  ],
  DEATH: [
    (28, 38, 56, 48), (22, 32, 58, 48), (25, 27, 58, 48), (25, 27, 58, 48), (25, 23, 58, 48),
    (25, 21, 58, 48), (25, 17, 58, 48), (27, 6, 58, 48), (26, 7, 58, 48)
  ],
  FALL: [
    (28, 36, 51, 48), (28, 36, 51, 48)
  ],
  GET_HIT: [
     (28, 33, 58, 48), (25, 35, 58, 48), (25, 38, 56, 48)
  ],
  IDLE: [
    (22, 40, 55, 48), (22, 38, 55, 48), (22, 36, 55, 48), (22, 36, 55, 48), (22, 36, 55, 48),
    (22, 39, 55, 48), (22, 39, 55, 48), (22, 39, 55, 48), (22, 39, 55, 48), (22, 39, 55, 48)
  ],
  JUMP: [
    (29, 39, 47, 48), (30, 39, 47, 48)
  ],
  RUN: [
    (30, 37, 52, 48), (38, 38, 46, 48), (30, 38, 52, 48), (30, 37, 53, 48), (32, 38, 53, 48), (28, 38, 53, 48)
  ],
}

HITBOX_A_WARRIOR_1 = {
  ATTACK_1: [
    (26, 7, 91, 74), (26, 7, 92, 74), (97, 41, 12, 57), (10, 11, 38, 58)
  ],
  ATTACK_2: [
    (10, 11, 38, 58), (10, 11, 38, 58), (108, 38, 11, 61), (26, 7, 91, 74)
  ],
  ATTACK_3: [
    (25, 8, 89, 70), (23, 18, 82, 51), (22, 19, 80, 55), (103, 72, 2, 48), (22, 10, 24, 48)
  ]
}

HITBOX_B_WARRIOR_2 = {
  ATTACK_1: [
    (23, 44, 72, 62), (30, 42, 82, 62), (30, 42, 82, 62), (30, 42, 82, 62), (30, 42, 63, 62), (30, 42, 63, 62), (30, 42, 62, 62)
  ],
  ATTACK_2: [
    (22, 39, 64, 62), (24, 39, 62, 62), (22, 42, 84, 62), (22, 42, 82, 62), (22, 42, 82, 62), (22, 42, 82, 62), (22, 42, 83, 62)
  ],
  ATTACK_3: [
    (22, 42, 83, 62), (22, 42, 83, 62), (22, 42, 84, 62), (22, 40, 84, 62), (24, 30, 61, 62), (18, 30, 62, 62), (18, 32, 62, 62), (18, 33, 63, 62)
  ],
  DEATH: [
    (18, 39, 75, 62), (18, 42, 73, 62), (16, 42, 73, 62), (16, 41, 68, 62), (26, 22, 52, 62), (26, 6, 36, 62), (26, 4, 37, 62)
  ],
  FALL: [
    (16, 40, 72, 62), (16, 40, 72, 62), (15, 40, 72, 62)
  ],
  GET_HIT: [
     (17, 40, 77, 62), (17, 40, 77, 62), (17, 40, 75, 62)
  ],
  IDLE: [
    (16, 44, 73, 62), (16, 43, 73, 62), (16, 43, 73, 62), (15, 41, 73, 62), (15, 42, 73, 62),
    (16, 42, 73, 62), (16, 43, 73, 62), (16, 43, 73, 62), (16, 44, 73, 62), (16, 44, 73, 62)
  ],
  JUMP: [
    (17, 40, 70, 62), (17, 40, 70, 62), (17, 40, 70, 62)
  ],
  RUN: [
    (17, 40, 69, 62), (22, 37, 69, 62), (19, 36, 69, 62), (19, 39, 68, 62), (19, 40, 68, 62), (19, 39, 68, 62), (19, 37, 68, 62), (19, 38, 68, 62)
  ],
}

HITBOX_A_WARRIOR_2 = {
  ATTACK_1: [
    (27, 12, 63, 69), (26, 11, 117, 74), (26, 11, 116, 74), (29, 14, 108, 71), (64, 43, 30, 65), (13, 12, 70, 96), (14, 12, 70, 96)
  ],
  ATTACK_2: [
    (14, 11, 70, 97), (13, 11, 70, 97), (103, 61, 33, 61), (53, 60, 83, 62), (22, 19, 112, 103), (22, 19, 112, 103), (22, 19, 112, 103)
  ],
  ATTACK_3: [
    (22, 19, 112, 103), (14, 24, 102, 111), (9, 25, 92, 111), (28, 11, 107, 105), (104, 86, 25, 61), (26, 36, 29, 60), (25, 11, 32, 63), (25, 11, 35, 64)
  ]
}

WARRIOR_1 = {
  ATTACK_1: (FRAMES_WARRIOR_1[ATTACK_1], HITBOX_B_WARRIOR_1[ATTACK_1], HITBOX_A_WARRIOR_1[ATTACK_1]),
  ATTACK_2: (FRAMES_WARRIOR_1[ATTACK_2], HITBOX_B_WARRIOR_1[ATTACK_2], HITBOX_A_WARRIOR_1[ATTACK_2]),
  ATTACK_3: (FRAMES_WARRIOR_1[ATTACK_3], HITBOX_B_WARRIOR_1[ATTACK_3], HITBOX_A_WARRIOR_1[ATTACK_3]),
  DEATH: (FRAMES_WARRIOR_1[DEATH], HITBOX_B_WARRIOR_1[DEATH]),
  FALL: (FRAMES_WARRIOR_1[FALL], HITBOX_B_WARRIOR_1[FALL]),
  GET_HIT: (FRAMES_WARRIOR_1[GET_HIT], HITBOX_B_WARRIOR_1[GET_HIT]),
  IDLE: (FRAMES_WARRIOR_1[IDLE], HITBOX_B_WARRIOR_1[IDLE]),
  JUMP: (FRAMES_WARRIOR_1[JUMP], HITBOX_B_WARRIOR_1[JUMP]),
  RUN: (FRAMES_WARRIOR_1[RUN], HITBOX_B_WARRIOR_1[RUN])
}

WARRIOR_2 = {
  ATTACK_1: (FRAMES_WARRIOR_2[ATTACK_1], HITBOX_B_WARRIOR_2[ATTACK_1], HITBOX_A_WARRIOR_2[ATTACK_1]),
  ATTACK_2: (FRAMES_WARRIOR_2[ATTACK_2], HITBOX_B_WARRIOR_2[ATTACK_2], HITBOX_A_WARRIOR_2[ATTACK_2]),
  ATTACK_3: (FRAMES_WARRIOR_2[ATTACK_3], HITBOX_B_WARRIOR_2[ATTACK_3], HITBOX_A_WARRIOR_2[ATTACK_3]),
  DEATH: (FRAMES_WARRIOR_2[DEATH], HITBOX_B_WARRIOR_2[DEATH]),
  FALL: (FRAMES_WARRIOR_2[FALL], HITBOX_B_WARRIOR_2[FALL]),
  GET_HIT: (FRAMES_WARRIOR_2[GET_HIT], HITBOX_B_WARRIOR_2[GET_HIT]),
  IDLE: (FRAMES_WARRIOR_2[IDLE], HITBOX_B_WARRIOR_2[IDLE]),
  JUMP: (FRAMES_WARRIOR_2[JUMP], HITBOX_B_WARRIOR_2[JUMP]),
  RUN: (FRAMES_WARRIOR_2[RUN], HITBOX_B_WARRIOR_2[RUN])
}