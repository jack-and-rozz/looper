# -*- coding:utf-8 -*-
#from __future__ import print_function
import sys, os, time, re, math, collections
import numpy as np

from itertools import chain
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, WARNING, ERROR, CRITICAL


############################################
#        Inheritance
############################################

class SuperSyntaxSugarMeta(type):
  def __new__(cls, name, bases, dct):
    obj = type.__new__(cls, name, bases, dct)
    setattr(obj, '_%s__super' % name, super(obj))
    return obj


############################################
#        List
############################################

def select_instance(l, c_list):
  return [x for x in l if True in [isinstance(x, c) for c in c_list]]
def remove_instance(l, c_list):
  return [x for x in l if not True in [isinstance(x, c) for c in c_list]]
def include_instance(l, c):
  return True if True in [isinstance(x, c) for x in l] else False

############################################
#        Dictionary
############################################

class dotDict(dict):
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__

  '''
  __getattr__ must be overridden to enable it to apply copy.deepcopy, since the object to be copied has to raise AttributeError instead of KeyError when a key is not in itself. 
  https://stackoverflow.com/questions/33387801/deep-copy-failure-when-copying-custom-object
  '''
  def __getattr__(self, key):
    if key in self:
      return self[key]
    raise AttributeError

class recDotDict(dict):
  __getattr__ = dict.__getitem__
  __setattr__ = dict.__setitem__
  __delattr__ = dict.__delitem__
  def __init__(self, _dict={}):
    for k in _dict:
      if isinstance(_dict[k], dict):
        _dict[k] = recDotDict(_dict[k])
      if isinstance(_dict[k], list):
        for i,x in enumerate(_dict[k]):
          if isinstance(x, dict):
            _dict[k][i] = dotDict(x)
    super(recDotDict, self).__init__(_dict)

  def __getattr__(self, key):
    if key in self:
      return self[key]
    raise AttributeError

class rec_defaultdict(collections.defaultdict):
  def __init__(self):
    self.default_factory = type(self)

class recDotDefaultDict(collections.defaultdict):
  __getattr__ = collections.defaultdict.__getitem__
  __setattr__ = collections.defaultdict.__setitem__
  __delattr__ = collections.defaultdict.__delitem__
  def __init__(self, _=None):
    super(recDotDefaultDict, self).__init__(recDotDefaultDict)

def to_ids(l,  start=0, dict_func=dotDict):
  return dict_func(zip(l, [i for i in range(start,len(l)+start)]))

def unicode_to_str(d, mode='encode', dict_func=collections.OrderedDict):
  def _unicode_to_str(v):
    if mode == 'encode':
      return v.encode('utf-8') if type(v) == unicode else v
    elif mode == 'decode':
      return v.decode('utf-8') if type(v) == str else v
    else:
      raise ValueError()
  new_d = dict_func({})
  for key, value in d.items():
    key = _unicode_to_str(key)
    value = [_unicode_to_str(x) for x in value] if type(value) == list else _unicode_to_str(value) 

    if isinstance(value, dict):
      new_d[key] = dict_func(unicode_to_str(value))
    else:
      new_d[key] = value
  return dict_func(new_d)

def dict_print(d, indent=0):
  for key, value in d.items():
    space =' '
    if isinstance(value, dict):
      print (space * indent + str(key) + ': ')
      dict_print(value, indent+1)
    elif type(value) == list:
      print (space * indent + str(key) + ': ')
      print (space * (indent+1) + ', '.join(str(x) for x in value))
    else:
      print (space * indent + str(key) + ': ' + str(value))

# dictionaryのkey:value入れ替え
def invert_dict(dictionary):
  return {v:k for k, v in dictionary.items()}





