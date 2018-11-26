# coding:utf-8
from utils import common
from collections import OrderedDict
from game.base import consts
from game.base.consts import instance_types as itypes

class AffairBase(object):
  def __init__(self, day, culprit):
    self.instance_type = itypes.Affair
    self.day = day
    self.culprit = culprit
    self.culprit_revealed = False
    self.occurred = False
    self.classname = self.__class__.__name__

  def reset(self):
    self.occured = False

  def reveal(self):
    self.culprit_revealed = True

  def state(self, show_hidden, as_ids):
    state = []
    state += [
      ('_id', self._id), 
      ('day', self.day),
      ('classname', self.classname),
      ('occurred', self.occurred),
    ]
    if show_hidden and not self.culprit_revealed:
      state += [('culprit', self.culprit._id if as_ids else self.culprit.classname)]
    else:
      state += [('culprit', consts.Unknown._id if as_ids else consts.Unknown.classname )]
    return OrderedDict(state)


  pass
