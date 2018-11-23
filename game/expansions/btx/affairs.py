# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base.affairs import AffairBase

class MurderCase(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class IncreasingUnease(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class FoulEvil(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class Suicide(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class HospitalIncident(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class FarawayMurder(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class MissingPerson(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class Spreading(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class ButterflyEffect(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

name_to_class = OrderedDict((
  ('殺人事件', MurderCase),
  ('不安拡大', IncreasingUnease),
  ('邪気の汚染', FoulEvil),
  ('自殺', Suicide),
  ('病院の事件', HospitalIncident),
  ('遠隔殺人', FarawayMurder),
  ('行方不明', MissingPerson),
  ('流布', Spreading),
  ('蝶の羽ばたき', ButterflyEffect),
))
class_to_name = common.invert_dict(name_to_class)
