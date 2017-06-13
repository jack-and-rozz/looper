# coding:utf-8
from utils import common

class RoleBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self):
    self.limit = 0
    self.immortal = False # 不死
    self.ign_friend = False # 友好無視
    self.ign_friend_abs = False # 絶対友好無視
    self.classname = self.__class__.__name__
  pass
