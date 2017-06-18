# coding:utf-8
from collections import OrderedDict
from utils import common

class ActionBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, n_cards=1, n_available=None):
    self.available = True
    self.n_available = n_available

  def consume(self):
    if self.n_available != None:
      self.n_available -= 1
      if self.n_available <= 0:
        self.available = False

  def __call__(self, target):
    return

class GoodwillAction(ActionBase):
  __metaclass__ = common.SuperSyntaxSugarMeta

class IntrigueAction(ActionBase):
  __metaclass__ = common.SuperSyntaxSugarMeta

class ParanoiaAction(ActionBase):
  __metaclass__ = common.SuperSyntaxSugarMeta

class MovementAction(ActionBase):
  __metaclass__ = common.SuperSyntaxSugarMeta

class ForbidMovement(MovementAction):
  def __init__(self):
    self.__super.__init__(n_available=1)

class MoveUp(MovementAction):
  def __init__(self):
    self.__super.__init__()

class MoveDown(MovementAction):
  def __init__(self):
    self.__super.__init__()

class MoveLeft(MovementAction):
  def __init__(self):
    self.__super.__init__()

class MoveRight(MovementAction):
  def __init__(self):
    self.__super.__init__()

class MoveCross(MovementAction):
  def __init__(self):
    self.__super.__init__(n_available=1)

class PlusOneParanoia(ParanoiaAction):
  def __init__(self, n_cards=1):
    self.__super.__init__(n_cards=n_cards)

class MinusOneParanoia(ParanoiaAction):
  def __init__(self, n_available=None):
    self.__super.__init__(n_available=n_available)

class ForbidParanoia(ParanoiaAction):
  def __init__(self):
    self.__super.__init__()

class PlusOneGoodwill(GoodwillAction):
  def __init__(self):
    self.__super.__init__()

class PlusTwoGoodwill(GoodwillAction):
  def __init__(self):
    self.__super.__init__(n_available=1)

class ForbidGoodwill(GoodwillAction):
  def __init__(self):
    self.__super.__init__()

class PlusOneIntrigue(IntrigueAction):
  def __init__(self):
    self.__super.__init__()

class PlusTwoIntrigue(IntrigueAction):
  def __init__(self):
    self.__super.__init__(n_available=1)

class ForbidIntrigue(IntrigueAction):
  def __init__(self):
    self.__super.__init__()

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
  ('不安禁止', ForbidParanoia),
  ('暗躍禁止', ForbidIntrigue),
  ('移動禁止', ForbidMovement),
))
