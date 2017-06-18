# coding:utf-8
import importlib
from pandas import DataFrame

from utils import common
from game.base import places, characters, consts, actions
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
    self._state.characters = common.dotDict()
    self._state.places = common.dotDict()
    self._state.actors_plots = []
    self._state.loop = board.loop
    self._state.day = board.day
    self._state.ex_gauge = board.ex_gauge
    self.characters.ids = [c._id for c in board.characters]
    self.characters.positions = [c.position._id for c in board.characters]
    self.characters.alive = [c.alive for c in board.characters]
    self.characters.paranoia = [c.paranoia for c in board.characters]
    self.characters.goodwill = [c.goodwill for c in board.characters]
    self.characters.intrigue = [c.intrigue for c in board.characters]
    self.places.ids = [p._id for p in board.places]
    self.places.intrigue = [p.intrigue for p in board.places]
    # Hidden
    if show_hidden:
      self._state.roles = [c.role._id for c in board.characters]
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
    self.actors_plots = [] #[((0 or 1, dest_id), action_id), ...]
    self.writers_plots = [] #[((0 or 1, dest_id), action_id), ...]
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

    header = ['<Place>', '<Intrigue>', '<Paranoia>', '<Goodwill>']
    data = [[p.classname, p.intrigue, p.paranoia, p.goodwill] for p in self.places]
    df = DataFrame(data, columns=header, index=[p._id for p in self.places])
    print df
    print ''

    header = ['<Character>', '<Role>', '<Position>', '<Intrigue>']
    data = [[character.classname, character.role.classname, character.position.classname, character.intrigue] for character in self.characters]
    df = DataFrame(data, columns=header, index=[c._id for c in self.characters])
    print df
  
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
      position_id = self.writer.plot_henchmans_position(self.get_state())
      position = self.places.get(position_id)
      self.characters.get(characters.HenchMan).set_position(position)

  def plot_writer_actions(self):
    self.phase = consts.phases.WritersAction

    state = self.get_state(show_hidden=True)
    self.writers_plots = self.writer.plot_action(state)

  def plot_actor_actions(self, leader_id):
    self.phase = consts.phases.ActorsAction
    for actor in self.actors:
      state = self.get_state(show_plots=False)
      action = actor.plot_action(state)
      self.actors_plots.append(action)

  def process_actions(self):
    self.phase = consts.phases.ProcessAction
    #self.writer.restore_actions()
    #for actor in self.actors:
    #  actor.restore_actions()

    actions_on_board = self.actors_plots + self.writers_plots

    # 暗躍禁止2つ以上あったら両方無効
    if len([a for a in self.actors_plots if isinstance(a[1], actions.ForbidIntrigue)]) > 1:
      actions_on_board = [a for a in actions_on_board if not isinstance(a, actions.ForbidIntrigue)]

    for p in self.places:
      a = [x[1] for x in filter(lambda x:x[0] == (consts.to_place, p._id), actions_on_board)]
      for x in a:
        x.consume()
      p.apply_actions(a)

    for c in self.characters:
      a = [x[1] for x in filter(lambda x:x[0] == (consts.to_character, c._id), actions_on_board)]
      for x in a:
        x.consume()
      c.apply_actions(a, self.places)

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
