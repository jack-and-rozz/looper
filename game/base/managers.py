# coding:utf-8
from game.base.board import Board
import game.base.players as players

#生成したインスタンスとIDとの関連付け
class InstanceManager(object):
  def __init__(self, name_to_instance, instances):
    self.name_to_instance
    self.instances = instances
    self.instanceIds = dict(zip(self.name_to_instance.values(), xrange(self.name_to_instance)))
    print self.instanceIds
    exit(1)
  def get(self, _id):
    pass
  def to_id(self, inst):
    pass


class GameManager(object):
  def __init__(self, scenerio):
    self.board = None
    self.actors = [getattr(players, actor_type)() for actor_type in scenerio.actors]
    self.writer = getattr(players, scenerio.writer)()
    self.leader = 0
    self.loop = 1
    self.scenerio = scenerio
    self.max_loop = scenerio.loop
    self.max_day = scenerio.days

  def start_game(self):
    for l in xrange(1, self.max_loop):
      result = self.start_loop(l)
      if result == True:
        return True
    return self.final_battle()

  def final_battle(self):
    return False

  def day_step(self):
    # 脚本家行動フェイズ
    self.writer.plot_action(self.board)
    # 主人公行動フェイズ
    for player in self.players:
      player.plot_action(self.board)
      pass
    # 脚本家能力フェイズ
    # 主人公能力フェイズ
    # 事件フェイズ
    # ターン終了フェイズ
    pass
    exit(1)

  def start_loop(self, loop):
    self.board = Board(self.scenerio, loop, self.board)
    self.board.show()
    for d in xrange(1, self.max_day):
      self.day_step()
    
    pass
