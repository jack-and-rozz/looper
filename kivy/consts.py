
from kivy.utils import get_color_from_hex
from utils.common import recDotDefaultDict
import images
menu = recDotDefaultDict()
menu.text.font_size = 40
#menu.text.color =(0,0,0,1)
menu.text.color = (1,1,1,1)
#menu.button.color = (1,1,1,0.3)#get_color_from_hex('#FFFFFF')
menu.button.color = (0,0,0,0.0)#get_color_from_hex('#FFFFFF')
menu.button.image = images.BUTTON + '/paint.jpg'
#menu.background.image = images.BACKGROUND + '/e286db2a2060738393e005798189da23_s.jpg'
menu.background.image = images.BACKGROUND + '/hondana.jpg'
menu.background.opacity = 0.8


#font = 'mplus-2c-regular.ttf'
font = 'maboroshi.otf'