# # 辞書のvalueでソート。デフォルトは降順
# def sort_dict(dic, sort_type="DESC"):
#     counter = collections.Counter(dic)
#     if sort_type == "ASC":
#         count_pairs = sorted(counter.items(), key=lambda x: x[1])
#     elif sort_type == "DESC":
#         count_pairs = sorted(counter.items(), key=lambda x: -x[1])
#     key, value = list(zip(*count_pairs))
#     return (key, value)

# # funcは key, valueのタプルを引数に取り、同じく key, valueのタプルを返す関数
# def map_dict(func, _dict):
#     return dict([func(k,v) for k,v in _dict.items()]) 


# def split_dict():
#     pass

# class rec_defaultdict(collections.defaultdict):
#     def __init__(self):
#         self.default_factory = type(self)

# def modulize(dictionary):
#     import imp
#     m = imp.new_module("")
#     m.__dict__.update(dictionary)
#     return m


# ############################################
# #        Batching
# ############################################

# def zero_one_vector(one_indices, n_elem):
#   l = [0.0 for _ in xrange(n_elem)]
#   for idx in one_indices:
#     l[idx] = 1.0
#   return l

# ############################################
# #        Random
# ############################################

# # arr = [arr0, arr1, ...]
# # size_arr : [len(arr0), len(arr1), ...]
# def random_select_by_scale(size_arr):
#   scale = [sum(size_arr[:i + 1]) / float(sum(size_arr)) for i in xrange(len(size_arr))]
#   random_number_01 = np.random.random_sample()
#   _id = min([i for i in xrange(len(scale))
#              if scale[i] > random_number_01])
#   return _id

# ############################################
# #        Text Formatting
# ############################################

# def format_zen_han(l):
#   import mojimoji
#   l = l.decode('utf-8') if type(l) == str else l
#   l = mojimoji.zen_to_han(l, kana=False) #全角数字・アルファベットを半角に
#   l = mojimoji.han_to_zen(l, digit=False, ascii=False) #半角カナを全角に
#   return l.encode('utf-8')


# ############################################
# #        Logging
# ############################################

# def logManager(logger_name='main', 
#               handler=StreamHandler(),
#               log_format = "[%(levelname)s] %(asctime)s - %(message)s",
#               level=DEBUG):
#     formatter = Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
#     logger = getLogger(logger_name)
#     handler.setFormatter(formatter)
#     handler.setLevel(level)
#     logger.setLevel(level)
#     logger.addHandler(handler)
#     return logger


# ############################################
# #        File reading
# ############################################

# def read_file(file_path, type_f=str, do_flatten=False, replace_patterns=None,
#               do_tokenize=True, delim=' ', max_rows=None):
#   lines = []
#   for i, line in enumerate(open(file_path, "r")):
#     if max_rows and i > max_rows:
#       break
#     line = line.replace("\n", "")
#     if replace_patterns:
#       for (before, after) in replace_patterns:
#         line = line.replace(before,  after)
#     lines.append(line)

#   if do_tokenize:
#     lines = [[type_f(t) for t in line.split(delim) if t != ''] for line in lines]

#   if do_flatten:
#     lines = flatten(lines)
#   return lines

# def read_file_with_header(file_path, type_f=str, do_flatten=False, delim=' ', do_tokenize=True):
#     data = read_file(file_path, type_f, do_flatten, delim, do_tokenize)
#     header = data[0]
#     data = data[1:]
#     return header, data

# def read_vector(file_path, type_f=float):
#     # あんまりサイズが大きくなるとエラー？
#     lines = read_file(file_path)
#     vector_dict = collections.OrderedDict({})
#     # 初めの一行目はベクトルの行数と次元なのでスキップ
#     for l in lines[1:]:
#         vector_dict[l[0]] = np.array([type_f(w) for w in l[1:]])
#     return vector_dict


# def read_file_with_id(file_path, delim=None):
#   _ids = []
#   _texts = []
#   with open(file_path, "r") as f:
#     # 同じツイートをひとまとめにされると面倒なのでlistで
#     for l in f:
#       line = l.replace("\n", "").split(delim)
#       _ids.append(line[0])
#       _texts.append(line[1:])
#     return _ids, _texts


