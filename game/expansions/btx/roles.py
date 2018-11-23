# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base.roles import RoleBase
from game.expansions.btx.role_abilities import *

class Person(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)

class KeyPerson(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)

class Killer(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.ign_friend = True
    self.abilities = [
      KillerAbility(self.board, self.character),
      KillerAbility2(self.board, self.character),
    ]

class Brain(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.ign_friend = True
    self.abilities = [BrainAbility(self.board, self.character)]

class Cultist(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.ign_friend_abs = True
    self.abilities = [CultistAbility(self.board, self.character)]

class TimeTraveler(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.unkillable = True
    self.abilities = [TimeTravelerAbility(self.board, self.character)]

class Witch(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.ign_friend_abs = True

class Friend(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.limit = 2
    self.abilities = [
      FriendAbility(self.board, self.character),
      FriendAbility2(self.board, self.character),
    ]

class ConspiracyTheorist(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.limit = 1

class Lover(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)

class LovedOne(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)

class SerialKiller(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)

class Factor(RoleBase):
  def __init__(self, *args):
    super(self.__class__, self).__init__(*args)
    self.ign_friend = True


name_to_class = OrderedDict([
  ('パーソン', Person),
  ('キーパーソン', KeyPerson),
  ('キラー', Killer),
  ('クロマク', Brain),
  ('カルティスト', Cultist),
  ('タイムトラベラー', TimeTraveler),
  ('ウィッチ', Witch),
  ('フレンド', Friend),
  ('ミスリーダー', ConspiracyTheorist),
  ('ラバーズ', LovedOne),
  ('メインラバーズ', Lover),
  ('シリアルキラー', SerialKiller),
  ('ファクター', Factor),
])
class_to_name = common.invert_dict(name_to_class)
