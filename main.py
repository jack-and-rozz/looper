# coding:utf-8

from game.managers.game_manager import GameManager
from utils import common
import argparse, codecs, sys, collections

import yaml
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: collections.OrderedDict(loader.construct_pairs(node)))

ROOT_PATH = '/Users/rozz/workspace/working/rooper'
SCENERIO_PATH = ROOT_PATH + '/scenerios'
sys.path.append(ROOT_PATH)

def game():
  m = GameManager(SCENERIO_PATH + "/sample.yml")
  return m

def main(args):
  m = GameManager(SCENERIO_PATH + "/sample.yml")
  m.start_game()

if __name__ == "__main__":
  desc = ""
  parser = argparse.ArgumentParser(description=desc)
  args = parser.parse_args()
  main(args)
