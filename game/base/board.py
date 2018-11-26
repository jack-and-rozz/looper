# coding:utf-8
import importlib, json

from utils.common import recDotDict
from game.base import locations, characters, consts, actions

from game.managers.instance_manager import *#InstanceManager, CharacterManager
import game.expansions as expansions

#能力などによって得た確定情報をまとめるクラス
# キャラの役職
# キャラの友好能力が使えたか
# キャラに友好無視されたか
# ルールX
# 事件が起こったかどうか
# 事件の犯人


#プレイヤーに渡される現在のボードの状態
# class State(object):
#   def __init__(self, board, show_hidden, as_ids):
#     self._state = common.dotDict()

#     self._state.loop = board.loop
#     self._state.day = board.day
#     self._state.phase = board.phase
#     self._state.ex_gauge = board.ex_gauge

#     self._state.rules = board.rules.state(show_hidden, as_ids)
#     self._state.characters = board.characters.state(show_hidden, as_ids)
#     self._state.locations = board.locations.state(show_hidden, as_ids)
#     self._state.affairs = board.affairs.state(show_hidden, as_ids)

#     self._state.actors = [actor.state(show_hidden, as_ids) for actor in board.actors]
#     self._state.writer = board.writer.state(show_hidden, as_ids)

#   @property
#   def loop(self):
#     return self._state.loop

#   def day(self):
#     return self._state.day

#   def phase(self):
#     return self._state.phase

#   @property
#   def actions(self):
#     return self._state.actions

#   @property
#   def characters(self):
#     return self._state.characters

#   @property
#   def locations(self):
#     return self._state.locations

#   @property
#   def roles(self):
#     return self._state.roles

#   @property
#   def rules(self):
#     return self._state.rules

#   @property
#   def plots(self):
#     return self._state.plots

#   def __str__(self):
#     return json.dumps(self._state, ensure_ascii=False)


