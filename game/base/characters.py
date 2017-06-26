# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base import consts
from game.base import places as places_lib
from game.base import actions as actions_lib
from game.base import character_abilities as cabi_lib
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

  def apply_actions(self, actions, places):
    if not actions:
      return
    actions = actions_lib.remove_forbidden_actions(actions)
    counter_action_types = [
      actions_lib.IntrigueAction,
      actions_lib.GoodwillAction,
      actions_lib.ParanoiaAction,
    ]
    for a in [a for a in common.select_instance(actions, counter_action_types)]:
      a(self)
    self.goodwill = max(0, self.goodwill)
    self.intrigue = max(0, self.intrigue)
    self.paranoia = max(0, self.paranoia)

    move_action_types = [
      actions_lib.MoveRight,
      actions_lib.MoveLeft,
      actions_lib.MoveUp,
      actions_lib.MoveDown,
      actions_lib.MoveCross
    ]
    direction = (0, 0)
    for a in [a for a in common.select_instance(actions, move_action_types)]:
      direction = [d1 + d2 for d1, d2 in zip(direction, a(self))]
    self.move(direction, places)

  def move(self, direction, places):
    new_position = None
    if isinstance(self.position, places_lib.Hospital):
      if direction[0] > 0:
        if direction[1] < 0:
          new_position = places.get(places_lib.School)
        else:
          new_position = places.get(places_lib.Shrine)
      elif direction[1] < 0:
        new_position = places.get(places_lib.City)

    elif isinstance(self.position, places_lib.Shrine):
      if direction[0] < 0:
        if direction[1] < 0:
          new_position = places.get(places_lib.City)
        else:
          new_position = places.get(places_lib.Hospital)
      elif direction[1] < 0:
        new_position = places.get(places_lib.School)

    elif isinstance(self.position, places_lib.City):
      if direction[0] > 0:
        if direction[1] > 0:
          new_position = places.get(places_lib.Shrine)
        else:
          new_position = places.get(places_lib.School)
      elif direction[1] > 0:
        new_position = places.get(places_lib.Hospital)
    elif isinstance(self.position, places_lib.School):
      if direction[0] < 0:
        if direction[1] > 0:
          new_position = places.get(places_lib.Hospital)
        else:
          new_position = places.get(places_lib.City)
      elif direction[1] > 0:
        new_position = places.get(places_lib.Shrine)
    if new_position and places.get_class(new_position) not in self.keepout:
      self.position = new_position

class BoyStudent(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [2]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.School
    self.prop = [cprop.Student, cprop.Boy]

class GirlStudent(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [2]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = places_lib.School
    self.prop = [cprop.Student, cprop.Girl]
    self.requisite_goodwills = [2]

class RichMansDaughter(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [3]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 1
    self.init_position = places_lib.School
    self.prop = [cprop.Student, cprop.Girl]

class ClassRep(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [2]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.School
    self.prop = [cprop.Student, cprop.Girl]

class MysteryBoy(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [3]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = places_lib.School
    self.prop = [cprop.Student, cprop.Boy]

class ShrineMaiden(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [3, 5]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.Shrine
    self.prop = [cprop.Student, cprop.Girl]
    self.keepout = [places_lib.City]

class Alien(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [4, 5]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = places_lib.Shrine
    self.prop = [cprop.Girl]
    self.keepout = [places_lib.Hospital]

class GodlyBeing(CharacterBase):
  def __init__(self, appearing_day):
    self.requisite_goodwills = [3, 5]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = places_lib.Shrine
    self.appearing_day = appearing_day
    self.prop = [cprop.Male, cprop.Female]

class PoliceOfficer(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [4, 5]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = places_lib.City
    self.prop = [cprop.Adult, cprop.Male]

class OfficeWorker(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [3]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.City
    self.prop = [cprop.Adult, cprop.Male]
    self.keepout = [places_lib.School]

class Informer(CharacterBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = places_lib.City
    self.prop = [cprop.Adult, cprop.Female]

class PopIdol(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [3, 4]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.City
    self.prop = [cprop.Student, cprop.Girl]

class Journalist(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [2, 2]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.City
    self.prop = [cprop.Adult, cprop.Male]

class Boss(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [5]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 4
    self.init_position = places_lib.City
    self.prop = [cprop.Adult, cprop.Male]

class Doctor(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [2, 3]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.Hospital
    self.prop = [cprop.Adult, cprop.Male]

class Patient(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = []
    super(self.__class__, self).__init__()
    self.paranoia_limit = 2
    self.init_position = places_lib.Hospital
    self.prop = [cprop.Boy]
    self.keepout = [places_lib.City, places_lib.School, places_lib.Shrine]

class Nurse(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [2]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 3
    self.init_position = places_lib.Hospital
    self.prop = [cprop.Adult, cprop.Female]

class HenchMan(CharacterBase):
  def __init__(self):
    self.requisite_goodwills = [3]
    super(self.__class__, self).__init__()
    self.paranoia_limit = 1
    self.init_position = places_lib.Hospital # (仮)
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
