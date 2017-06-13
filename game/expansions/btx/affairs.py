# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base.affairs import AffairBase

class MurderCase(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class ParanoirExpansion(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class EvilPollution(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class Suicide(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class HospitalIncident(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class RemoteMurder(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class Missing(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class RumorSpreading(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

class ButterflyFlapping(AffairBase):
  def __init__(self, day, offender):
    super(self.__class__, self).__init__(day, offender)  

name_to_class = OrderedDict((
  ('殺人事件', MurderCase),
  ('不安拡大', ParanoirExpansion),
  ('邪気の汚染', EvilPollution),
  ('自殺', Suicide),
  ('病院の事件', HospitalIncident),
  ('遠隔殺人', RemoteMurder),
  ('行方不明', Missing),
  ('流布', RumorSpreading),
  ('蝶の羽ばたき', ButterflyFlapping),
))
class_to_name = common.invert_dict(name_to_class)
