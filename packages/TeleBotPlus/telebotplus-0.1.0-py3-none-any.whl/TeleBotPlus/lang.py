import os
from . import HTML
from MainShortcuts2 import ms
from typing import *


class Lang:
  def __init__(self, path: str = "lang.json"):
    self.path = os.path.abspath(path)
    self.load()
    self.reload_categories()

  def reload_categories(self):
    def get_wrapper(cat: str):
      def wrapper(name: str, values: Union[Iterable, dict[str, Any]] = {}) -> str:
        return self.get(cat, name, values)
      return wrapper
    for category in self.data:
      if not (category.startswith("_") or hasattr(self, category)):
        setattr(self, category, get_wrapper(category))

  def load(self, **kw):
    if os.path.exists(self.path):
      kw["path"] = self.path
      if not "like_json5" in kw:
        kw["like_json5"] = False
      self.data: dict[str, dict[str, Any]] = ms.json.read(**kw)
    else:
      self.data: dict[str, dict[str, Any]] = {}
    self.cache = {}

  def save(self, **kw):
    self.data["_format"] = "TeleBotPlus.lang"
    kw["data"] = self.data
    kw["path"] = self.path
    ms.json.write(**kw)

  def build_cache(self):
    for category in self.data:
      if not category.startswith("_"):
        for name in self.data[category]:
          text, allow_cache = HTML.from_dict(self.data[category][name])
          if allow_cache:
            self.cache[category, name] = text

  def get(self, category: str, name: str, values: Union[str, list, tuple, dict[str, Any]] = {}) -> str:
    v = values
    if type(values) in [list, tuple]:
      v = []
      for i in values:
        if type(i) == str:
          v.append(HTML.normal(i))
        else:
          v.append(i)
    if type(values) == dict:
      v = {}
      for i, obj in values.items():
        if type(obj) == str:
          v[i] = HTML.normal(obj)
        else:
          v[i] = obj
    if type(values) == str:
      v = HTML.normal(values)
    if not (category, name) in self.cache:
      text, allow_cache = HTML.from_dict(self.data[category][name])
      if allow_cache:
        self.cache[category, name] = text
      return text % v
    return self.cache[category, name] % v
