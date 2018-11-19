# coding:utf-8
import importlib, json

from utils import common
from game.base import places, characters, consts, actions
from game.managers.instance_manager import *#InstanceManager, CharacterManager
import game.expansions as expansions

#能力などによって得た確定情報をまとめるクラス
# キャラの役職
# キャラの友好能力が使えたか
# キャラに友好無視されたか
# ルールX
# 事件が起こったかどうか
# 事件の犯人


#これはクラスじゃなく関数のほうがいい？get_state, restore_state

# class Summary(object):
#   def __init__(self, board):
#     self._summary = common.dotDict()
#     self._summary.characters = board.characters.info(show_hidden)
#     self._summary.places = board.places.info(show_hidden)
#     self._summary.affairs = board.affairs.info(show_hidden)
    

#   def __str__(self):
#     return json.dumps(self._summary, ensure_ascii=False)

#プレイヤーに渡される現在のボードの状態
class State(object):
  def __init__(self, board, show_hidden, as_ids):
    self._state = common.dotDict()

    self._state.loop = board.loop
    self._state.day = board.day
    self._state.phase = board.phase
    self._state.ex_gauge = board.ex_gauge

    self._state.characters = board.characters.state(show_hidden, as_ids)
    self._state.places = board.places.state(show_hidden, as_ids)
    self._state.affairs = board.affairs.state(show_hidden, as_ids)

    self._state.actors = [actor.state(show_hidden, as_ids) for actor in board.actors]
    self._state.writer = board.writer.state(show_hidden, as_ids)

    
    #self._state.rules = board.rules.state(show_hidden)

    # if show_plots[0]:
    #   self.plots.writer = [(dest, act._id) for dest, act in board.writers_plots]
    # else:
    #   self.plots.writer = [(dest, consts.Unknown) for dest, act in board.writers_plots]
    # self.plots.actors = []
    # for i, (dest, act) in enumerate(board.actors_plots):
    #   act_id = act._id if show_plots[1][i] else consts.Unknown
    #   self.plots.actors.append((dest, act._id))

    # self._state.actions = common.dotDict()
    # self.actions.writer = sorted(board.writer.available_actions)
    # self.actions.actors = [a.available_actions for a in board.actors]

  @property
  def loop(self):
    return self._state.loop

  def day(self):
    return self._state.day

  def phase(self):
    return self._state.phase

  @property
  def actions(self):
    return self._state.actions

  @property
  def characters(self):
    return self._state.characters

  @property
  def places(self):
    return self._state.places

  @property
  def roles(self):
    return self._state.roles

  @property
  def rules(self):
    return self._state.rules

  @property
  def plots(self):
    return self._state.plots

  def __str__(self):
    return json.dumps(self._state, ensure_ascii=False)

class Board(object):
  def __init__(self, scenerio, loop, actors, writer, prev_board=None):
    self.scenerio = scenerio
    self.loop = loop
    self.actors = actors
    self.writer = writer
    self.actors_plots = [] #[((0 or 1, dest_id), action_id), ...]
    self.writers_plots = [] #[((0 or 1, dest_id), action_id), ...]
    self.day = 1
    self.phase = consts.phases.PreLoop
    self.ex_gauge = 0
    self.expansion = importlib.import_module('game.expansions.' + scenerio.expansion)
    places_list = [p() for _, p in places.name_to_class.items()]
    self.places = InstanceManager(places.name_to_class, places_list)

    characters_list = []
    roles_list = []
    for char_name, role_name in scenerio.characters.items():
      # if char_name == characters.class_to_name[characters.GodlyBeing]:
      #   character = characters.name_to_class[char_name](scenerio.godly_being_day)
      # else:
      character = characters.name_to_class[char_name](self)
      role = self.expansion.roles.name_to_class[role_name](self, character)
      character.set_role(role)
      character.set_place(self.places.get(character.init_place))
      characters_list.append(character)
      roles_list.append(role)
    self.characters = InstanceManager(characters.name_to_class, characters_list)

    #roles_list = [r() for _, r in self.expansion.roles.name_to_class.items()]
    self.roles = InstanceManager(self.expansion.roles.name_to_class, roles_list)
    #print(self.roles)
    #exit(1)

    affairs_list = []
    for day, (affair_name, char_name) in scenerio.affairs.items():
      affair = self.expansion.affairs.name_to_class[affair_name](
        day, self.characters.get(char_name))
      affairs_list.append(affair)

    self.affairs = InstanceManager(self.expansion.affairs.name_to_class, 
                                   affairs_list)
    rules_list = []
    # for rule_name in [scenerio.rule_y, scenerio.rule_x1, scenerio.rule_x2]:
    #   rule = self.expansion.rules.name_to_class[rule_name]()
    # self.rules =  InstanceManager(self.expansion.rules.name_to_class, 
    #                               rules_list)
    self.check_logic_error()

  def check_logic_error(self):
    return
  
  def get_state(self, show_hidden=True, as_ids=True):
    '''
    変化するものを表示
    - show_hidden: 非公開情報を表示するか
    '''
    state = State(self, show_hidden=show_hidden, as_ids=as_ids)
    return state

  def get_summary(self):
    '''
    変化しないものを表示
    '''
    return Summary(self)

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
  #   info.places = self.places.id_info
  #   return info

  # def pre_loop(self, writer, actor):
  #   self.phase = consts.phases.PreLoop
  #   if self.characters.include(characters.HenchMan):
  #     place_id = self.writer.plot_henchmans_place(self.get_state())
  #     place = self.places.get(place_id)
  #     self.characters.get(characters.HenchMan).set_place(place)

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

  #   # for p in self.places:
  #   #   a = [x[1] for x in filter(lambda x:x[0] == (consts.Place, p._id), ploted_actions)]
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

