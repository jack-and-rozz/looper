# coding:utf-8
from utils import common
from collections import OrderedDict
from game.base.consts import instance_types as itypes

class RoleBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, board):
    self.board = board
    self.character = None
    self.instance_type = itypes.Role
    self.classname = self.__class__.__name__
    self.limit = 0
    self.unkillable = False # 不死
    self.ign_friend = False # 友好無視
    self.ign_friend_abs = False # 絶対友好無視
    self.abilities = []

  def state(self, show_hidden, as_ids):
    state = []
    state += [
      ('_id', self._id), 
      ('name', self.classname),
      ('limit', self.limit),
      ('unkillable', self.unkillable),
      ('ignore_friendship', self.ign_friend),
      ('ignore_friendship_abs', self.ign_friend_abs),
    ]

    return OrderedDict(state)
    
