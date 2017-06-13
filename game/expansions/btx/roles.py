# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base.roles import RoleBase

class Person(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()

class KeyPerson(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()

class Killer(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.ign_friend = True

class Brain(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.ign_friend = True

class Cultist(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.ign_friend_abs = True

class TimeTraveler(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.immportal = True

class Witch(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.ign_friend_abs = True


class Friend(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.limit = 2

class Misleader(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.limit = 1

class Lovers(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()

class MainLovers(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()

class SerialKiller(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()

class Factor(RoleBase):
  def __init__(self):
    super(self.__class__, self).__init__()
    self.ign_friend = True


name_to_class = OrderedDict({
  'パーソン': Person,
  'キーパーソン': KeyPerson,
  'キラー': Killer,
  'クロマク': Brain,
  'カルティスト': Cultist,
  'タイムトラベラー': TimeTraveler,
  'ウィッチ': Witch,
  'フレンド': Friend,
  'ミスリーダー': Misleader,
  'ラバーズ': Lovers,
  'メインラバーズ': MainLovers,
  'シリアルキラー': SerialKiller,
  'ファクター': Factor,
})
class_to_name = common.invert_dict(name_to_class)
