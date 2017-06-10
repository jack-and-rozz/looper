# coding:utf-8
from game.base.board import Board
from game.base.players import Actor, Writer

class GameManager(object):
  def __init__(self, scenerio):
    self.board = None
    self.actors = [Actor() for _ in xrange(3)]
    self.writer = Writer()
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
    pass

  def start_loop(self, loop):
    self.board = Board(self.scenerio, loop, self.board)
    exit(1)
    for d in xrange(1, self.max_day):
      self.day_step()
    
    pass
