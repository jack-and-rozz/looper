# coding:utf-8
import random, itertools
from collections import OrderedDict
from utils import common
from game.base import consts, actions as act
from game.managers.instance_manager import InstanceManager

class PlayerBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.actions = []
    self.classname = self.__class__.__name__

  def restore_actions(self):
    for action in self.actions:
      action.restore()

  def plot_action(self, state):
    raise NotImplementedError()

  def plot_ability(self, state, available_abilities):
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

  def state(self, show_hidden, as_ids):
    state = [
      ('_id', self._id), 
      ('name', self.classname),
      ('PlusTwoGoodwill', self.actions[act.PlusTwoGoodwill].available),
      ('MinusOneParanoia', self.actions[act.MinusOneParanoia].available),
      ('ForbidMovement', self.actions[act.ForbidMovement].available),
    ]
    return OrderedDict(state)


class Writer(PlayerBase):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()
    self.actions = [
      act.MoveUp(), act.MoveDown(), act.MoveLeft(), act.MoveRight(),
      act.MoveCross(), act.PlusOneParanoia(), act.PlusOneParanoia(),
      act.MinusOneParanoia(), act.PlusOneIntrigue(),
      act.PlusTwoIntrigue(), act.ForbidGoodwill(), act.ForbidParanoia()
    ]
    self.actions = InstanceManager(act.name_to_class, self.actions)

  def state(self, show_hidden, as_ids):
    state = [
      ('name', self.classname),
      ('PlusTwoIntrigue', self.actions[act.PlusTwoIntrigue].available),
      ('MoveCross', self.actions[act.MoveCross].available),
    ]
    return OrderedDict(state)

  def plot_henchmans_position(state):
    raise NotImplementedError

class RandomActor(Actor):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, _id):
    self.__super.__init__(_id)

  def plot_action(self, state):
    dests = set(list(itertools.product([consts.Place], state.places.ids)) + list(itertools.product([consts.Character], state.characters.ids)))
    filled_dests = set([d for d, _ in state.plots.actors])
    dests = list(dests.difference(filled_dests))
    dest = random.choice(dests)
    action = random.choice(self.available_actions)
    res = (dest, self.actions.get(action))
    return res

  def plot_ability(self, state, available_abilities):
    return None

class RandomWriter(Writer):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()

  def plot_action(self, state):
    dests = set(list(itertools.product([consts.Place], state.places.ids)) + list(itertools.product([consts.Character], state.characters.ids)))
    dests = random.sample(dests, 3)
    actions = random.sample(self.available_actions, 3)
    res = [(d, self.actions.get(a)) for d, a in zip(dests, actions)]
    return res

class HumanActor(Actor):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, _id):
    self.__super.__init__(_id)

class HumanWriter(Writer):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()
  pass



