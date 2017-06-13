# coding:utf-8
from collections import OrderedDict
from utils import common

class ActionBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, n_cards=1, n_available=None):
    self.usable = True
    self.n_available = n_available
    self.n_cards = n_cards
    self._n_cards = n_cards

  def restore(self):
    self.n_cards = self._n_cards

class MoveUp(ActionBase):
  def __init__(self):
    self.__super.__init__()

class MoveDown(ActionBase):
  def __init__(self):
    self.__super.__init__()

class MoveLeft(ActionBase):
  def __init__(self):
    self.__super.__init__()

class MoveRight(ActionBase):
  def __init__(self):
    self.__super.__init__()

class PlusOneGoodwill(ActionBase):
  def __init__(self):
    self.__super.__init__()

class PlusOneParanoia(ActionBase):
  def __init__(self, n_cards=1):
    self.__super.__init__(n_cards=n_cards)

class MinusOneParanoia(ActionBase):
  def __init__(self, n_available=None):
    self.__super.__init__(n_available=n_available)

class PlusTwoGoodwill(ActionBase):
  def __init__(self):
    self.__super.__init__(n_available=1)


class ForbidIntrigue(ActionBase):
  def __init__(self):
    self.__super.__init__()

class ForbidMovement(ActionBase):
  def __init__(self):
    self.__super.__init__(n_available=1)

class MoveCross(ActionBase):
  def __init__(self):
    self.__super.__init__(n_available=1)

class ForbidGoodwill(ActionBase):
  def __init__(self):
    self.__super.__init__()

class ForbidParanoir(ActionBase):
  def __init__(self):
    self.__super.__init__()

class PlusOneIntrigue(ActionBase):
  def __init__(self):
    self.__super.__init__()

class PlusTwoIntrigue(ActionBase):
  def __init__(self):
    self.__super.__init__(n_available=1)


name_to_class = OrderedDict((
  ('移動上', MoveUp),
  ('移動下', MoveDown),
  ('移動左', MoveLeft),
  ('移動右', MoveRight),
  ('移動斜', MoveCross),
  ('友好+1', PlusOneGoodwill),
  ('友好+2', PlusTwoGoodwill),
  ('不安+1', PlusOneParanoia),
  ('不安-1', MinusOneParanoia),
  ('暗躍+1', PlusOneIntrigue),
  ('暗躍+2', PlusTwoIntrigue),
  ('友好禁止', ForbidGoodwill),
  ('不安禁止', ForbidParanoir),
  ('暗躍禁止', ForbidIntrigue),
  ('移動禁止', ForbidMovement),
))
