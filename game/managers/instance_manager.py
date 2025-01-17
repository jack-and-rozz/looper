#coding: utf-8
from collections import OrderedDict
from utils import common

#生成したインスタンスとIDとの関連付け．インスタンスはシングルトンを想定
class InstanceManager(object):
  def __init__(self, name_to_class, instances):
    self.names = name_to_class.keys()
    self.instances = instances
    self.class_to_id = OrderedDict(zip(name_to_class.values(), range(1, len(name_to_class)+1)))
    self.name_to_id = OrderedDict(zip(name_to_class.keys(), range(1, len(name_to_class)+1)))
    self.instance_to_id = OrderedDict({ins:self.class_to_id[ins.__class__] for ins in instances})
    self.id_to_name = common.invert_dict(self.name_to_id)
    self.id_to_instance = common.invert_dict(self.instance_to_id)
    self.id_to_class = common.invert_dict(self.class_to_id)
    self._itercounter = 0
    for instance in instances:
      instance._id = self.get_id(instance)
      instance.name = self.get_name(instance)

  def info(self):
    return [x.info for x in self.instances]

  def state(self, show_hidden, as_ids):
    state = []
    for x in self.instances:
      s = x.state(show_hidden, as_ids)
      if s:
        state.append(s)
    return state
  
  @property
  def ids(self):
    return [x._id for x in self.instances]

  @property
  def id_info(self):
    return common.dotDict(
      ((c.__name__, _id) for c, _id in self.class_to_id.items())
    )

  def __str__(self):
    return str(self.instances)

  def __iter__(self):
    return self

  def next(self):
    if self._itercounter == len(self.instances):
      self._itercounter = 0
      raise StopIteration()
    instance = self.instances[self._itercounter]
    self._itercounter += 1
    return instance

  def get_id(self, key):
    if key == None:
      return None
    if type(key) == str:
      return self.name_to_id[key] if key in self.name_to_id else None
    elif type(key) == int:
      return key
    elif isinstance(key, type):
      return self.class_to_id[key] if key in self.class_to_id else None
    else:
      return self.instance_to_id[key] if key in self.instance_to_id else None
  def get_name(self, key):
    return self.id_to_name[self.get_id(key)] if self.get_id(key) in self.id_to_name else None

  def get(self, key):
    return self.id_to_instance[self.get_id(key)] if self.get_id(key) in self.id_to_instance else None

  def get_class(self, key):
    return self.id_to_class[self.get_id(key)]

  def include(self, key):
    return True if self.get_id(key) in self.id_to_instance else False

  def __getitem__(self, key):
    return self.get(key)
