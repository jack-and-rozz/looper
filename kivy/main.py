#-*- coding: utf-8 -*-

from kivy.core.audio import SoundLoader
# #sound = SoundLoader.load('sounds/bgm/kamikakushi_loop.mp3')
#xqsound = SoundLoader.load('/Users/rozz/workspace/working/rooper.bak/kivy/sounds/bgm/senses-circuit/loop_68.wav')

from kivy.config import Config
Config.set('graphics', 'width', '640')
Config.set('graphics', 'height', '480')
#WIDTH = 1334 * 0.5
#HEIGHT = 750* 0.5
#Config.set('graphics', 'width', int(WIDTH))
#Config.set('graphics', 'height', int(HEIGHT))


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
from scenerios.scenerios import load_all

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
    self.root.add_widget(ScenerioDetailWidget(root=self.root, 
                                              scenerio=self.scenerio))
  pass


# class MenuItem(ButtonBehavior, Label):
#   def __init__(self, **kwargs):
#     super(MenuItem, self).__init__(**kwargs)

# class Menu(BoxLayout):
#   def __init__(self, **kwargs):
#     super(Menu, self).__init__(**kwargs)
  
class ScenerioSelectWidget(Widget):
  def __init__(self, **kwargs):
    super(ScenerioSelectWidget, self).__init__(**kwargs)
    self.mode = kwargs['mode']
    self.scenerios = load_all()    
    #for scenerio in self.scenerios:
    if self.mode == 'edit':
      scenerio_widget = ScenerioSummaryWidget(root=self, scenerio=None)
      self.scenerio_list.page.add_widget(scenerio_widget)
      
    for i in range(8):
      scenerio = self.scenerios[0]
      scenerio_widget = ScenerioSummaryWidget(root=self, scenerio=scenerio)
      self.scenerio_list.page.add_widget(scenerio_widget)
      

    # print(self.ids.scenerio_pages.orientation)
    # print(dir(self.ids.scenerio_pages))
    # print(dir(self.ids.scenerio_pages.children[0]))
  def back(self):
    self.parent.to_mainmenu()


class GameBoardWidget(Widget):
    def __init__(self, **kwargs):
      super(GameBoard, self).__init__(**kwargs)
    def back(self):
      pass
      #self.parent.to_mainmenu()



class GameRoot(BoxLayout):
    def __init__(self, **kwargs):
      super(GameRoot, self).__init__(**kwargs)

    def to_title(self):
      self.clear_widgets()
      self.add_widget(TitleWidget())

    def to_mainmenu(self):
      self.clear_widgets()
      self.add_widget(MainMenuWidget())
      pass

    def to_scenerio_select(self, mode):
      self.clear_widgets()
      self.add_widget(ScenerioSelectWidget(mode=mode))


class TestApp(App):
  def __init__(self, **kwargs):
    super(TestApp, self).__init__(**kwargs)
    self.title = 'Tragedy Rooper'

if __name__ == '__main__':
  import sys
  reload(sys)
  sys.setdefaultencoding('utf-8')
  TestApp().run()


