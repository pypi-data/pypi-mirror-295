import inspect
import telebot
from .assets import Assets
from datetime import timedelta
from functools import wraps
from MainShortcuts2 import ms
from telebot import types
from typing import *
args_names: dict[str, tuple] = {}
for attr_name in dir(telebot.TeleBot):
  attr = getattr(telebot.TeleBot, attr_name)
  if callable(attr):
    try:
      attr_sign = inspect.signature(attr)
      args_names[attr_name] = []
      for i in attr_sign.parameters.keys():
        if i != "self":
          args_names[attr_name].append(i)
    except Exception:
      pass
del attr
del attr_name
del attr_sign
SHORT_NAMES = {
    "send_document": ["send_doc", "send_file"],
    "send_message": ["send_msg", "send_text"],
}


class Action:
  def __init__(self, func, args: Iterable = (), kwargs: dict[str, Any] = {}, is_async: bool = False, *, after: Iterable = [], before: Iterable = [], onetime: bool = False):
    self.after = after
    self.args = args
    self.before = before
    self.func = func
    self.kwargs = kwargs
    self.onetime = onetime
    if is_async:
      self.__call__ = self.async_run
    else:
      self.__call__ = self.run

  async def async_run(self):
    if self.onetime:
      if hasattr(self, "result"):
        raise RuntimeError("It can be performed only once")
    for i in self.before:
      i(self)
    self.result = await self.func(*self.args, **self.kwargs)
    for i in self.after:
      i(self)
    return self.result

  def run(self):
    if self.onetime:
      if hasattr(self, "result"):
        raise RuntimeError("It can be performed only once")
    for i in self.before:
      i(self)
    self.result = self.func(*self.args, **self.kwargs)
    for i in self.after:
      i(self)
    return self.result

  def set_args(self, *args, **kwargs):
    self.args = args
    self.kwargs = kwargs


class Reply2Message:
  def __init__(self, bot, msg: types.Message):
    self.bot: TeleBotPlus = bot
    self.msg = msg
    for k, v in SHORT_NAMES.items():
      if hasattr(self, k):
        for i in v:
          setattr(self, i, getattr(self, k))  # Сокращение названий функций

  def __getattr__(self, k):
    if k in self.__dict__:
      return self.__dict__[k]
    return getattr(self.bot, k)

  def __hasattr__(self, k: str):
    if k in self.__dict__:
      return True
    else:
      return hasattr(self.bot, k)

  def __dir__(self, *, original: bool = True, patched: bool = True):
    result = []
    if original:
      for i in dir(self.bot):
        if not i in result:
          result.append(i)
    if patched:
      for i in self.__dict__.keys():
        if not i in result:
          result.append(i)
    return result

  def _send(self, name: str, args: dict[str, Any] = {}, **kw) -> types.Message:
    if "kw" in args:
      args.update(args.pop("kw"))
    for i in args_names[name]:
      if i in args:
        kw[i] = args[i]
    if kw.get("allow_sending_without_reply") == None:
      kw["allow_sending_without_reply"] = True
    for i in ["chat_id", "message_thread_id", "reply_parameters"]:
      if i in kw:
        kw.pop(i)
    kw["chat_id"] = self.msg
    kw["reply_to_message_id"] = self.msg
    return getattr(self.bot, name)(**kw)

  def send_message(self, text, parse_mode=None, entities=None, disable_web_page_preview=None, disable_notification=None, protect_content=None, allow_sending_without_reply=None, reply_markup=None, timeout=None, link_preview_options=None, business_connection_id=None, message_effect_id=None, **kw) -> types.Message:
    return self._send("send_message", locals())

  def send_dice(self, emoji, disable_notification=None, reply_markup=None, timeout=None, allow_sending_without_reply=None, protect_content=None, business_connection_id=None, message_effect_id=None, **kw) -> types.Message:
    return self._send("send_dice", locals())

  def send_photo(self, photo, caption=None, parse_mode=None, caption_entities=None, disable_notification=None, protect_content=None, allow_sending_without_reply=None, reply_markup=None, timeout=None, has_spoiler=None, business_connection_id=None, message_effect_id=None, show_caption_above_media=None, **kw) -> types.Message:
    return self._send("send_photo", locals())

  def send_audio(self, audio, caption=None, duration=None, performer=None, title=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, thumbnail=None, caption_entities=None, allow_sending_without_reply=None, protect_content=None, thumb=None, business_connection_id=None, message_effect_id=None, **kw) -> types.Message:
    return self._send("send_audio", locals())

  def send_voice(self, voice, caption, duration=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, caption_entities=None, allow_sending_without_reply=None, protect_content=None, business_connection_id=None, message_effect_id=None, **kw) -> types.Message:
    return self._send("send_voice", locals())

  def send_document(self, document, caption=None, reply_markup=None, parse_mode=None, disable_notification=None, timeout=None, thumbnail=None, caption_entities=None, allow_sending_without_reply=None, visible_file_name=None, disable_content_type_detection=None, data=None, protect_content=None, thumb=None, business_connection_id=None, message_effect_id=None, **kw) -> types.Message:
    return self._send("send_document", locals())

  def send_sticker(self, sticker, reply_markup=None, disable_notification=None, timeout=None, allow_sending_without_reply=None, protect_content=None, data=None, emoji=None, business_connection_id=None, message_effect_id=None, **kw) -> types.Message:
    return self._send("send_sticker", locals())

  def send_video(self, video, duration=None, width=None, height=None, thumbnail=None, caption=None, parse_mode=None, caption_entities=None, supports_streaming=None, disable_notification=None, protect_content=None, allow_sending_without_reply=None, reply_markup=None, timeout=None, data=None, has_spoiler=None, thumb=None, business_connection_id=None, message_effect_id=None, show_caption_above_media=None, **kw) -> types.Message:
    return self._send("send_video", locals())

  def send_media_group(self, media, disable_notification, protect_content, timeout, allow_sending_without_reply, business_connection_id=None, message_effect_id=None, **kw) -> List[types.Message]:
    return self._send("send_media_group", locals())

  def send_location(self, latitude, longitude, live_period=None, reply_markup=None, disable_notification=None, timeout=None, horizontal_accuracy=None, heading=None, proximity_alert_radius=None, allow_sending_without_reply=None, protect_content=None, business_connection_id=None, message_effect_id=None) -> types.Message:
    return self._send("send_location", locals())


