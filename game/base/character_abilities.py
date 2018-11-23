# coding: utf-8
from utils import common
from game.base.consts import character_properties as cprop
from game.base.consts import instance_types as itypes
from game.base.consts import phases

from game.base.errors import *
from game.base.locations import *

class CharacterAbilityBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, character):
    self.goodwill = 0
    self.character = character
    self.refusable = True # 友好無視で拒否可能かどうか
    self.betrayal = False # 友好暴発
    self.consumed = False # 1回限りの能力を使ったかどうか
    self.same_location_with_target = False # 対象と同一エリアである必要があるか (多いのでまとめる)
    self.target_is_alive = True # 対象が生きている必要があるか（キャラクタ限定）
    self.target_types = [] # 対象のタイプ (Character, Location, ...)
    self.available_phase = phases.ActorsAbility # 使用可能なタイミング

  def consume(self):
    self.consumed = True

  def reset(self):
    self.consumed = False

  def available(self, target):
    '''
    システム的な友好能力の使用可否判定。拒否するかどうかは別に判定する。
    '''
    res = character.goodwill >= self.goodwill and not self.consumed
    if self.same_location_with_target:
      res = res and self.character.is_in_the_same_location(target)
    if self.target_is_alive and target.instance_type == itypes.Character:
      res = res and target.alive
    return res


class BoyStudentAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 2
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    target.add_paranoia(-1)

  def available(self, target):
    return self.__super.available(target) and target.has_prop(cprop.Student) and target != self.character

GirlStudentAbility = BoyStudentAbility

class RichMansDaughterAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 3
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Character
    target.add_goodwill(1)

  def available(self, target):
    if self.__super.available(target):
      if self.character.is_in(School) or self.character.is_in(City):
        return True
    return False

class ClassRepAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 2
    self.target_types = [itypes.Action]

  def __call__(self, target):
    # target: Action
    target.reset()
    self.consume()

  def available(self, target):
    return self.__super.available(target) and not target.available

class MysteryBoyAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.refusable = False
    self.goodwill = 3
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Character (self)
    target.reveal()

  def available(self, target):
    return self.__super.available(target) and target == self.character and self.board.loop != 1


class ShrineMaidenAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 3
    self.target_types = [itypes.Location]

  def __call__(self, target):
    # target: Location
    target.add_intrigue(-1)

  def available(self, target):
    if self.__super.available(target) and self.character.is_in(Shrine) and isinstance(target, Shrine):
      return True
    return False

class ShrineMaidenAbility2(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 5
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Character
    target.reveal()
    self.consume()


class AlienAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 4
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Character
    target.die()
    self.consume()

class AlienAbility2(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 5
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_is_alive = False # 対象が生きている必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Affair
    target.revive()
    self.consume()

  def available(self, target):
    if self.__super.available(target) and not target.alive:
      return True
    return False

# class GodlyBeingAbility(CharacterAbilityBase):
#   def __init__(self, *args):
#     self.__super.__init__(*args)

# class GodlyBeingAbility2(CharacterAbilityBase):
#   def __init__(self, *args):
#     self.__super.__init__(*args)

class PoliceOfficerAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 4
    self.target_types = [itypes.Affair]

  def __call__(self, target):
    # target: Affair
    target.reveal()
    self.consume()

  def available(self, target):
    if self.__super.available(target) and target.occured:
      return True
    return False


class PoliceOfficerAbility2(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 5
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    raise NotImplementedError


class OfficeWorkerAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 3
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Character
    target.reveal()

  def available(self, target):
    if self.__super.available(target) and target == self.character:
      return True
    return False

class InformerAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 5
    self.target_types = [itypes.RuleX]

  def __call__(self, target):
    raise NotImplementedError

  def available(self, target):
    raise NotImplementedError

class PopIdolAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 3
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    target.add_paranoia(-1)

class PopIdolAbility2(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 4
    self.same_location_with_target = True # 対象と同一エリアである必要があるか
    self.target_types = [itypes.Character]

  def __call__(self, target):
    target.add_goodwill(1)


class JournalistAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 2
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Character
    raise NotImplementedError
 
class JournalistAbility2(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 2
    self.is_in_the_same_location = True
    self.target_types = [itypes.Character, itypes.Location]

  def __call__(self, target):
    target.add_intrigue(1)


class BossAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 5
    self.target_types = [itypes.Character]

  def __call__(self, target):
    # target: Character
    target.reveal()
    self.consume()

  def available(self, target):
    if self.__super.available(target) and (self.character.is_in_the_same_location(target) or target.is_in(self.character.turf)):
      return True
    return False

class DoctorAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.goodwill = 2
    self.betrayal = True # 友好暴発
    self.same_location_with_target = True #対象と同一エリア限定
    self.target_types = [itypes.Character]

  def __call__(self, target):
    raise NotImplementedError

class DoctorAbility2(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.n_available = 1
    self.goodwill = 3
    self.target_types = [itypes.Character]

  def __call__(self, target):
    pass
    #target.
    #raise NotImplementedError

  def available(self, target):
    # characters.pyでimportしてるからここは直に書くしか無い…?
    if self.__super.available(target) and target.classname == 'Patient': 
      return True
    return False


class NurseAbility(CharacterAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.refusable = False
    self.goodwill = 2
    self.same_location_with_target = True #対象と同一エリア限定
    self.target_types = [itypes.Character]

  def __call__(self, target):
    target.add_paranoia(-1)

  def available(self, target):
    if self.__super.available(target) and target.paranoia >= target.paranoia_limit: 
      return True
    return False

# class HenchmanAbility(CharacterAbilityBase):
#   def __init__(self, *args):
#     self.__super.__init__(*args)
