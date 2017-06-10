# coding:utf-8
from utils import common

CharacterPropertyList = ['学生', '大人', '少年', '少女', '男性', '女性']
CharacterPropertyIds = common.to_ids(CharacterPropertyList)

CharacterInfo = {
  '男子学生': {'paranoia_limit':2, 'prop':['学生', '少年'], 'position':'学校'},
  '女子学生': {'paranoia_limit':3, 'prop':['学生', '少女'], 'position':'学校'},
  'お嬢様': {'paranoia_limit':1, 'prop':['学生', '少女'], 'position':'学校'},
  '委員長': {'paranoia_limit':2, 'prop':['学生', '少女'], 'position':'学校'},
  'イレギュラー': {'paranoia_limit':3, 'prop':['学生', '少年'], 'position':'学校'},
  '巫女': {'paranoia_limit':2, 'prop':['学生', '少女'], 'position':'神社'},
  '異世界人': {'paranoia_limit':2, 'prop':['少女'], 'position':'神社'},
  '神格': {'paranoia_limit':3, 'prop':['男性', '女性'], 'position':'神社'},
  '刑事': {'paranoia_limit':3, 'prop':['大人', '男性'], 'position':'都市'},
  'サラリーマン': {'paranoia_limit':2, 'prop':['大人', '男性'], 'position':'都市'},
  '情報屋': {'paranoia_limit':3, 'prop':['大人', '女性'], 'position':'都市'},
  'アイドル': {'paranoia_limit':2, 'prop':['学生', '少女'], 'position':'都市'},
  'マスコミ': {'paranoia_limit':2, 'prop':['大人', '男性'], 'position':'都市'}, 
  '大物': {'paranoia_limit':4, 'prop':['大人', '男性'], 'position':'都市'},
  '医者': {'paranoia_limit':2, 'prop':['大人', '男性'], 'position':'病院'},
  '入院患者': {'paranoia_limit':2, 'prop':['少年'], 'position':'病院'},
  'ナース': {'paranoia_limit':3, 'prop':['大人', '女性'], 'position':'病院'},
  '手先': {'paranoia_limit':1, 'prop':['大人', '男性'], 'position': None},
}
CharacterIds = common.to_ids(CharacterInfo).keys()

class CharacterBase(object):
  def __init__(self, info):
    self.counters = []
    self.paranoia_limit = info.paranoia_limit
    self.prop = info.prop

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

