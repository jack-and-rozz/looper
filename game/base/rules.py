# coding: utf-8
from utils import common

class RuleBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.__super.__init__()  

# class RuleX(RuleBase):
#   __metaclass__ = common.SuperSyntaxSugarMeta
#   def __init__(self):
#     self.__super.__init__()  

# class RuleY(RuleBase):
#   __metaclass__ = common.SuperSyntaxSugarMeta
#   def __init__(self):
#     self.__super.__init__()  
