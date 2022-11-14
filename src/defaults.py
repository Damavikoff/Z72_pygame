import os
from os.path import join

FPS = 60

DEF_WIN_W = 900
DEF_WIN_H = 400
DEF_WIN_SCALE = .6

DIR_ASSETS = os.path.abspath('src/assets')

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

SCENE_SIZE = (288, 160)

SCENE_IMAGES= [
  join(DIR_ASSETS, 'scene', 'background_0.png'),
  join(DIR_ASSETS, 'scene', 'background_1.png'),
  join(DIR_ASSETS, 'scene', 'background_2.png'),
  join(DIR_ASSETS, 'scene', 'background_3.png'),
]

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

WARRIOR_1 = {
  ATTACK_1: (FRAMES_WARRIOR_1[ATTACK_1], HITBOX_B_WARRIOR_1[ATTACK_1]),
  ATTACK_2: (FRAMES_WARRIOR_1[ATTACK_2], HITBOX_B_WARRIOR_1[ATTACK_2]),
  ATTACK_3: (FRAMES_WARRIOR_1[ATTACK_3], HITBOX_B_WARRIOR_1[ATTACK_3]),
  DEATH: (FRAMES_WARRIOR_1[DEATH], HITBOX_B_WARRIOR_1[DEATH]),
  FALL: (FRAMES_WARRIOR_1[FALL], HITBOX_B_WARRIOR_1[FALL]),
  GET_HIT: (FRAMES_WARRIOR_1[GET_HIT], HITBOX_B_WARRIOR_1[GET_HIT]),
  IDLE: (FRAMES_WARRIOR_1[IDLE], HITBOX_B_WARRIOR_1[IDLE]),
  JUMP: (FRAMES_WARRIOR_1[JUMP], HITBOX_B_WARRIOR_1[JUMP]),
  RUN: (FRAMES_WARRIOR_1[RUN], HITBOX_B_WARRIOR_1[RUN])
}