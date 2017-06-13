# coding:utf-8

from game.managers.game_manager import GameManager
from utils import common
import argparse, codecs, sys, collections

import yaml
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: collections.OrderedDict(loader.construct_pairs(node)))

def load_scenerio(path):
  #d = yaml.load(open(path))
  d = yaml.load(codecs.open(path, 'r', 'utf-8'))
  return common.unicode_to_str(d, dict_func=collections.OrderedDict)

def main(args):
  scenerio = common.dotDict(load_scenerio("scenerios/sample.yml"))
  #common.dict_print(scenerio)
  m = GameManager(scenerio)
  m.start_game()
  
if __name__ == "__main__":
  desc = ""
  parser = argparse.ArgumentParser(description=desc)
  args = parser.parse_args()
  main(args)
