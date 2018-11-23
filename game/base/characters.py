# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base import consts
from game.base import locations as locations_lib
from game.base import actions as actions_lib
from game.base.character_abilities import *
from game.base.consts import character_properties as cprops
from game.base.consts import instance_types as itypes
from game.base.errors import *

class CharacterBase(object):
  def __init__(self, board, role):
    self.board = board
    self.role = role
    # ゲームを通して固定のパラメータ
    self.instance_type = itypes.Character
    self.classname = self.__class__.__name__
    self.init_location = None
    self.init_keepout = []
    self.init_prop = []
    self.abilities = []
    self.bodyguard = False # 刑事の護衛トークン

    # ゲームの中で変更され、ループを通して続くパラメータ
    self.role_revealed = False

    # ゲームの中で変更され得るが、ループの度にリセットされるパラメータ
    self.reset()

  def reset(self):
    self.paranoia = 0
    self.goodwill = 0
    self.intrigue = 0
    self.alive = True
    self.bodyguard = False

    self.location = self.board.locations[self.init_location]
    self.keepout = [self.board.locations[l] for l in self.init_keepout]
    self.prop = [p for p in self.init_prop]
    self.remove_actions()

    for ability in self.abilities:
      ability.reset()

  def remove_actions(self):
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
      ('location', self.location._id if as_ids else self.location.classname),
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

  def add_paranoia(self, value):
    self.paranoia = max(0, self.paranoia+value)

  def add_goodwill(self, value):
    self.goodwill = max(0, self.goodwill+value)

  def add_intrigue(self, value):
    self.intrigue = max(0, self.intrigue+value)

  def add_bodyguard(self):
    self.bodyguard = True

  def remove_bodyguard(self):
    self.bodyguard = False

  def reveal(self):
    #役職判明がトリガーの条件があるためメソッドにする
    self.role_revealed = True

  def die(self):
    if not self.role.unkillable or self.bodyguard:
      self.alive = False
    if self.bodyguard:
      self.remove_bodyguard()

  def revive(self):
    self.alive = True

  def is_in(self, location_class):
    '''
    - location: A class.
    '''
    if not type(location_class) == type:
      location_class = location_class.__class__

    return isinstance(self.location, location_class)

  def is_in_the_same_location(self, target):
    if target.instance_type == itypes.Character:
      return self.location == target.location
    elif target.instance_type == itypes.Location:
      return self.location == target
    else:
      return True
      #raise InvalidTargetError('This method must be called with Character or Location.')

  def has_prop(self, prop):
    return prop in self.prop

  def set_location(self, location):
    if not location in self.keepout:
      self.location = location

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
    self.move(direction, self.board.locations)

  def move(self, direction, locations):
    new_location = None
    if isinstance(self.location, locations_lib.Hospital):
      if direction[0] > 0:
        if direction[1] < 0:
          new_location = locations.get(locations_lib.School)
        else:
          new_location = locations.get(locations_lib.Shrine)
      elif direction[1] < 0:
        new_location = locations.get(locations_lib.City)

    elif isinstance(self.location, locations_lib.Shrine):
      if direction[0] < 0:
        if direction[1] < 0:
          new_location = locations.get(locations_lib.City)
        else:
          new_location = locations.get(locations_lib.Hospital)
      elif direction[1] < 0:
        new_location = locations.get(locations_lib.School)

    elif isinstance(self.location, locations_lib.City):
      if direction[0] > 0:
        if direction[1] > 0:
          new_location = locations.get(locations_lib.Shrine)
        else:
          new_location = locations.get(locations_lib.School)
      elif direction[1] > 0:
        new_location = locations.get(locations_lib.Hospital)
    elif isinstance(self.location, locations_lib.School):
      if direction[0] < 0:
        if direction[1] > 0:
          new_location = locations.get(locations_lib.Hospital)
        else:
          new_location = locations.get(locations_lib.City)
      elif direction[1] > 0:
        new_location = locations.get(locations_lib.Shrine)
    if new_location and locations.get_class(new_location) not in self.keepout:
      self.location = new_location


