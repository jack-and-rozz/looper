# coding:utf-8
from collections import OrderedDict
from utils import common
from game.base.role_abilities import RoleAbilityBase
from game.base.consts import ability_types as atypes 
from game.base.consts import instance_types as itypes
from game.base.consts import phases

class KillerAbility(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Optional
    self.target_types = [itypes.Character]
    self.available_phase = phases.EndDay
    self.same_place_with_target = True

  def __call__(self, target):
    target.die()

  def available(self, target):
    return self.__super.available(target) and target.role.classname == 'KeyPerson' and target.intrigue >= 2

class KillerAbility2(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Optional
    self.target_types = [itypes.Player]
    self.available_phase = phases.EndDay

  def __call__(self, target):
    #raise NotImplementedError
    self.board.kill_players()

  def available(self, target):
    return target == self.character and self.character.intrigue >= 4

class BrainAbility(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Optional
    self.target_types = [itypes.Character, itypes.Place]
    self.available_phase = phases.WritersAbility
    self.same_place_with_target = True

  def __call__(self, target):
    target.add_intrigue(1)

class TimeTravelerAbility(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Optional
    self.target_types = [itypes.Character]
    self.available_phase = phases.EndDay

  def __call__(self, target):
    raise NotImplementedError

  def available(self, target):
    return self.character == target and self.character.goodwill <= 2 and self.board.day == self.board.max_days

class CultistAbility(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Optional
    self.target_types = [itypes.Character, itypes.Location]
    self.available_phase = phases.ActionExecution
    self.same_place_with_target = True

  def __call__(self, target):
    raise NotImplementedError


class FriendAbility(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Mandatory
    self.target_types = [itypes.Character]
    self.available_phase = phases.EndLoop

  def __call__(self, target):
    self.board.defeat = True
    target.reveal()

  def available(self, target):
    return target == self.character and not target.alive

class FriendAbility2(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Mandatory
    self.target_types = [itypes.Character]
    self.available_phase = phases.StartLoop

  def __call__(self, target):
    target.add_goodwill(1)

  def available(self, target):
    return target == self.character and self.role_revealed


class ConspiracyTheoristAbility(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Optional
    self.target_types = [itypes.Character]
    self.available_phase = phases.WritersAbility
    self.same_place_with_target = True

  def __call__(self, target):
    target.add_paranoia(1)


# todo:ラバーズとメインラバーズが同時に死んだ時、強制は同時解決なので両方に置かれる問題どう処理しよう？
class LovedOneAbility(RoleAbilityBase):
  pass

class LoversAbility(RoleAbilityBase):
  pass

class LoversAbility2(RoleAbilityBase):
  pass


class SerialKillerAbility(RoleAbilityBase):
  def __init__(self, *args):
    self.__super.__init__(*args)
    self.ability_type = atypes.Mandatory
    self.target_types = [itypes.Character]
    self.available_phase = phases.EndDay
    self.same_place_with_target = True

  def __call__(self, target):
    target.die()

  def available(self, target):
    self.__super.available(target) and len(self.board.characters_on_the_location(self.character.location)) == 2

class FactorAbility(RoleAbilityBase):
  pass