# def read_stc_file(file_path, tokenize_text=True):
#     _ids = []
#     _texts = []
#     with open(file_path, "r") as f:
#         # 同じツイートをひとまとめにされると面倒なのでlistで
#         for l in f:
#             if tokenize_text:
#                 line = l.replace("\n", "").split()
#                 _ids.append(line[0])
#                 _texts.append(line[1:])
#             else:
#                 line = l.replace("\n", "").split('\t')
#                 _ids.append(line[0])
#                 _texts.append(line[1])
#     return _ids, _texts

# def read_id(file_path): 
#     with open(file_path, "r") as f:
#         lines = [line.replace("\n", "").split()[0] for line in f]
#     return lines


# def read_mconfig(model_path, config_file = "config"):
#     res = dotDict({})
#     with open(model_path + '/' + config_file) as f:
#         for l in f:
#             m = re.search("(.+)=(.+)", l)
#             if m :
#                 res[m.group(1)] = m.group(2)
#     return res

# ############################################
# #        String
# ############################################

# def concatenate_sequence(seq, id_to_word=None):
#     if id_to_word:
#         return ' '.join([id_to_word[word_id] for word_id in seq])
#     else:
#         return ' '.join([str(word) for word in seq])


# # 単語のid列を文に変更してprint
# def print_sequence(seq, id_to_word=None):
#     if id_to_word:
#       print (" ".join([id_to_word[word_id] for word_id in seq]))
#       print ('')
#     else:
#       print (" ".join([word for word in seq]))
#       print ('')

# # argparserの文字列をboolに変換
# def str_to_bool(str_):
#     bool_ = True
#     if str_ in ["T", "True", "true", "1", True]:
#         bool_ = True
#     elif str_ in ["F", "False", "false", "0", False]:
#         bool_ = False
#     else:
#         print("Irregular bool string")
#         exit(1)
#     return bool_


# def separate_path_and_filename(file_path):
#     pattern = '^(.+)/(.+)$'
#     m = re.match(pattern, file_path)
#     if m:
#       path, filename = m.group(1), m.group(2) 
#     else:
#       path, filename = None , file_path
#     return path, filename

# def count_uniq_tokens(sentence_array):
#     vocab = collections.defaultdict(int)
#     for s in sentence_array:
#         for token in s:
#             vocab[token] += 1
#     return vocab

# # 数値文字列の行列 ([['1', '3'], ['2', '4']]) を数値に 
# # read_file 時に指定すればいいのでは？
# #def strmat_to_type(mat, type_f):
# #    res = [[type_f(i) for i in l] for l in mat]
# #    return res

# ############################################
# #        List
# ############################################

# def regexp_indices(pattern, l):
#     """
#     リストの中で正規表現にマッチしたものをすべて返す
#     pattern: regexp
#     l      : list
#     """
#     res = []
#     for i, x in enumerate(l):
#         m = re.match(pattern, x)
#         if not m == None:
#             res.append(i)
#     return res

# def devide_by_labels(elements, labels, N):
#     """
#     elementsを付与されたラベルlabelsで分けた結果を返す
#     elements: list
#     labels  : list
#     N       : int
#     """
#     res = [[] for _ in xrange(0, N)]
#     for i, label in enumerate(labels):
#         res[label].append(elements[i])
#     return res

# def find_first(predicate, l):
#     """
#     条件を満たす最初の要素を返す
#     predicate: function returns bool
#     l: list
#     """
#     if len(l) == 0:
#         return 
#     if predicate(l[0]):
#         return l[0]
#     else:
#         find_first(predicate, l[1:])


# def flatten(l):
#     return list(chain.from_iterable(l))

# def max_elem( lis ):
#   L = lis[:]#copy
#   S = set(lis)
#   S = list(S)
#   MaxCount=0
#   ret='nothing...'

