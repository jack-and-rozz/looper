import random
from utils.common import recDotDefaultDict
from game.base import locations, characters, consts, actions

ROOT = './images'
TRAGEDY = ROOT + '/tragedy_commons_kai'
BACKGROUND = ROOT + '/background'
BUTTON = ROOT + '/button'

title = recDotDefaultDict
title.effect = BACKGROUND + '/dd60692ac8adedd4dd51c031d50d8cb4_s.jpg'
tragedy = recDotDefaultDict()
tragedy.logo = TRAGEDY + '/logo.png'

for k in locations.classnames:
  tragedy.locations[k] = TRAGEDY + '/%s.png' % k

for _idx, classname in enumerate(characters.classnames):
  idx = _idx + 1
  tragedy.characters[classname].stand = TRAGEDY + '/chara_stand_%02d.png' % idx
  tragedy.characters[classname].alive_card = TRAGEDY + '/chara_cards_%02d_01.png' % idx
  tragedy.characters[classname].dead_card = TRAGEDY + '/chara_cards_%02d_00.png' % idx

tragedy.databoard = TRAGEDY + '/data.png'


def get_random_character_path(N):
  res = random.sample(tragedy.characters.values(), N)
  print(res)
  return res
  #return [tragedy.characters[19], tragedy.characters[0]]
