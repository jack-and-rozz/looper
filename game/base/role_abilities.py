# coding:utf-8
from utils import common

class RoleAbilityBase(object):
  __metaclass__ = common.SuperSyntaxSugarMeta
  def __init__(self, board, character):
    self.board = board
    self.character = character
    self.consumed = False # 1回限りの能力を使ったかどうか
    self.same_place_with_target = False # 対象と同一エリアである必要があるか (多いのでまとめる)
    self.target_is_alive = True # 対象が生きている必要があるか（キャラクタ限定）
    self.target_types = []      # 対象のタイプ (Character, Place, ...)
    self.ability_type = None    # 強制 or 任意
    self.available_phase = None # 使用可能フェイズ

  def consume(self):
    self.consumed = True

  def available(self, target):
    # 自身が生きている必要があるかは拡張のルールによって変わるので、能力使用フェイズで別にチェック
    res = not self.consumed
    if not target.instance_type in self.target_types:
      return False
    if self.same_place_with_target:
      res = res and self.character.is_in_the_same_place(target)
    if self.target_is_alive and target.instance_type == itypes.Character:
      res = res and target.alive
    return res
