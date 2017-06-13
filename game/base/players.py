# coding:utf-8
from utils import common
from game.base import consts
import game.base.actions as act
from game.managers.instance_manager import InstanceManager

class PlayerBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.actions = []

  @property
  def available_actions(self):
    return [action._id for action in self.actions if action.n_available != 0 and action.n_cards != 0]

  def restore_actions(self):
    for action in self.actions:
      action.restore()

  def plot_action(self, state):
    raise NotImplementedError()

class Actor(PlayerBase):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, _id):
    self.__super.__init__()
    self._id = _id
    self.actions = [
      act.MoveUp(), act.MoveDown(), act.MoveLeft(), act.MoveRight(),
      act.PlusOneGoodwill(), act.PlusTwoGoodwill(),
      act.PlusOneParanoia(), act.MinusOneParanoia(n_available=1),
      act.ForbidIntrigue(), act.ForbidMovement(),
    ]
    self.actions = InstanceManager(act.name_to_class, self.actions)

class Writer(PlayerBase):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()
    self.actions = [
      act.MoveUp(), act.MoveDown(), act.MoveLeft(), act.MoveRight(),
      act.MoveCross(), act.PlusOneParanoia(n_cards=2),
      act.MinusOneParanoia(), act.PlusOneIntrigue(),
      act.PlusTwoIntrigue(), act.ForbidGoodwill(), act.ForbidParanoir()
    ]
    self.actions = InstanceManager(act.name_to_class, self.actions)

  def plot_henchmans_position(board):
    raise NotImplementedError

class RandomActor(Actor):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, _id):
    self.__super.__init__(_id)
  def plot_action(self, state):
    print state
    exit(1)

class RandomWriter(Writer):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()
  def plot_action(self, state):
    
    print state
    exit(1)


class HumanActor(Actor):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, _id):
    self.__super.__init__(_id)

class HumanWriter(Writer):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()
  pass