class BoyStudent(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [BoyStudentAbility(self)]
    self.paranoia_limit = 2
    self.init_location = locations_lib.School
    self.init_prop = [cprops.Student, cprops.Boy]

class GirlStudent(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [GirlStudentAbility(self)]
    self.paranoia_limit = 3
    self.init_location = locations_lib.School
    self.init_prop = [cprops.Student, cprops.Girl]

class RichMansDaughter(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [RichMansDaughterAbility(self)]
    self.paranoia_limit = 1
    self.init_location = locations_lib.School
    self.init_prop = [cprops.Student, cprops.Girl]

class ClassRep(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [ClassRepAbility(self)]
    self.paranoia_limit = 2
    self.init_location = locations_lib.School
    self.init_prop = [cprops.Student, cprops.Girl]

class MysteryBoy(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [MysteryBoyAbility(self)]
    self.paranoia_limit = 3
    self.init_location = locations_lib.School
    self.init_prop = [cprops.Student, cprops.Boy]

class ShrineMaiden(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [ShrineMaidenAbility(self), ShrineMaidenAbility2(self)]
    self.paranoia_limit = 2
    self.init_location = locations_lib.Shrine
    self.init_prop = [cprops.Student, cprops.Girl]
    self.init_keepout = [locations_lib.City]

class Alien(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [AlienAbility(self), AlienAbility2(self)]
    self.paranoia_limit = 3
    self.init_location = locations_lib.Shrine
    self.init_prop = [cprops.Girl]
    self.init_keepout = [locations_lib.Hospital]

# class GodlyBeing(CharacterBase):
#   def __init__(self, appearing_day):
#     super(self.__class__, self).__init__(*args)
#     self.paranoia_limit = 3
#     self.init_location = locations_lib.Shrine
#     self.init_prop = [cprops.Male, cprops.Female]
#     self.appearing_day = appearing_day

class PoliceOfficer(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [PoliceOfficerAbility(self), PoliceOfficerAbility2(self)]
    self.paranoia_limit = 3
    self.init_location = locations_lib.City
    self.init_prop = [cprops.Adult, cprops.Male]

class OfficeWorker(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [OfficeWorkerAbility(self)]
    self.paranoia_limit = 2
    self.init_location = locations_lib.City
    self.init_prop = [cprops.Adult, cprops.Male]
    self.init_keepout = [locations_lib.School]

class Informer(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [InformerAbility(self)]
    self.paranoia_limit = 3
    self.init_location = locations_lib.City
    self.init_prop = [cprops.Adult, cprops.Female]

class PopIdol(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [PopIdolAbility(self), PopIdolAbility2(self)]
    self.paranoia_limit = 2
    self.init_location = locations_lib.City
    self.init_prop = [cprops.Student, cprops.Girl]

class Journalist(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [JournalistAbility(self), JournalistAbility2(self)]

    self.paranoia_limit = 2
    self.init_location = locations_lib.City
    self.init_prop = [cprops.Adult, cprops.Male]

class Boss(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [BossAbility(self)]
    self.paranoia_limit = 4
    self.init_location = locations_lib.City
    self.init_prop = [cprops.Adult, cprops.Male]
    self.turf = None

class Doctor(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [DoctorAbility(self), DoctorAbility2(self)]
    self.paranoia_limit = 2
    self.init_location = locations_lib.Hospital
    self.init_prop = [cprops.Adult, cprops.Male]

class Patient(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.paranoia_limit = 2
    self.init_location = locations_lib.Hospital
    self.init_keepout = [locations_lib.City, locations_lib.School, locations_lib.Shrine]
    self.init_prop = [cprops.Boy]
  
class Nurse(CharacterBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.abilities = [NurseAbility(self)]
    self.paranoia_limit = 3
    self.init_location = locations_lib.Hospital
    self.init_prop = [cprops.Adult, cprops.Female]

# class HenchMan(CharacterBase):
#   def __init__(self, *args):
#     super(self.__class__, self).__init__(*args)
#     self.paranoia_limit = 1
#     self.init_location = None
#     self.init_prop = [cprops.Adult, cprops.Male]

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
