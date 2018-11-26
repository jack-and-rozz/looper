#coding: utf-8
from collections import OrderedDict
from utils import common
from game.base import actions as acts
from game.base.consts import instance_types as itypes

class LocationBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.instance_type = itypes.Location
    self.classname = self.__class__.__name__
    self.noeffect_actions = []
    self.intrigue = 0

    # プロット時に乗っているカード
    self.actors_plot = None
    self.writers_plot = None

  def remove_actions(self):
    self.actors_plot = None
    self.writers_plot = None

  def state(self, show_hidden, as_ids):
    state = []
    state += [
      ('_id', self._id), 
      ('classname', self.classname),
      ('intrigue', self.intrigue),
    ]
    if show_hidden:
      actors_plot = self.actors_plot
      writers_plot = self.writers_plot
    else:
      actors_plot = consts.Unknown if self.actors_plot else None
      writers_plot = consts.Unknown if self.writers_plot else None
    attr = '_id' if as_ids else 'classname'

    state += [
      ("actors_plot", getattr(actors_plot, attr) if actors_plot else None),
      ("writers_plot", getattr(writers_plot, attr) if writers_plot else None),
    ]
    return OrderedDict(state)

  def change_intrigue(self, value):
    self.intrigue = max(0, self.intrigue+value)

  def apply_actions(self, actions):
    if not actions:
      return
    actions = acts.remove_forbidden_actions(actions)
    # TODO: 幻想がいる場合
    for a in [a for a in common.select_instance(actions, [acts.IntrigueAction])]:
      a(self)
    self.intrigue = max(0, self.intrigue)

class Hospital(LocationBase):
  def __init__(self):
    self.__super.__init__()
    self.point = (-1, 1)

class Shrine(LocationBase):
  def __init__(self):
    self.__super.__init__()
    self.point = (1, 1)

class City(LocationBase):
  def __init__(self):
    self.__super.__init__()
    self.point = (-1, -1)

class School(LocationBase):
  def __init__(self):
    self.__super.__init__()
    self.point = (1, -1)


name_to_class = OrderedDict((
  ('病院', Hospital),
  ('神社', Shrine),
  ('都市', City), 
  ('学校', School),
))

class_to_name = common.invert_dict(name_to_class)
classnames = [c.__name__ for c in class_to_name.keys()]
