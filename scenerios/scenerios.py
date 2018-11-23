# coding: utf-8

import yaml, codecs, collections
import glob 
from utils import common

def load_scenerio(path):
  d = yaml.load(codecs.open(path, 'r', 'utf-8'))
  s = common.unicode_to_str(d, dict_func=collections.OrderedDict)
  scenerio = common.recDotDict(s)
  return scenerio

def load_all(scenerios_dir='scenerios'):
  return [load_scenerio(path) for path in glob.glob(scenerios_dir + '/*.yml')]
