# coding:utf-8
import importlib
from pandas import DataFrame

from utils import common
from game.base import places, characters, consts
from game.managers.instance_manager import InstanceManager
import game.expansions as expansions

#能力などによって得た確定情報をまとめるクラス
# キャラの役職
# キャラの友好能力が使えたか
# キャラに友好無視されたか
# ルールX
# 事件が起こったかどうか
# 事件の犯人

class Information(object):
  def __init__(self):
    pass

#プレイヤーに渡される現在のボードの状態
class State(object):
  def __init__(self, board, show_hidden, show_plots):
    self._state = common.dotDict()
    self._state.characters = []
    self._state.places = []
    self._state.actors_plots = []
    self._state.loop = board.loop
    self._state.day = board.day
    for c in board.characters:
      l = [c._id, c.position._id, c.alive, c.counters]
      self._state.characters.append(l) 
    for p in board.places:
      l = [p._id, p.counters]
      self._state.places.append(l)
    # Hidden
    if show_hidden:
      self._state.roles = []
      for c in board.characters:
        l = [c._id, c.role._id]
        self._state.roles.append(l) 
      self._state.rules = [r._id for r in board.rules]
    if board.writers_plots and board.actors_plots:
      pass
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
  def actors_plots(self):
    return self._state.actors_plots

  def writer_plots(self):
    return self._state.writers_plots

  def __str__(self):
    return str(self._state)

class Board(object):
  def __init__(self, scenerio, loop, actors, writer, prev_board=None):
    self.scenerio = scenerio
    self.loop = loop
    self.actors = actors
    self.writer = writer
    self.actors_plots = []
    self.writers_plots = []
    self.day = 1
    self.phase = None
    self.ex_gauge = 0
    self.expansion = importlib.import_module('game.expansions.' + scenerio.expansion)
    self.information = Information()
    places_list = [p() for _, p in places.name_to_class.items()]
    self.places = InstanceManager(places.name_to_class, places_list)

    characters_list = []
    roles_list = []
    for char_name, role_name in scenerio.characters.items():
      role = self.expansion.roles.name_to_class[role_name]()
      if char_name == characters.class_to_name[characters.GodlyBeing]:
        character = characters.name_to_class[char_name](scenerio.godly_being_day)
      else:
        character = characters.name_to_class[char_name]()
      character.set_role(role)
      character.set_position(self.places.get(character.init_position))
      roles_list.append(role)
      characters_list.append(character)
    self.characters = InstanceManager(characters.name_to_class, characters_list)
    self.roles = InstanceManager(self.expansion.roles.name_to_class, roles_list)

    affairs_list = []
    for day, (affair_name, char_name) in scenerio.affairs.items():
      affair = self.expansion.affairs.name_to_class[affair_name](
        day, self.characters.get(char_name))
      affairs_list.append(affair)

    self.affairs = InstanceManager(self.expansion.affairs.name_to_class, 
                                   affairs_list)
    self.rules = []
  def show_as_text(self):
    print ('-' * 40)
    print ("Loop: %d" % self.loop)
    print ("Day : %d" % self.day)
    for place in self.places:
      print place.classname + ' : ' + ', '.join(place.counters)
    header = ['<Character>', '<Role>', '<Position>', 'Counters']
    data = [[character.classname, character.role.classname, character.position.classname, character.counters] for character in self.characters]
    print DataFrame(data, columns=header)
  
  def get_state(self, show_hidden=False, show_plots=True):
    # show_hidden: 非公開情報を表示するか
    # show_plots: プロットしたアクション内容を表示するか

    state = State(self, show_hidden=show_hidden, show_plots=show_plots)
    return state

  @property
  def id_info(self):
    info = common.dotDict()
    info.counters = consts.counters
    info.character_properties = consts.character_properties
    info.characters = self.characters.id_info
    info.actor_actions = self.actors[0].actions.id_info
    info.writer_actions = self.writer.actions.id_info
    info.roles = self.roles.id_info
    info.affairs = self.affairs.id_info
    info.places = self.places.id_info
    return info

  def pre_loop(self, writer, actor):
    self.phase = consts.phases.PreLoop
    if self.characters.include(characters.HenchMan):
      position = self.writer.plot_henchmans_position(self)
      self.characters.get(characters.HenchMan).set_position(position)

  def plot_writer_actions(self):
    self.phase = consts.phases.WritersAction

    state = self.get_state(show_hidden=True)
    self.writers_plots = self.writer.plot_action(state)

  def plot_actor_actions(self, leader_id):
    self.phase = consts.phases.ActorsAction
    for actor in self.actors:
      state = self.get_state()
      action = actor.plot_action(state, show_plots=False)
    self.actors_plots.append(action)

  def process_actions(self):
    self.phase = consts.phases.ProcessAction
    self.writer.restore_actions()
    for actor in self.actors:
      actor.restore_actions()
  def use_writer_abilities(self):
    self.phase = consts.phases.WritersAbility

  def use_actor_abilities(self, leader_id):
    self.phase = consts.phases.ActorsAbility

  def process_affairs(self, leader_id):
    self.phase = consts.phases.ProcessAffair

  def end_day(self, writer):
    self.phase = consts.phases.EndDay
    self.actors_plots = []
    self.writers_plots = []
    self.day += 1

  def end_loop(self):
    self.phase = consts.phases.EndLoop
