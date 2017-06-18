#coding: utf-8
from collections import OrderedDict
from utils import common

class PlaceBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.counters = []
    self.classname = self.__class__.__name__
    self.noeffect_actions = []

  def apply_actions(self, actions):
    if not actions:
      return

class Hospital(PlaceBase):
  def __init__(self):
    self.__super.__init__()  

class Shrine(PlaceBase):
  def __init__(self):
    self.__super.__init__()  

class City(PlaceBase):
  def __init__(self):
    self.__super.__init__()  

class School(PlaceBase):
  def __init__(self):
    self.__super.__init__()  


name_to_class = OrderedDict((
  ('病院', Hospital),
  ('神社', Shrine),
  ('都市', City), 
  ('学校', School),
))

