# coding: utf-8
from utils import common
from game.base.consts import instance_types as itypes
from collections import OrderedDict

class RuleBase(object):
  def __init__(self, board):
    self.board = board
    self.roles = []
    self.classname = self.__class__.__name__
    pass

  def state(self, show_hidden, as_ids):
    state = []
    state += [
      ('_id', self._id), 
      ('name', self.classname),
      #('jname', self.name)
    ]
    return OrderedDict(state)

class RuleY(RuleBase):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.instance_type = itypes.RuleY

class RuleX(RuleBase):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.instance_type = itypes.RuleX

 