class TeleBotPlus(telebot.TeleBot):
  TELEBOT_TESTED_VERSIONS = ()
  TELEBOT_COMPATIBLE_VERSIONS = ()

  def __init__(self,
               token: str,
               parse_mode: Optional[str] = None,
               threaded: Optional[bool] = True,
               skip_pending: Optional[bool] = False,
               num_threads: Optional[int] = 2,
               next_step_backend: Optional[telebot.HandlerBackend] = None,
               reply_backend: Optional[telebot.HandlerBackend] = None,
               exception_handler: Optional[telebot.ExceptionHandler] = None,
               last_update_id: Optional[int] = 0,
               suppress_middleware_excepions: Optional[bool] = False,
               state_storage: Optional[telebot.StateStorageBase] = telebot.StateMemoryStorage(),
               use_class_middlewares: Optional[bool] = False,
               disable_web_page_preview: Optional[bool] = None,
               disable_notification: Optional[bool] = None,
               protect_content: Optional[bool] = None,
               allow_sending_without_reply: Optional[bool] = None,
               colorful_logs: Optional[bool] = False,
               **kw):
    args = locals()
    for i in args_names["__init__"]:
      if i in args:
        kw[i] = args[i]
    kw["self"] = self
    exec("self.__getattr__=self._getattr")  # Чтобы VSCode не задерживалось на __getattr__
    # self.MAX_CHATMESSAGES_PER_MINUTE = 20  # Максимум сообщений в минуту на чат
    # self.MAX_REQUESTS_PER_SECOND = 30  # Максимум запросов в секунду
    self.stats: dict[str, int] = {}  # Статистика использования изменённых функций
    telebot.TeleBot.__init__(**kw)  # Создание оригинального бота
    self._assets = None
    # self.queue = Queue()  # Очередь
    # self.queue_thread = Thread(target=self._queue_sender, daemon=False)
    # self.queue_thread.start()  # Запуск обработчика очереди

    for k, v in SHORT_NAMES.items():
      if hasattr(self, k):
        for i in v:
          setattr(self, i, getattr(self, k))  # Сокращение названий функций

  @property
  def assets(self) -> Assets:
    if self._assets is None:
      self._assets = Assets(bot=self)
    return self._assets

  def _getattr(self, k: str):
    """Если функция отсутствует, будет использована из оригинального бота"""
    if k in self.__dict__:
      return self.__dict__[k]
    else:
      result = getattr(telebot.TeleBot, k)
      if callable(result):
        @wraps(result)
        def wrapper(*args, **kwargs):
          ps, kw = ms.utils.args2kwargs(result, args, kwargs)
          self._prep_kw(kw, result)
          return result(*ps, **kw)
        return wrapper
      return result

  def _is_patched(self, k: str):
    """Изменён ли аттрибут или взят из оригинала"""
    if k in dir(telebot.TeleBot):
      return False
    return True

  def _is_original(self, k: str):
    if k in dir(telebot.TeleBot):
      return True
    return False

  def _call_original(self, _name, **kw):
    """Вызвать функцию оригинального бота"""
    self._prep_kw(kw, _name)
    result = getattr(telebot.TeleBot, _name)(**kw)
    if not _name in self.stats:
      self.stats[_name] = 0
    self.stats[_name] += 1
    return result

  def _prep_kw(self, kw: dict[str, Any], names: Union[str, Callable, Iterable] = None, copy: bool = False) -> dict[str, Any]:
    if copy:
      kw = kw.copy()
    kw["self"] = self
    if kw.get("message_id") != None:
      msg = kw["message_id"]
      if type(msg) == types.Message:
        kw["message_id"] = msg.id
        if kw.get("chat_id") == None:
          kw["chat_id"] = msg
    if kw.get("reply_to_message_id") != None:
      msg = kw.pop("reply_to_message_id")
      rp_kw = {}
      if type(msg) == types.Message:
        rp_kw["chat_id"] = msg.chat.id
        rp_kw["message_id"] = msg.id
      else:
        rp_kw["message_id"] = msg
      if "allow_sending_without_reply" in kw:
        allow_sending_without_reply = kw.pop("allow_sending_without_reply")
      else:
        allow_sending_without_reply = None
      rp_kw["allow_sending_without_reply"] = self.allow_sending_without_reply if (allow_sending_without_reply is None) else allow_sending_without_reply
      if kw.get("reply_parameters") != None:
        for k, v in rp_kw.items():
          setattr(kw["reply_parameters"], k, v)
      else:
        kw["reply_parameters"] = types.ReplyParameters(**rp_kw)
      if kw.get("chat_id") == None:
        kw["chat_id"] = msg
    if kw.get("from_chat_id") != None:
      if type(kw["from_chat_id"]) in [types.Chat, types.User]:
        chat = kw["from_chat_id"]
        kw["from_chat_id"] = chat.id
      if type(kw["from_chat_id"]) == types.Message:
        msg = kw["from_chat_id"]
        kw["from_chat_id"] = msg.chat.id
    if kw.get("chat_id") != None:
      if type(kw["chat_id"]) in [types.Chat, types.User]:
        chat = kw["chat_id"]
        kw["chat_id"] = chat.id
      if type(kw["chat_id"]) == types.Message:
        msg = kw["chat_id"]
        kw["chat_id"] = msg.chat.id
        # kw["message_thread_id"] = msg.message_thread_id
    if kw.get("timeout") != None:
      if type(kw["timeout"]) == timedelta:
        kw["timeout"] = kw["timeout"].total_seconds()
    if names != None:
      if type(names) == str:
        names = getattr(telebot.TeleBot, names)
      if callable(names):
        func = names
        names = tuple(inspect.signature(func).parameters.keys())
      for i in kw:
        if not i in names:
          kw.pop(i)
    return kw

  def Reply(self, msg: types.Message) -> Reply2Message:
    return Reply2Message(self, msg)

  def send_document(self,
                    chat_id: Union[int, str],
                    document: Union[Any, str],
                    reply_to_message_id: Optional[int] = None,
                    caption: Optional[str] = None,
                    reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
                    parse_mode: Optional[str] = None,
                    disable_notification: Optional[bool] = None,
                    timeout: Optional[int] = None,
                    thumbnail: Optional[Union[Any, str]] = None,
                    caption_entities: Optional[List[types.MessageEntity]] = None,
                    allow_sending_without_reply: Optional[bool] = None,
                    visible_file_name: Optional[str] = None,
                    disable_content_type_detection: Optional[bool] = None,
                    data: Optional[Union[Any, str]] = None,
                    protect_content: Optional[bool] = None,
                    message_thread_id: Optional[int] = None,
                    thumb: Optional[Union[Any, str]] = None,
                    reply_parameters: Optional[types.ReplyParameters] = None,
                    business_connection_id: Optional[str] = None,
                    message_effect_id: Optional[str] = None,
                    auto_close_file: bool = True,
                    **kw,
                    ) -> types.Message:
    args = locals()
    for i in args_names["send_document"]:
      if i in args:
        kw[i] = args[i]
    asset = None
    if type(document) == "str":
      if len(document) == self.assets.ID_LEN:
        asset = self.assets.get(document, "document", bot=self)
        if asset != None:
          kw["document"] = asset["file"]
          if visible_file_name == None:
            file_renamed = False
            if "name" in asset:
              if asset["name"]:
                kw["visible_file_name"] = asset["name"]
                file_renamed = True
            if not file_renamed:
              if "extension" in asset:
                if asset["extension"]:
                  kw["visible_file_name"] = "unknown." + asset["extension"]
                  file_renamed = True
            if not file_renamed:
              kw["visible_file_name"] = "unknown"
              file_renamed = True
    result: types.Message = self._call_original("send_document", **kw)
    if asset != None:
      self.assets.set_file_id(asset["id"], result.document.file_id, "document", bot=self)
    if auto_close_file:
      if hasattr(kw["document"], "close"):
        if callable(kw["document"].close):
          kw["document"].close()
    return result

  def send_photo(self,
                 chat_id: Union[int, str],
                 photo: Union[Any, str],
                 caption: Optional[str] = None,
                 parse_mode: Optional[str] = None,
                 caption_entities: Optional[List[types.MessageEntity]] = None,
                 disable_notification: Optional[bool] = None,
                 protect_content: Optional[bool] = None,
                 reply_to_message_id: Optional[int] = None,
                 allow_sending_without_reply: Optional[bool] = None,
                 reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
                 timeout: Optional[int] = None,
                 message_thread_id: Optional[int] = None,
                 has_spoiler: Optional[bool] = None,
                 reply_parameters: Optional[types.ReplyParameters] = None,
                 business_connection_id: Optional[str] = None,
                 message_effect_id: Optional[str] = None,
                 show_caption_above_media: Optional[bool] = None,
                 auto_close_file: bool = True,
                 **kw,
                 ) -> types.Message:
    args = locals()
    for i in args_names["send_photo"]:
      if i in args:
        kw[i] = args[i]
    asset = None
    if type(photo) == "str":
      if len(photo) == self.assets.ID_LEN:
        asset = self.assets.get(photo, "photo", bot=self)
        if asset != None:
          kw["photo"] = asset["file"]
    result: types.Message = self._call_original("send_photo", **kw)
    if asset != None:
      self.assets.set_file_id(asset["id"], result.photo[-1].file_id, "photo", bot=self)
    if auto_close_file:
      if hasattr(kw["photo"], "close"):
        if callable(kw["photo"].close):
          kw["photo"].close()
    return result

  def send_message(self,
                   chat_id: Union[int, str],
                   text: str,
                   parse_mode: Optional[str] = None,
                   entities: Optional[List[types.MessageEntity]] = None,
                   disable_web_page_preview: Optional[bool] = None,
                   disable_notification: Optional[bool] = None,
                   protect_content: Optional[bool] = None,
                   reply_to_message_id: Optional[int] = None,
                   allow_sending_without_reply: Optional[bool] = None,
                   reply_markup: Optional[telebot.REPLY_MARKUP_TYPES] = None,
                   timeout: Optional[int] = None,
                   message_thread_id: Optional[int] = None,
                   reply_parameters: Optional[types.ReplyParameters] = None,
                   link_preview_options: Optional[types.LinkPreviewOptions] = None,
                   business_connection_id: Optional[str] = None,
                   message_effect_id: Optional[str] = None,
                   **kw,
                   ) -> types.Message:
    args = locals()
    for i in args_names["send_message"]:
      if i in args:
        kw[i] = args[i]
    result: types.Message = self._call_original("send_message", **kw)
    return result