class Board(object):
  def __init__(self, scenerio, loop, actors, writer, interface):
    self.scenerio = scenerio
    self.max_loops = scenerio.loop
    self.loop = loop
    self.max_days = scenerio.days
    self.day = 1
    self.actors = actors
    self.writer = writer
    self.interface = interface

    # self.actors_plots = [] #[((0 or 1, dest_id), action_id), ...]
    # self.writers_plots = [] #[((0 or 1, dest_id), action_id), ...]
    self.phase = consts.phases.PreLoop
    self.ex_gauge = 0
    self.defeat = False
    self.expansion = importlib.import_module('game.expansions.' + scenerio.expansion)
    locations_list = [p() for _, p in locations.name_to_class.items()]
    self.locations = InstanceManager(locations.name_to_class, locations_list)

    characters_list = []
    roles_list = []
    for char_name, role_name in scenerio.characters.items():
      # if char_name == characters.class_to_name[characters.GodlyBeing]:
      #   character = characters.name_to_class[char_name](scenerio.godly_being_day)
      # else:
      role = self.expansion.roles.name_to_class[role_name](self)
      character = characters.name_to_class[char_name](self, role)
      #character.location = self.locations[character.init_location]
      role.character = character
      character.reset()
      characters_list.append(character)
      roles_list.append(role)

    self.characters = InstanceManager(characters.name_to_class, characters_list)
    self.roles = InstanceManager(self.expansion.roles.name_to_class, roles_list)

    affairs_list = []
    for day, (affair_name, char_name) in scenerio.affairs.items():
      affair = self.expansion.affairs.name_to_class[affair_name](
        day, self.characters.get(char_name))
      affairs_list.append(affair)

    self.affairs = InstanceManager(self.expansion.affairs.name_to_class, 
                                   affairs_list)
    rules_list = []
    for rule_name in [scenerio.rule_y, scenerio.rule_x1, scenerio.rule_x2]:
      rule = self.expansion.rules.name_to_class[rule_name](self)
      rules_list.append(rule)
    self.rules =  InstanceManager(self.expansion.rules.name_to_class, 
                                  rules_list)
    self.check_logic_error()

  def characters_on_the_location(self, location):
    return [c for c in self.characters if c.location == location]

  def check_logic_error(self):
    return

  def get_state(self, show_hidden=True, as_ids=False):
    '''
    変化するものを表示
    - show_hidden: 非公開情報を表示するか
    '''
    board = self
    state = recDotDict()
    state.loop = board.loop
    state.day = board.day
    state.phase = board.phase
    state.ex_gauge = board.ex_gauge
    
    state.rules = board.rules.state(show_hidden, as_ids)
    state.characters = board.characters.state(show_hidden, as_ids)
    state.locations = board.locations.state(show_hidden, as_ids)
    state.affairs = board.affairs.state(show_hidden, as_ids)
    
    state.actors = [actor.state(show_hidden, as_ids) for actor in board.actors]
    state.writer = board.writer.state(show_hidden, as_ids)
    return recDotDict(state)

  def get_summary(self):
    '''
    変化しないものを表示
    '''
    return Summary(self)

  ###############################################3

  def kill_players(self):
    raise NotImplementedError

  
  # @property
  # def id_info(self):
  #   info = common.dotDict()
  #   info.counters = consts.counters
  #   info.character_properties = consts.character_properties
  #   info.characters = self.characters.id_info
  #   info.actor_actions = self.actors[0].actions.id_info
  #   info.writer_actions = self.writer.actions.id_info
  #   info.roles = self.roles.id_info
  #   info.affairs = self.affairs.id_info
  #   info.locations = self.locations.id_info
  #   return info

  # def pre_loop(self, writer, actor):
  #   self.phase = consts.phases.PreLoop
  #   if self.characters.include(characters.HenchMan):
  #     location_id = self.writer.plot_henchmans_location(self.get_state())
  #     location = self.locations.get(location_id)
  #     self.characters.get(characters.HenchMan).set_location(location)

  # def plot_writer_actions(self):
  #   self.phase = consts.phases.WritersPlot

  #   state = self.get_state(show_hidden=True)
  #   self.writers_plots = self.writer.plot_action(state)

  # def plot_actor_actions(self, leader_id):
  #   self.phase = consts.phases.ActorsPlot
  #   for i, actor in enumerate(self.actors):
  #     # プロットしたカードが何かは隠す
  #     show_plots = (False, [False, False, False])
  #     show_plots[1][i] = True
  #     state = self.get_state(show_plots=show_plots)
  #     action = actor.plot_action(state)
  #     self.actors_plots.append(action)

  # def process_actions(self):
  #   self.phase = consts.phases.ProcessAction

  #   ploted_actions = self.actors_plots + self.writers_plots

  #   # 暗躍禁止2つ以上あったら両方無効
  #   duplicated_forbid_intrigue = len([a for a in self.actors_plots if isinstance(a[1], actions.ForbidIntrigue)])
    
  #   if duplicated_forbid_intrigue:
  #     ploted_actions = [a for a in ploted_actions if not isinstance(a, actions.ForbidIntrigue)]

  #   # for p in self.locations:
  #   #   a = [x[1] for x in filter(lambda x:x[0] == (consts.Location, p._id), ploted_actions)]
  #   #   for x in a:
  #   #     x.consume()
  #   #   p.apply_actions(a)

  #   # for c in self.characters:
  #   #   a = [x[1] for x in filter(lambda x:x[0] == (consts.Character, c._id), ploted_actions)]
  #   #   for x in a:
  #   #     x.consume()
  #   #   c.apply_actions(a)

  # def use_writer_abilities(self):
  #   self.phase = consts.phases.WritersAbility

  # def use_actor_abilities(self, leader_id):
  #   self.phase = consts.phases.ActorsAbility

  #   state = self.get_state()
  #   plot = self.actors[leader_id].plot_ability(state, None)
  #   while plot:
  #     state = self.get_state()
  #     plot = self.actors[leader_id].plot_ability(state, None)

  # def process_affairs(self, leader_id):
  #   self.phase = consts.phases.ProcessAffair
  #   exit(1)


  # def end_day(self, writer):
  #   self.phase = consts.phases.EndDay
  #   self.actors_plots = []
  #   self.writers_plots = []
  #   self.day += 1

  # def end_loop(self):
  #   self.phase = consts.phases.EndLoop

