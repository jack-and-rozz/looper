# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base import places
from game.base.consts import character_properties as cprop

class CharacterBase(object):
  def __init__(self):
    self.paranoia = 0 # 不安
    self.goodwill = 0 # 友好
    self.intrigue = 0 # 暗躍
    self.counters = []
    self.keepout = []
    self.position = None
    self.role = None
    self.alive = True
    self.classname = self.__class__.__name__

  def set_role(self, role):
    self.role = role

  def set_position(self, place):
    if not place in self.keepout:
      self.position = place

  def apply_actions(self, actions):
    if not actions:
      return

  def move(self, direction):
    if isinstance(self.position, places.Hospital):
      pass
    elif isinstance(self.position, places.Shrine):
      pass
    elif isinstance(self.position, places.City):
      pass
    elif isinstance(self.position, places.School):
      pass

class BoyStudent(CharacterBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = '学校'
    self.prop = [cprop.Student, cprop.Boy]

class GirlStudent(CharacterBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = '学校'
    self.prop = [cprop.Student, cprop.Girl]

class RichMansDaughter(CharacterBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.paranoia_limit = 1
    self.init_position = '学校'
    self.prop = [cprop.Student, cprop.Girl]

class ClassRep(CharacterBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = '学校'
    self.prop = [cprop.Student, cprop.Girl]

class MysteryBoy(CharacterBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = '学校'
    self.prop = [cprop.Student, cprop.Boy]

class ShrineMaiden(CharacterBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = '神社'
    self.prop = [cprop.Student, cprop.Girl]

class Alien(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 3
     self.init_position = '神社'
     self.prop = [cprop.Girl]

class GodlyBeing(CharacterBase):
  def __init__(self, appearing_day):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 3
     self.init_position = '神社'
     self.appearing_day = appearing_day
     self.prop = [cprop.Male, cprop.Female]

class PoliceOfficer(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 3
     self.init_position = '都市'
     self.prop = [cprop.Adult, cprop.Male]

class OfficeWorker(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 2
     self.init_position = '都市'
     self.prop = [cprop.Adult, cprop.Male]

class Informer(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 3
     self.init_position = '都市'
     self.prop = [cprop.Adult, cprop.Female]

class PopIdol(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 2
     self.init_position = '都市'
     self.prop = [cprop.Student, cprop.Girl]

class Journalist(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 2
     self.init_position = '都市'
     self.prop = [cprop.Adult, cprop.Male]

class Boss(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 4
     self.init_position = '都市'
     self.prop = [cprop.Adult, cprop.Male]

class Doctor(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 2
     self.init_position = '病院'
     self.prop = [cprop.Adult, cprop.Male]

class Patient(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 2
     self.init_position = '病院'
     self.prop = [cprop.Boy]

class Nurse(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 3
     self.init_position = '病院'
     self.prop = [cprop.Adult, cprop.Female]

class HenchMan(CharacterBase):
  def __init__(self):
     super(self.__class__, self).__init__()
     self.paranoia_limit = 1
     self.init_position = '病院' # (仮)
     self.prop = [cprop.Adult, cprop.Male]

name_to_class = OrderedDict((
  ('男子学生', BoyStudent),
  ('女子学生', GirlStudent),
  ('お嬢様', RichMansDaughter),
  ('委員長', ClassRep),
  ('イレギュラー', MysteryBoy),
  ('巫女', ShrineMaiden),
  ('異世界人', Alien),
  ('神格', GodlyBeing),
  ('刑事', PoliceOfficer),
  ('サラリーマン', OfficeWorker),
  ('情報屋', Informer),
  ('アイドル', PopIdol),
  ('マスコミ', Journalist),
  ('大物', Boss),
  ('医者', Doctor),
  ('入院患者', Patient),
  ('ナース',  Nurse),
  ('手先',  HenchMan),
))

class_to_name = common.invert_dict(name_to_class)
