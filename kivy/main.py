#-*- coding: utf-8 -*-
from pprint import pprint
from kivy.core.audio import SoundLoader
# #sound = SoundLoader.load('sounds/bgm/kamikakushi_loop.mp3')
#xqsound = SoundLoader.load('/Users/rozz/workspace/working/rooper.bak/kivy/sounds/bgm/senses-circuit/loop_68.wav')
from kivy.config import Config

Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')
WIDTH = 1334 * 0.65 
HEIGHT = 750* 0.8
Config.set('graphics', 'width', int(WIDTH))
Config.set('graphics', 'height', int(HEIGHT))


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.label import Label

from kivy.properties import StringProperty, ListProperty

from kivy.core.text import LabelBase, DEFAULT_FONT
from kivy.resources import resource_add_path
from kivy.core.audio import SoundLoader

from kivy.lang import Builder
from kivy.factory import Factory

import images, consts
from utils.common import recDotDict
from scenerios.scenerios import load_all
from game.managers.game_manager import GameManager

# デフォルトに使用するフォントを変更する
resource_add_path('./fonts')
LabelBase.register(DEFAULT_FONT, consts.font) #日本語が使用できるように日本語フォントを指定する


class TitleWidget(Widget):
  source = StringProperty(images.tragedy.logo)

  def __init__(self, **kwargs):
    super(TitleWidget, self).__init__(**kwargs)
    #path = './sounds/bgm/kamikakushi_loop.mp3'
    #if self.sound:
    #    self._stop()
    #self.sound = SoundLoader.load(path)
    #self.sound.play()
    pass

  def buttonClicked(self):
    pass
  
  def start_button_clicked(self):
    self.parent.to_mainmenu()
    #print(dir(self))
    pass
  
  def side_button_clicked(self):
    self.ids.characters_box.characters = images.get_random_character_path(2)
    pass


class MainMenuWidget(Widget):
  def __init__(self, **kwargs):
    super(MainMenuWidget, self).__init__(**kwargs)
    #print(self.ids['scenerio_pages'])

  def play_writer(self):
    self.parent.to_scenerio_select('play')

  def edit_scenerio(self):
    self.parent.to_scenerio_select('edit')

  def back(self):
    self.parent.to_title()

# TODO
class ScenerioDetailWidget(Widget):
  def __init__(self, **kwargs):
    self.root = kwargs['root']
    self.scenerio = kwargs['scenerio']
    super(ScenerioDetailWidget, self).__init__(**kwargs)
    print(self.size, self.x, self.y)
    
  def back(self):
    pass
    #self.root.

class ScenerioSummaryWidget(ButtonBehavior, Label):
  def __init__(self, **kwargs):
    super(ScenerioSummaryWidget, self).__init__(**kwargs)
    self.root = kwargs['root']
    self.scenerio = kwargs['scenerio']
    self.text = self.scenerio.title if self.scenerio else '[新規作成]'

  def to_detail(self):
    self.parent.add_widget(ScenerioDetailWidget(
      root=self.root, 
      scenerio=self.scenerio))

  def to_gameboard(self):
    self.root.to_gameboard(self.scenerio)
  pass

class ScenerioSelectWidget(Widget):
  def __init__(self, **kwargs):
    super(ScenerioSelectWidget, self).__init__(**kwargs)
    self.mode = kwargs['mode']
    self.root = kwargs['root']
    self.scenerios = load_all()    
    #for scenerio in self.scenerios:
    if self.mode == 'edit':
      scenerio_widget = ScenerioSummaryWidget(root=self.parent, scenerio=None)
      self.scenerio_list.page.add_widget(scenerio_widget)
      
    for i in range(8):
      scenerio = self.scenerios[0]
      scenerio_widget = ScenerioSummaryWidget(
        root=self.root, 
        scenerio=scenerio)
      self.scenerio_list.page.add_widget(scenerio_widget)
      

    # print(self.ids.scenerio_pages.orientation)
    # print(dir(self.ids.scenerio_pages))
    # print(dir(self.ids.scenerio_pages.children[0]))
  def back(self):
    self.parent.to_mainmenu()



class BoardCharacter(Button):
  def __init__(self, **kwargs):
    self.character = kwargs['character']
    self.images = images.tragedy.characters[self.character.classname]
    print(self.images)
    super(BoardCharacter, self).__init__(**kwargs)

class GameBoardWidget(BoxLayout):
    def __init__(self, **kwargs):
      super(GameBoardWidget, self).__init__(**kwargs)
      self.scenerio = kwargs['scenerio'] 
      self.game = GameManager(self.scenerio)
      self.game.init_board()
      self.state = self.game.board.get_state()
      self.display_state(self.state)

    def display_state(self, state):
      for chara_state in state.characters:
        chara = BoardCharacter(character=chara_state)
        self.locations.ids[chara_state.location].add_widget(chara)
        print(chara.character)
        #break

      # for c in self.locations.children[0].children:
      #   print('----')
      #   print(c, c.pos, c.size)
      #   for cc in  c.children:
      #     print(cc, cc.pos, cc.size)
      #     for ccc in  cc.children:
      #       print(ccc, ccc.pos, ccc.size)

    def back(self):
      print('back')
      pass
      #self.parent.to_mainmenu()
    def hospital_clicked(self):
      pass
    def shrine_clicked(self):
      pass
    def city_clicked(self):
      pass
    def school_clicked(self):
      pass



class GameRoot(BoxLayout):
    def __init__(self, **kwargs):
      super(GameRoot, self).__init__(**kwargs)
      #self.to_gameboard()
      
    def to_title(self):
      self.clear_widgets()
      self.add_widget(TitleWidget())

    def to_mainmenu(self):
      self.clear_widgets()
      self.add_widget(MainMenuWidget())
      pass

    def to_gameboard(self, scenerio=None):
      if not scenerio:
        scenerio = load_all()[0]
      self.clear_widgets()
      self.add_widget(GameBoardWidget(scenerio=scenerio))


    def to_scenerio_select(self, mode):
      self.clear_widgets()
      self.add_widget(ScenerioSelectWidget(
        root=self,
        mode=mode))


class RooperApp(App):
  def __init__(self, **kwargs):
    super(RooperApp, self).__init__(**kwargs)
    self.title = 'Tragedy Rooper'

if __name__ == '__main__':
  import sys
  reload(sys)
  sys.setdefaultencoding('utf-8')
  RooperApp().run()


