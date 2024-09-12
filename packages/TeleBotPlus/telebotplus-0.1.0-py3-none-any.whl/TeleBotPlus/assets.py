import os
import telebot
from . import assets_converter
from .utils import download_file
from hashlib import sha512
from MainShortcuts2 import ms
from typing import Union


class Assets:
  __format__ = 1
  ID_LEN = len(sha512(b"example").hexdigest())

  def __init__(self, dir: str = "assets", auto_load: bool = True, *, bot: telebot.TeleBot):
    self.bots = {}
    self.add_bot(bot)
    self.main_bot = bot.token
    self.dir = os.path.abspath(dir).replace("\\", "/")
    ms.path.rm(self.dir + "/.download_tmp")
    if auto_load:
      if os.path.isfile(f"{self.dir}/index.json"):
        self.index = ms.json.read(f"{self.dir}/index.json")
      else:
        self.index = {"objects": {}}
        self.index["format"] = self.__format__

  def __getitem__(self, k):
    try:
      return self.index["objects"][k]
    except KeyError:
      self.index["objects"][k] = {}
    return self.index["objects"][k]

  def __hasitem__(self, k):
    return k in self.index["objects"]

  def __setitem__(self, k, v):
    self.index["objects"][k] = v

  def add_bot(self, bot: telebot.TeleBot, update: bool = False):
    if not bot.token in self.bots:
      self.bots[bot.token] = {}
    if (not "bot" in self.bots[bot.token]) or update:
      self.bots[bot.token]["bot"] = bot
    if (not "id" in self.bots[bot.token]) or update:
      self.bots[bot.token]["id"] = bot.get_me().id
    return bot.token

  def get_bot(self, bot: Union[dict, str, int, telebot.TeleBot] = None) -> dict:
    if bot == None:
      return self.get_bot(self.main_bot)
    if type(bot) == dict:
      if "bot" in bot:
        bot = bot["bot"]
    if type(bot) == telebot.TeleBot:
      self.add_bot(bot)
      bot = bot.token
    if type(bot) == str:
      return self.bots[bot]
    if type(bot) == dict:
      if "id" in bot:
        bot = bot["id"]
    if type(bot) == int:
      for i in self.bots.values():
        if i["id"] == bot:
          return i

  def copy2dir(self, path: str, file_id: str = None, file_type: str = None, url: str = None, *, bot: Union[str, int, telebot.TeleBot] = None, move: bool = False, replace: bool = True):
    hash = sha512()
    with open(path, "rb") as f:
      for i in f:
        hash.update(i)
    hash_hex = hash.hexdigest()
    file = self[hash_hex]
    if not "file_id" in file:
      file["file_id"] = {}
    if file_id:
      bot = self.get_bot(bot)
      if not str(bot["id"]) in file["file_id"]:
        file["file_id"][str(bot["id"])] = {}
      if file_type:
        try:
          file["file_id"][str(bot["id"])][file_type] = bot["bot"].get_file(file_id).file_id
        except Exception as error:
          print(f'WARN: Failed to check "file_id" for the file "{hash_hex}": {error}')
    if ms.path.exists(f"{self.dir}/objects/{hash_hex}") and replace:
      ms.path.rm(f"{self.dir}/objects/{hash_hex}")
    ms.dir.create(f"{self.dir}/objects")
    if move:
      ms.file.move(path, f"{self.dir}/objects/{hash_hex}")
    else:
      ms.file.copy(path, f"{self.dir}/objects/{hash_hex}")
    if not "url" in file:
      file["url"] = None
    if url:
      file["url"] = url
    file["created"] = os.path.getctime(f"{self.dir}/objects/{hash_hex}")
    file["edited"] = os.path.getmtime(f"{self.dir}/objects/{hash_hex}")
    file["extension"] = None
    file["id"] = hash_hex
    file["name"] = os.path.basename(path)
    file["sha512"] = hash_hex
    file["size"] = os.path.getsize(f"{self.dir}/objects/{hash_hex}")
    if "." in file["name"]:
      file["extension"] = file["name"].split(".")[-1].lower()
    return file

  def move2dir(self, path: str, file_id: str = None, file_type: str = None, url: str = None, *, bot: Union[str, int, telebot.TeleBot] = None, copy: bool = False, replace: bool = True):
    kw = {}
    kw["bot"] = bot
    kw["file_id"] = file_id
    kw["file_type"] = file_type
    kw["move"] = not copy
    kw["path"] = path
    kw["replace"] = replace
    kw["url"] = url
    return self.copy2dir(**kw)

  def url2dir(self, url: str, file_id: str, file_type: str = None, *, bot: Union[str, int, telebot.TeleBot] = None, replace: bool = True, save_url: bool = True, **kw):
    path = self.dir + "/.download_tmp/" + url.encode("utf-8").hex()
    kw["path"] = path
    kw["url"] = url
    ms.dir.create(self.dir + "/.download_tmp")
    download_file(**kw)
    kw = {}
    kw["bot"] = bot
    kw["file_id"] = file_id
    kw["file_type"] = file_type
    kw["path"] = path
    kw["replace"] = replace
    if save_url:
      kw["url"] = url
    return self.move2dir(**kw)

  def file_id2dir(self, file_id: str, file_type: str = None, *, bot: Union[str, int, telebot.TeleBot] = None, replace: bool = True):
    bot = self.get_bot(bot)
    path = self.dir + "/.download_tmp/" + (str(bot["id"]) + file_id).encode("utf-8").hex()
    ms.dir.create(self.dir + "/.download_tmp")
    download_file(bot["bot"].get_file_url(file_id), path)
    return self.move2dir(path, file_id, file_type, bot=bot, replace=replace)

  def save(self, **kw):
    kw["data"] = self.index
    kw["path"] = f"{self.dir}/index.json"
    return ms.json.write(**kw)

  def load(self, **kw):
    kw["path"] = f"{self.dir}/index.json"
    if not "like_json5" in kw:
      kw["like_json5"] = False
    self.index = ms.json.read(**kw)
    for k, v in self.index["objects"].items():
      v["id"] = k
    if self.index["format"] != self.__format__:
      if hasattr(assets_converter, "f{}to{}".format(self.index["format"], self.__format__)):
        self.index = getattr(assets_converter, "f{}to{}".format(self.index["format"], self.__format__))(index=self.index)
      else:
        raise ValueError("Assets index format is not supported")
    return self.index

  def get(self, id: Union[str, dict], file_type: str = None, bot: Union[str, int, telebot.TeleBot] = None) -> Union[None, dict]:
    if type(id) == dict:
      id = id.get("id")
    if self[id] != {}:
      file = self[id].copy()
      if file_type:
        if file_type == "url" and ("url" in file):
          file["file"] = file["url"]
        else:
          bot = self.get_bot(bot)
          if "file_id" in file:
            if str(bot["id"]) in file["file_id"]:
              if file_type in file["file_id"][str(bot["id"])]:
                file["file"] = file["file_id"][str(bot["id"])][file_type]
      if not "file" in file:
        if os.path.isfile("{}/objects/{}".format(self.dir, file["sha512"])):
          file["file"] = open("{}/objects/{}".format(self.dir, file["sha512"]), "rb")
      if "file" in file:
        return file

  def search(self, id: Union[str, dict] = None, name: str = None, only_first: bool = False, bot: Union[str, int, telebot.TeleBot] = None) -> Union[None, dict, list[dict]]:
    r = []
    if type(id) == dict:
      id = id.get("id")
    if id:
      file = self.get(id, bot=bot)
      if file:
        if only_first:
          return file
        r.append(file)
    if name:
      for k, v in self.index.items():
        if v["name"] == name:
          file = self.get(k, bot=bot)
          if file:
            if only_first:
              return file
            r.append(file)
    return r

  def set_file_id(self, id: Union[str, dict], file_id: Union[str, telebot.types.File], file_type: str, bot: Union[str, int, telebot.TeleBot] = None):
    bot = self.get_bot(bot)
    if type(id) == dict:
      id = id.get("id")
    if type(file_id) == telebot.types.File:
      file_id = file_id.file_id
    file = self.index["objects"][id]
    if not "file_id" in file:
      file["file_id"] = {}
    if not str(bot["id"]) in file["file_id"]:
      file["file_id"][str(bot["id"])] = {}
    file["file_id"][str(bot["id"])][file_type] = file_id
