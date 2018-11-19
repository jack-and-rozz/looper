# coding:utf-8

from game.managers.game_manager import GameManager
from utils import common
import argparse, codecs, sys, collections, os
sys.path.append(os.getcwd())

import yaml
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    lambda loader, node: collections.OrderedDict(loader.construct_pairs(node)))

def game():
  m = GameManager(args.scenerio_path)
  return m

def main(args):
  m = GameManager(args.scenerio_path)
  state = m.init_board()
  print(state)
  #m.start_game()

if __name__ == "__main__":
  desc = ""
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('--scenerio_path', default='scenerios/sample.yml')
  args = parser.parse_args()
  main(args)
