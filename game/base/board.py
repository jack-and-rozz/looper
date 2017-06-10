# coding:utf-8
from utils import common

PlaceList = ['病院', '神社', '都市', '学校']
PlaceIds = common.to_ids(PlaceList, start=1)

class Board(object):
  def __init__(self, scenerio, loop, prev_board=None):
    self.scenerio = scenerio
    self.day = 0
    self.loop = loop
    self.places = [Hospital(), Shrine(), City(), School()]
    print scenerio

  def show(self):
    pass

class PlaceBase(object):
  def __init__(self):
    self.counters = []
    self.characters = []

class Hospital(PlaceBase):
  def __init__(self):
     super().__init__()
     self.name = '病院'
     self._id = 1 

class Shrine(PlaceBase):
  def __init__(self):
     super().__init__()
     self.name = '神社'
     self._id = 2 

class City(PlaceBase):
  def __init__(self):
     super().__init__()
     self.name = '都市'
     self._id = 3

class School(PlaceBase):
  def __init__(self):
     super().__init__()
     self.name = '学校'
     self._id = 4



