# coding:utf-8
from utils import common

phases = ['PreLoop', 'WritersAction', 'ActorsAction', 'ProcessAction', 'WritersAbility', 'ActorsAbility', 'ProcessAffair', 'EndDay', 'EndLoop']
phases = common.to_ids(phases, start=1)

character_properties = ['Student', 'Adult', 'Boy', 'Girl', 'Male', 'Female']
character_properties = common.to_ids(character_properties, start=1)

counters = ['Paranoia', 'Goodwill', 'Intrigue']
counters = common.to_ids(counters, start=1)

Unknown = 0
Place = 1
Character = 2
#Role = 3
#Rule = 4


CharacterInfo = {
  '男子学生': {'paranoia_limit':2, 'prop':['学生', '少年'], 'position':'学校'},
  '女子学生': {'paranoia_limit':3, 'prop':['学生', '少女'], 'position':'学校'},
  'お嬢様': {'paranoia_limit':1, 'prop':['学生', '少女'], 'position':'学校'},
  '委員長': {'paranoia_limit':2, 'prop':['学生', '少女'], 'position':'学校'},
  'イレギュラー': {'paranoia_limit':3, 'prop':['学生', '少年'], 'position':'学校'},
  '巫女': {'paranoia_limit':2, 'prop':['学生', '少女'], 'position':'神社'},
  '異世界人': {'paranoia_limit':2, 'prop':['少女'], 'position':'神社'},
  '神格': {'paranoia_limit':3, 'prop':['男性', '女性'], 'position':'神社'},
  '刑事': {'paranoia_limit':3, 'prop':['大人', '男性'], 'position':'都市'},
  'サラリーマン': {'paranoia_limit':2, 'prop':['大人', '男性'], 'position':'都市'},
  '情報屋': {'paranoia_limit':3, 'prop':['大人', '女性'], 'position':'都市'},
  'アイドル': {'paranoia_limit':2, 'prop':['学生', '少女'], 'position':'都市'},
  'マスコミ': {'paranoia_limit':2, 'prop':['大人', '男性'], 'position':'都市'}, 
  '大物': {'paranoia_limit':4, 'prop':['大人', '男性'], 'position':'都市'},
  '医者': {'paranoia_limit':2, 'prop':['大人', '男性'], 'position':'病院'},
  '入院患者': {'paranoia_limit':2, 'prop':['少年'], 'position':'病院'},
  'ナース': {'paranoia_limit':3, 'prop':['大人', '女性'], 'position':'病院'},
  '手先': {'paranoia_limit':1, 'prop':['大人', '男性'], 'position': None},
}
