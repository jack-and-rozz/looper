# coding:utf-8
from collections import OrderedDict
from game.base import consts
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

class Pass(ActionBase):
  pass

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
  def __call__(self, target):
    return (0, 2)

class MoveDown(MovementAction):
  def __init__(self):
    self.__super.__init__()

  def __call__(self, target):
    return (0, -2)

class MoveLeft(MovementAction):
  def __init__(self):
    self.__super.__init__()
  def __call__(self, target):
    return (-2, 0)

class MoveRight(MovementAction):
  def __init__(self):
    self.__super.__init__()
  def __call__(self, target):
    return (2, 0)

class MoveCross(MovementAction):
  def __init__(self):
    self.__super.__init__(n_available=1)
  def __call__(self, target):
    movex = target.position.point[0] * -2
    movey = target.position.point[1] * -2
    return (movex, movey)

class PlusOneParanoia(ParanoiaAction):
  def __init__(self, n_cards=1):
    self.__super.__init__(n_cards=n_cards)
  def __call__(self, target):
    target.paranoia += 1

class MinusOneParanoia(ParanoiaAction):
  def __init__(self, n_available=None):
    self.__super.__init__(n_available=n_available)
  def __call__(self, target):
    target.paranoia -= 1


class ForbidParanoia(ParanoiaAction):
  def __init__(self):
    self.__super.__init__()

class PlusOneGoodwill(GoodwillAction):
  def __init__(self):
    self.__super.__init__()
  def __call__(self, target):
    target.goodwill += 1

class PlusTwoGoodwill(GoodwillAction):
  def __init__(self):
    self.__super.__init__(n_available=1)
  def __call__(self, target):
    target.goodwill += 2

class ForbidGoodwill(GoodwillAction):
  def __init__(self):
    self.__super.__init__()

class PlusOneIntrigue(IntrigueAction):
  def __init__(self):
    self.__super.__init__()
  def __call__(self, target):
    target.intrigue += 1

class PlusTwoIntrigue(IntrigueAction):
  def __init__(self):
    self.__super.__init__(n_available=1)
  def __call__(self, target):
    target.intrigue += 2

class ForbidIntrigue(IntrigueAction):
  def __init__(self):
    self.__super.__init__()

def remove_forbidden_actions(a):
  if common.include_instance(a, ForbidIntrigue):
    a = common.remove_instance(a, [IntrigueAction])
  if common.include_instance(a, ForbidMovement):
    a = common.remove_instance(a, [MovementAction])
  if common.include_instance(a, ForbidGoodwill):
    a = common.remove_instance(a, [GoodwillAction])
  if common.include_instance(a, ForbidParanoia):
    a = common.remove_instance(a, [ParanoiaAction])
  return a



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
