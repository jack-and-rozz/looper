# coding:utf-8
from utils import common

class AffairBase(object):
  def __init__(self, day, offender):
    self.day = day
    self.offender = offender
    self.occured = False
  def __str__(self):
    return self.__class__.__name__

  pass
