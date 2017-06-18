# coding:utf-8
import random, itertools
from utils import common
from game.base.consts import to_place as ToPlace, to_character as ToCharacter
import game.base.actions as act
from game.managers.instance_manager import InstanceManager

class PlayerBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.actions = []

  @property
  def available_actions(self):
    return [action._id for action in self.actions if action.available]

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
      act.PlusTwoIntrigue(), act.ForbidGoodwill(), act.ForbidParanoia()
    ]
    self.actions = InstanceManager(act.name_to_class, self.actions)

  @property
  def available_actions(self):
    actions = self.__super.available_actions + [self.actions.get_id(act.PlusOneParanoia)]
    return actions

  def plot_henchmans_position(state):
    raise NotImplementedError

class RandomActor(Actor):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, _id):
    self.__super.__init__(_id)
  def plot_action(self, state):
    dests = set(list(itertools.product([ToPlace], state.places.ids)) + list(itertools.product([ToCharacter], state.characters.ids)))
    filled_dests = set([d for d, _ in state.actors_plots])
    dests = list(dests.difference(filled_dests))
    dest = random.choice(dests)
    action = random.choice(self.available_actions)
    res = (dest, self.actions.get(action))
    return res

class RandomWriter(Writer):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()

  def plot_action(self, state):
    dests = set(list(itertools.product([ToPlace], state.places.ids)) + list(itertools.product([ToCharacter], state.characters.ids)))
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



