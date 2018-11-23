import random
from utils.common import recDotDefaultDict
ROOT = './images'
TRAGEDY = ROOT + '/tragedy_commons_kai'
BACKGROUND = ROOT + '/background'
BUTTON = ROOT + '/button'
tragedy = recDotDefaultDict()
tragedy.logo = TRAGEDY + '/logo.png'
tragedy.characters = [TRAGEDY + '/chara_stand_%02d.png' % idx for idx in range(1, 21)]
for k in ['hospital', 'shrine', 'city', 'school']:
  tragedy.locations[k] = TRAGEDY + '/%s.png' % k

title = recDotDefaultDict
title.effect = BACKGROUND + '/dd60692ac8adedd4dd51c031d50d8cb4_s.jpg'

def get_random_character_path(N):
  return random.sample(tragedy.characters, N)
  #return [tragedy.characters[19], tragedy.characters[0]]
