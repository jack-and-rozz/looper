# coding:utf-8
import importlib

from utils import common
import game.base.characters as characters
import game.expansions as expansions

class Board(object):
  def __init__(self, scenerio, loop, prev_board=None):
    self.scenerio = scenerio
    self.day = 0
    self.loop = loop
    self.places = [Hospital(), Shrine(), City(), School()]
    self.expansion = importlib.import_module('game.expansions.btx')
    #print self.expansion.roles
    exit(1)
    for c, r in scenerio.characters.items():
      role = RoleBase
      #character = 

  def show(self):
    pass

class PlaceBase(object):
  def __init__(self):
    self.counters = []
    self.characters = []

class Hospital(PlaceBase):
  def __init__(self):
    self.name = '病院'
    self._id = 1 

class Shrine(PlaceBase):
  def __init__(self):
    self.name = '神社'
    self._id = 2 
     
class City(PlaceBase):
  def __init__(self):
    self.name = '都市'
    self._id = 3

class School(PlaceBase):
  def __init__(self):
    self.name = '学校'
    self._id = 4
     