#   for elem in S:
#     c=0
#     while elem in L:
#       ind = L.index(elem)
#       foo = L.pop(ind)
#       c+=1
#     if c>MaxCount:
#       MaxCount=c
#       ret = elem
#   return ret

# ############################################
# #        Measuring
# ############################################

# def benchmark(func=None, prec=3, unit='auto', name_width=0, time_width=8):
#     """
#     A decorator that prints the time a function takes
#     to execute per call and cumulative total.

#     Accepts the following keyword arguments:

#     `unit`  str  time unit for display. one of `[auto, us, ms, s, m]`.
#     `prec`  int  radix point precision.
#     `name_width`  int  width of the right-aligned function name field.
#     `time_width`  int  width of the right-aligned time value field.

#     For convenience you can also set attributes on the benchmark
#     function itself with the same name as the keyword arguments
#     and the value of those will be used instead. This saves you
#     from having to call the decorator with the same arguments each
#     time you use it. Just set, for example, `benchmark.prec = 5`
#     before you use the decorator for the first time.
#     """
#     import time
#     if hasattr(benchmark, 'prec'):
#         prec = getattr(benchmark, 'prec')
#     if hasattr(benchmark, 'unit'):
#         unit = getattr(benchmark, 'unit')
#     if hasattr(benchmark, 'name_width'):
#         name_width = getattr(benchmark, 'name_width')
#     if hasattr(benchmark, 'time_width'):
#         time_width = getattr(benchmark, 'time_width')
#     if func is None:
#         return partial(benchmark, prec=prec, unit=unit,
#                        name_width=name_width, time_width=time_width)

#     @wraps(func)
#     def wrapper(*args, **kwargs):  # IGNORE:W0613
#         def _get_unit_mult(val, unit):
#             multipliers = {'us': 1000000.0, 'ms': 1000.0, 's': 1.0, 'm': (1.0 / 60.0)}
#             if unit in multipliers:
#                 mult = multipliers[unit]
#             else:  # auto
#                 if val >= 60.0:
#                     unit = "m"
#                 elif val >= 1.0:
#                     unit = "s"
#                 elif val <= 0.001:
#                     unit = "us"
#                 else:
#                     unit = "ms"
#                 mult = multipliers[unit]
#             return (unit, mult)
#         t = time.clock()
#         res = func(*args, **kwargs)
#         td = (time.clock() - t)
#         wrapper.total += td
#         wrapper.count += 1
#         tt = wrapper.total
#         cn = wrapper.count
#         tdu, tdm = _get_unit_mult(td, unit)
#         ttu, ttm = _get_unit_mult(tt, unit)
#         td *= tdm
#         tt *= ttm
#         print(" -> {0:>{8}}() @ {1:>03}: {3:>{7}.{2}f} {4:>2}, total: {5:>{7}.{2}f} {6:>2}"
#               .format(func.__name__, cn, prec, td, tdu, tt, ttu, time_width, name_width))
#         return res
#     wrapper.total = 0
#     wrapper.count = 0
#     return wrapper

# # 時間を測るデコレータ
# def timewatch(logger=None):
#     if logger is None:
#         logger = logManager(logger_name='utils')
#     def _timewatch(func):
#         def wrapper(*args, **kwargs):
#             start = time.time()
#             result = func(*args, **kwargs)
#             end = time.time()
#             logger.info("%s: %f sec" % (func.__name__ , end - start))
#             return result
#         return wrapper
#     return _timewatch


# ############################################
# #        MultiProcessing
# ############################################

# def argwrapper(args):
#     '''
#     args.append((func, arg1, arg2, ...))
#     p = multiprocessing.Pool(n_process)
#     res = p.map(argwrapper, args)

#     '''
#     return args[0](*args[1:])


# #############################################
# #        Others
# #############################################

# def decorate_instance_methods(func_list, decorator):
#   for func in func_list:
#     func = decorater(func)
