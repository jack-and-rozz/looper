# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base.rules import RuleY, RuleX

##########################
##       Rule Y
##########################

class MurderPlan(RuleY):
  def __init__(self, *args):
    self.__super.__init__(*args)

class TheSealedItem(RuleY):
  def __init__(self, *args):
    self.__super.__init__(*args)

class SignWithMe(RuleY):
  def __init__(self, *args):
    self.__super.__init__(*args)


class ChangeofFuture(RuleY):
  def __init__(self, *args):
    self.__super.__init__(*args)


class GiantTimeBomb(RuleY):
  def __init__(self, *args):
    self.__super.__init__(*args)


##########################
##       Rule X
##########################

class CircleofFriends(RuleX):
  def __init__(self, *args):
    self.__super.__init__(*args)

class ALoveAffair(RuleX):
  def __init__(self, *args):
    self.__super.__init__(*args)
 
class TheHiddenFreak(RuleX):
  def __init__(self, *args):
    self.__super.__init__(*args)
 
class AnUnsettlingRumour(RuleX):
  def __init__(self, *args):
    self.__super.__init__(*args)

class ParanoiaVirus(RuleX):
  def __init__(self, *args):
    self.__super.__init__(*args)

class ThreadsofFate(RuleX):
  def __init__(self, *args):
    self.__super.__init__(*args)

class UnknownFactorX(RuleX):
  def __init__(self, *args):
    self.__super.__init__(*args)


#class_to_name = common.invert_dict(name_to_class)

name_to_class = OrderedDict((
  # Rule Y
  ('殺人計画', MurderPlan),
  ('封印されしモノ', TheSealedItem),
  ('僕と契約しようよ！', SignWithMe),
  ('未来改変プラン', ChangeofFuture),
  ('巨大時限爆弾Xの存在', GiantTimeBomb),
  # Rule X
  ('友情サークル', CircleofFriends),
  ('恋愛風景', ALoveAffair),
  ('潜む殺人鬼', TheHiddenFreak),
  ('不穏な噂', AnUnsettlingRumour),
  ('妄想拡大ウイルス', ParanoiaVirus),
  ('因果の糸', ThreadsofFate),
  ('不定因子x', UnknownFactorX),
))

class_to_name = common.invert_dict(name_to_class)

