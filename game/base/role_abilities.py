# coding:utf-8
from utils import common

class RoleAbilityBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, character):
    self.character = character
    self.consumed = False # 1回限りの能力を使ったかどうか
    self.same_place_with_target = False # 対象と同一エリアである必要があるか (多いのでまとめる)
    self.target_is_alive = True # 対象が生きている必要があるか（キャラクタ限定）
    self.target_types = [] # 対象のタイプ (Character, Place, ...)

  def consume(self):
    self.consumed = True

  def available(self, target):
    res = not self.consumed
    if self.same_place_with_target:
      res = res and self.character.is_in_the_same_place(target)
    if self.target_is_alive and target.instance_type == itypes.Character:
      res = res and target.alive
    return res
