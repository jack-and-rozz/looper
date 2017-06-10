# coding:utf-8
from utils import common
from game.base.consts import PlaceIds, CharacterIds, CharacterInfo

class CharacterBase(object):
  def __init__(self, cname, role):
    self.counters = []
    info = CharacterInfo(cname)
    self._id = CharacterInfo(cname)
    self.paranoia_limit = info.paranoia_limit
    self.prop = info.prop
    self.role = role

# class BoyStudent(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class GirlStudent(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class RichMansDaughter(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class ClassRep(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class MysteryBoy(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class ShrineMaiden(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class Alien(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class GodlyBeing(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class ShrineMaiden(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class PoliceOfficer(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class OfficeWorker(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class Informer(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class PopIdol(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class Journalist(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class Boss(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class Doctor(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class Patient(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

# class Nurse(CharacterBase)
#   def __init__(self, info):
#      super().__init__(info)

