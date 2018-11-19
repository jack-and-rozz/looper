# coding:utf-8
import codecs, yaml, collections
from utils import common
import pandas as pd

from game.base.board import Board
import game.base.players as players

class GameManager(object):
  '''
  CUI-based.
  '''
  def __init__(self, scenerio_path):
    self.board = None
    self.leader = 0
    self.loop = 1
    self.scenerio = self.load_scenerio(scenerio_path)
    self.max_loop = self.scenerio.loop
    self.max_day = self.scenerio.days

  def init_board(self):
    self.actors = [getattr(players, actor_type)(actor_id) for actor_id, actor_type in enumerate(self.scenerio.actors)]
    self.writer = getattr(players, self.scenerio.writer)()
    self.board = Board(self.scenerio, self.loop, 
                       self.actors, self.writer, self.board)
    self.show_as_text(self.board, show_hidden=True, as_ids=True)
    return self.board.get_state(show_hidden=False)

  def load_scenerio(self, path):
    d = yaml.load(codecs.open(path, 'r', 'utf-8'))
    s = common.unicode_to_str(d, dict_func=collections.OrderedDict)
    scenerio = common.dotDict(s)
    return scenerio

  def show_as_text(self, board, show_hidden, as_ids):
    print ('-' * 40)
    print('========== Game ============')
    print ("Loop: %d" % board.loop,
           "Day : %d" % board.day,
           "Phase: %d" % board.phase,
           "Ex: %d" % board.ex_gauge)
    pd.set_option('display.width', 120)

    print('========== Place ============')
    header = list(board.places.state(show_hidden, as_ids)[0].keys())
    data = [[values for keys, values in x.items()] for x in board.places.state(show_hidden, as_ids)] 
    df = pd.DataFrame(data, columns=header).set_index(header[0])
    print(df)
    print('')

    print('========== Characters ============')
    header = list(board.characters.state(show_hidden, as_ids)[0].keys())
    data = [[values for keys, values in x.items()] for x in board.characters.state(show_hidden, as_ids)] 

    df = pd.DataFrame(data, columns=header).set_index(header[0])
    print(df)
    print('') 
    
    print('========== Affairs ============')
    header = list(board.affairs.state(show_hidden, as_ids)[0].keys())
    data = [[values for keys, values in x.items()] for x in board.affairs.state(show_hidden, as_ids)] 
    df = pd.DataFrame(data, columns=header).set_index(header[0])
    print(df)
    print('') 

    print("========== Actors' Cards ============")
    header = list(board.actors[0].state(show_hidden, as_ids).keys())
    data = [[values for keys, values in x.state(show_hidden, as_ids).items()] for x in board.actors] 
    df = pd.DataFrame(data, columns=header).set_index(header[0])
    print(df)
    print('') 
    print("========== Writer's Cards ============")
    header = list(board.writer.state(show_hidden, as_ids).keys())
    data = [[values for keys, values in board.writer.state(show_hidden, as_ids).items()]]
    df = pd.DataFrame(data, columns=header).set_index(header[0])
    print(df)
    print('') 
    print("=====================================")


  # def start_game(self):
  #   for l in xrange(1, self.max_loop):
  #     self.loop = l
  #     result = self.start_loop()
  #     return result
  #     if result == True:
  #       return True
  #   return self.final_battle()

  # def final_battle(self):
  #   res = self.actors[self.leader].plot_final_battle(board)
  #   return False

  # def day_step(self, day):
  #   # 脚本家行動フェイズ
  #   self.board.plot_writer_actions()
  #   # 主人公行動フェイズ
  #   self.board.plot_actor_actions(self.leader)
  #   # 行動解決フェイズ
  #   self.board.process_actions()
  #   # 脚本家能力フェイズ
  #   self.board.use_writer_abilities()
  #   # 主人公能力フェイズ
  #   self.board.use_actor_abilities(self.leader)
  #   # 事件フェイズ
  #   self.board.process_affairs(self.leader)
  #   # ターン終了フェイズ
  #   self.board.end_day(self.writer)
  #   #exit(1)

  # def start_loop(self):
  #   self.init_board()
  #   self.board.pre_loop(self.writer, self.actors[self.leader])
  #   for d in xrange(1, self.max_day):
  #     self.day_step(d)
  #   self.board.end_loop(self.writer)
    
