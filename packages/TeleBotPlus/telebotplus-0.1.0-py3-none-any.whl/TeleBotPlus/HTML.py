import html
import random
from .utils import id_bot2client
from typing import *
__all__ = [
    "bold",
    "code",
    "from_list",
    "hide",
    "italic",
    "link",
    "mono",
    "normal",
    "quote",
    "spoiler",
    "strike",
    "text_mention",
    "underline",
    "url",
    "user",
    "userlink",
]
EXAMPLE_SIMPLE = {
    "type": "simple",
    "text": [
        "Hello ",
        {
            "styles": {
                "bold": None,
                "user": "%(id)s"
            },
            "text": "%(name)s"
        }
    ]
}
EXAMPLE_RANDOM = {
    "type": "random",
    "texts": [
        EXAMPLE_SIMPLE,
        "Hi"
    ]
}


def normal(text: str, escape: bool = True):
  """Не изменяет текст"""
  if escape:
    text = html.escape(text)
  return text


def bold(text: str, escape: bool = True):
  """Жирный"""
  if escape:
    text = html.escape(text)
  return "<b>{}</b>".format(text)


def code(text: str, lang: str = "", escape: bool = True):
  """Блок кода"""
  if escape == True:
    escape = (True, True)
  elif escape == False:
    escape = (False, True)
  elif type(escape) == dict:
    escape = (escape["text"], escape["lang"])
  if escape[0]:
    text = html.escape(text)
  if escape[1]:
    lang = html.escape(lang)
  return '<pre><code class="{}">{}</code></pre>'.format(lang.lower(), text)


def italic(text: str, escape: bool = True):
  """Курсив"""
  if escape:
    text = html.escape(text)
  return "<i>{}</i>".format(text)


def link(text: str, url: str, escape: bool = True):
  """Ссылка в тексте"""
  if escape == True:
    escape = (True, True)
  elif escape == False:
    escape = (False, True)
  elif type(escape) == dict:
    escape = (escape["text"], escape["url"])
  if escape[0]:
    text = html.escape(text)
  if escape[1]:
    url = html.escape(url)
  return '<a href="{}">{}</a>'.format(url, text)


url = link


def mono(text: str, escape: bool = True):
  """Моноширинный текст"""
  if escape:
    text = html.escape(text)
  return "<code>{}</code>".format(text)


def quote(text: str, expandable: bool = False, escape: bool = True):
  """Цитата"""
  if escape:
    text = html.escape(text)
  if expandable:
    return "<blockquote expandable>{}</blockquote>".format(text)
  else:
    return "<blockquote>{}</blockquote>".format(text)


def spoiler(text: str, escape: bool = True):
  """Скрытый текст"""
  if escape:
    text = html.escape(text)
  return "<tg-spoiler>{}</tg-spoiler>".format(text)


hide = spoiler


def strike(text: str, escape: bool = True):
  """Зачёркнутый текст"""
  if escape:
    text = html.escape(text)
  return "<s>{}</s>".format(text)


def underline(text: str, escape: bool = True):
  """Подчёркнутый текст"""
  if escape:
    text = html.escape(text)
  return "<u>{}</u>".format(text)


def user(text: str, id: int, convert_id: bool = False, *args, **kw):
  """Упоминание в тексте по ID"""
  if convert_id:
    id = id_bot2client(id)
  return link(text, f"tg://user?id={id}", *args, **kw)


text_mention = user


def userlink(text: str, id: int, convert_id: bool = False, *args, **kw):
  """Ссылка на пользователя в тексте (без упоминания)"""
  if convert_id:
    id = id_bot2client(id)
  return link(text, f"tg://openmessage?user_id={id}", *args, **kw)


_functions = {}
for k, v in tuple(locals().items()):
  if k in __all__:
    _functions[k] = v


def _build_text(l: Union[str, list]) -> str:
  if type(l) == str:
    return normal(l)
  t = ""
  for i in l:
    if type(i) == str:
      t += normal(i)
      continue
    if type(i) == dict:
      s = normal(i["text"])
      if "styles" in i:
        for k, v in i["styles"].items():
          if v == None:
            s = _functions[k](s, escape=False)
          else:
            s = _functions[k](s, v, escape=False)
      t += s
  return t


def from_dict(d: dict[str, Any]) -> tuple[str, bool]:
  """text,allow_cache"""
  if type(d) == str:
    return normal(d), True
  if not "type" in d:
    d["type"] = "simple"
  d["type"] = d["type"].lower()
  if d["type"] == "simple":
    return _build_text(d["text"]), True
  if d["type"] == "random":
    return from_dict(random.choice(d["texts"]))[0], False
  raise ValueError("Unknown type: %s" % d["type"])
