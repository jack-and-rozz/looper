# coding:utf-8
import codecs, yaml, collections
from utils import common
from game.base.board import Board
import game.base.players as players

class GameManager(object):
  def __init__(self, scenerio_path):
    self.board = None
    self.leader = 0
    self.loop = 1
    self.scenerio = self.load_scenerio(scenerio_path)
    self.max_loop = self.scenerio.loop
    self.max_day = self.scenerio.days
  def load_scenerio(self, path):
    d = yaml.load(codecs.open(path, 'r', 'utf-8'))
    s = common.unicode_to_str(d, dict_func=collections.OrderedDict)
    scenerio = common.dotDict(s)
    return scenerio

  def state(self):
    return self.board.get_state()

  def start_game(self):
    for l in xrange(1, self.max_loop):
      result = self.start_loop(l)
      return result
      if result == True:
        return True
    return self.final_battle()

  def final_battle(self):
    res = self.actors[self.leader].plot_final_battle(board)
    return False

  def day_step(self):
    # 脚本家行動フェイズ
    self.board.plot_writer_actions()
    # 主人公行動フェイズ
    self.board.plot_actor_actions(self.leader)
    # 行動解決フェイズ
    self.board.process_actions()
    # 脚本家能力フェイズ
    self.board.use_writer_abilities()
    # 主人公能力フェイズ
    self.board.use_actor_abilities(self.leader)
    # 事件フェイズ
    self.board.process_affairs(self.leader)
    # ターン終了フェイズ
    self.board.end_day()
    exit(1)

  def start_loop(self, loop):
    self.actors = [getattr(players, actor_type)(actor_id) for actor_id, actor_type in enumerate(self.scenerio.actors)]
    self.writer = getattr(players, self.scenerio.writer)()
    self.board = Board(self.scenerio, loop, self.actors, self.writer, self.board)
    #self.board.show_as_text()
    #return self.board.get_state()


    self.board.pre_loop(self.writer, self.actors[self.leader])
    for d in xrange(1, self.max_day):
      self.day_step()
    self.board.end_loop(self.writer)
