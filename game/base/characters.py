# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base import consts
from game.base import places as places_lib
from game.base import actions as actions_lib
from game.base.character_abilities import *
from game.base.consts import character_properties as cprops
from game.base.consts import instance_types as itypes
from game.base.errors import *

class CharacterBase(object):
  def __init__(self, board):
    self.board = board
    self.instance_type = itypes.Character
    self.classname = self.__class__.__name__
    self.paranoia = 0 # 不安
    self.goodwill = 0 # 友好
    self.intrigue = 0 # 暗躍
    self.abilities = []
    self.keepout = []
    self.prop = []
    self.place = None
    self.role = None
    self.role_revealed = False
    self.alive = True

    # プロット時に乗っているカード
    self.actors_plot = None
    self.writers_plot = None

  def state(self, show_hidden, as_ids):
    state = []
    state += [
      ('_id', self._id), 
      ('name', self.classname),
      #('jname', self.name)
    ]
    state += [
      ('place', self.place._id if as_ids else self.place.classname),
      ('alive', self.alive),
      ('paranoia', self.paranoia),
      ('goodwill', self.goodwill),
      ('intrigue', self.intrigue),
    ]

    if show_hidden:
      role = self.role
      actors_plot = self.actors_plot
      writers_plot = self.writers_plot
    else:
      role = consts.Unknown
      actors_plot = consts.Unknown if self.actors_plot else None
      writers_plot = consts.Unknown if self.writers_plot else None
    attr = '_id' if as_ids else 'classname'
    state += [
      ('role', getattr(role, attr)),
      ("actors_plot", getattr(actors_plot, attr) if actors_plot else None),
      ("writers_plot", getattr(writers_plot, attr) if writers_plot else None),
    ]
    return OrderedDict(state)

  def change_paranoia(self, value):
    self.paranoia = max(0, self.paranoia+value)

  def change_goodwill(self, value):
    self.goodwill = max(0, self.goodwill+value)

  def change_intrigue(self, value):
    self.intrigue = max(0, self.intrigue+value)

  def reveal(self):
    #役職判明がトリガーの条件があるためメソッドにする
    self.role_revealed = True

  def die(self):
    if not self.role.immortal:
      self.alive = False

  def revive(self):
    self.alive = True

  def is_in(self, place_class):
    '''
    - place: A class.
    '''
    if not type(place_class) == type:
      place_class = place_class.__class__

    return isinstance(self.place, place_class)

  def is_in_the_same_place(self, target):
    if target.instance_type == itypes.Character:
      return self.place == target.place
    elif target.instance_type == itypes.Place:
      return self.place == target
    else:
      raise InvalidTargetError('This method must be called with Character or Place.')

  def has_prop(self, prop):
    return prop in self.prop

  def set_role(self, role):
    self.role = role

  def set_place(self, place):
    if not place in self.keepout:
      self.place = place

  def apply_actions(self, actions):
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
    self.move(direction, self.board.places)

  def move(self, direction, places):
    new_place = None
    if isinstance(self.place, places_lib.Hospital):
      if direction[0] > 0:
        if direction[1] < 0:
          new_place = places.get(places_lib.School)
        else:
          new_place = places.get(places_lib.Shrine)
      elif direction[1] < 0:
        new_place = places.get(places_lib.City)

    elif isinstance(self.place, places_lib.Shrine):
      if direction[0] < 0:
        if direction[1] < 0:
          new_place = places.get(places_lib.City)
        else:
          new_place = places.get(places_lib.Hospital)
      elif direction[1] < 0:
        new_place = places.get(places_lib.School)

    elif isinstance(self.place, places_lib.City):
      if direction[0] > 0:
        if direction[1] > 0:
          new_place = places.get(places_lib.Shrine)
        else:
          new_place = places.get(places_lib.School)
      elif direction[1] > 0:
        new_place = places.get(places_lib.Hospital)
    elif isinstance(self.place, places_lib.School):
      if direction[0] < 0:
        if direction[1] > 0:
          new_place = places.get(places_lib.Hospital)
        else:
          new_place = places.get(places_lib.City)
      elif direction[1] > 0:
        new_place = places.get(places_lib.Shrine)
    if new_place and places.get_class(new_place) not in self.keepout:
      self.place = new_place


