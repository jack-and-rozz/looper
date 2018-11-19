# coding: utf-8
from utils import common
from game.base.consts import instance_types as itypes

class RuleBase(object):
  def __init__(self):
    pass

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

 