class BoyStudent(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [BoyStudentAbility(self)]
    self.paranoia_limit = 2
    self.init_place = places_lib.School
    self.prop = [cprops.Student, cprops.Boy]

class GirlStudent(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [GirlStudentAbility(self)]
    self.paranoia_limit = 3
    self.init_place = places_lib.School
    self.prop = [cprops.Student, cprops.Girl]

class RichMansDaughter(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [RichMansDaughterAbility(self)]
    self.paranoia_limit = 1
    self.init_place = places_lib.School
    self.prop = [cprops.Student, cprops.Girl]

class ClassRep(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [ClassRepAbility(self)]
    self.paranoia_limit = 2
    self.init_place = places_lib.School
    self.prop = [cprops.Student, cprops.Girl]

class MysteryBoy(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [MysteryBoyAbility(self)]
    self.paranoia_limit = 3
    self.init_place = places_lib.School
    self.prop = [cprops.Student, cprops.Boy]

class ShrineMaiden(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [ShrineMaidenAbility(self), ShrineMaidenAbility2(self)]
    self.paranoia_limit = 2
    self.init_place = places_lib.Shrine
    self.prop = [cprops.Student, cprops.Girl]
    self.keepout = [places_lib.City]

class Alien(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [AlienAbility(self), AlienAbility2(self)]
    self.paranoia_limit = 3
    self.init_place = places_lib.Shrine
    self.prop = [cprops.Girl]
    self.keepout = [places_lib.Hospital]

# class GodlyBeing(CharacterBase):
#   def __init__(self, appearing_day):
#     super(self.__class__, self).__init__(*args)
#     self.paranoia_limit = 3
#     self.init_place = places_lib.Shrine
#     self.prop = [cprops.Male, cprops.Female]
#     self.appearing_day = appearing_day

class PoliceOfficer(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [PoliceOfficerAbility(self), PoliceOfficerAbility2(self)]
    self.paranoia_limit = 3
    self.init_place = places_lib.City
    self.prop = [cprops.Adult, cprops.Male]

class OfficeWorker(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [OfficeWorkerAbility(self)]
    self.paranoia_limit = 2
    self.init_place = places_lib.City
    self.prop = [cprops.Adult, cprops.Male]
    self.keepout = [places_lib.School]

class Informer(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [InformerAbility(self)]
    self.paranoia_limit = 3
    self.init_place = places_lib.City
    self.prop = [cprops.Adult, cprops.Female]

class PopIdol(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [PopIdolAbility(self), PopIdolAbility2(self)]
    self.paranoia_limit = 2
    self.init_place = places_lib.City
    self.prop = [cprops.Student, cprops.Girl]

class Journalist(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [JournalistAbility(self), JournalistAbility2(self)]

    self.paranoia_limit = 2
    self.init_place = places_lib.City
    self.prop = [cprops.Adult, cprops.Male]

class Boss(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [BossAbility(self)]
    self.paranoia_limit = 4
    self.init_place = places_lib.City
    self.prop = [cprops.Adult, cprops.Male]
    self.territory = None

class Doctor(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [DoctorAbility(self), DoctorAbility2(self)]
    self.paranoia_limit = 2
    self.init_place = places_lib.Hospital
    self.prop = [cprops.Adult, cprops.Male]

class Patient(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.paranoia_limit = 2
    self.init_place = places_lib.Hospital
    self.prop = [cprops.Boy]
    self.keepout = [places_lib.City, places_lib.School, places_lib.Shrine]

class Nurse(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [NurseAbility(self)]
    self.paranoia_limit = 3
    self.init_place = places_lib.Hospital
    self.prop = [cprops.Adult, cprops.Female]

# class HenchMan(CharacterBase):
#   def __init__(self, *args):
#     super(self.__class__, self).__init__(*args)
#     self.paranoia_limit = 1
#     self.init_place = None
#     self.prop = [cprops.Adult, cprops.Male]

name_to_class = OrderedDict((
  ('男子学生', BoyStudent),
  ('女子学生', GirlStudent),
  ('お嬢様', RichMansDaughter),
  ('委員長', ClassRep),
  ('イレギュラー', MysteryBoy),
  ('巫女', ShrineMaiden),
  ('異世界人', Alien),
  ('刑事', PoliceOfficer),
  ('サラリーマン', OfficeWorker),
  ('情報屋', Informer),
  ('アイドル', PopIdol),
  ('マスコミ', Journalist),
  ('大物', Boss),
  ('医者', Doctor),
  ('入院患者', Patient),
  ('ナース',  Nurse),

  #('神格', GodlyBeing),
  #('手先',  HenchMan),
))

class_to_name = common.invert_dict(name_to_class)
