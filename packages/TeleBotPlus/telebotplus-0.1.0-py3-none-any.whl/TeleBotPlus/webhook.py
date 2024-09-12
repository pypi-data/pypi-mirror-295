"""/bot/lib/webhooks.py"""
import atexit
import ssl
from . import TeleBotPlus
from telebot import types
from threading import Thread
from typing import Union
from urllib.parse import urlparse
PRIORITIES = ["aiohttp", "flask", "http"]


class WebhookListener:
  """Прослушивание вебхука первой из доступных библиотек (`aiohttp`,`flask`,`http`)"""

  def __init__(self, *,
               atexit_reg: bool = True,
               auto_import: bool = True,
               bot: TeleBotPlus,
               cert_pass: str = None,
               cert_priv: str,
               cert_pub: str,
               host: str = "0.0.0.0",
               port: int,
               secret_token: str,
               set_webhook_kw: dict = None,
               set_webhook: bool = True,
               url: str,
               ):
    url_path = urlparse(url).path
    self._running = False
    self.app_name: str = None
    self.app = None
    self.bot: TeleBotPlus = bot[0] if type(bot) == tuple else bot
    self.cert_pass: str = cert_pass
    self.cert_priv: str = cert_priv
    self.cert_pub: str = cert_pub
    self.host: str = host
    self.port: int = port
    self.secret_token: str = secret_token
    self.ssl_context: ssl.SSLContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    self.url_path: str = url_path[:-1] if url_path.endswith("/") else url_path
    self.url: str = url
    self.ssl_context.load_cert_chain(self.cert_pub, self.cert_priv, self.cert_pass)
    if atexit_reg:
      atexit.register(self.stop)
    if auto_import:
      self.import_app()
    if set_webhook:
      bot.remove_webhook()
      if set_webhook_kw is None:
        set_webhook_kw = {}
      with open(self.cert_pub, "rb") as f:
        set_webhook_kw["certificate"] = f
        set_webhook_kw["secret_token"] = self.secret_token
        set_webhook_kw["url"] = self.url
        bot.set_webhook(**set_webhook_kw)

  @property
  def running(self) -> bool:
    if self.app_name == "http":
      return self.app.__is_shut_down.is_set()
    return self._running

  def start(self, timeout: Union[None, float] = None):
    """Запустить прослушивание вебхука"""
    if self.running:
      return
    t = Thread(daemon=False, target=self._start)
    t.start()
    self._running = True
    if timeout == 0:
      return
    t.join(timeout)

  def stop(self, timeout: Union[None, float] = None):
    """Остановить вебхук"""
    if self.running:
      t = Thread(daemon=False, target=self._stop)
      t.start()
      if timeout == 0:
        return
      t.join(timeout)
      self._running = False

  def import_app(self, priorities: list[str] = PRIORITIES):
    """Импортировать первую доступную библиотеку"""
    for i in priorities:
      try:
        app, start, stop = getattr(self, i)()
        self._start = start
        self._stop = stop
        self.app_name = i
        self.app = app
        return
      except Exception:
        pass
    raise ImportError("There are no available libraries")

  def aiohttp(self, app_kw={}, run_kw={}):
    import asyncio
    from aiohttp import web
    app = web.Application(**app_kw)

    async def handle(request: web.Request):
      if request.headers.get("X-Telegram-Bot-Api-Secret-Token") == self.secret_token:
        self.bot.process_new_updates([types.Update.de_json((await request.read()).decode("utf-8"))])
        return web.Response(status=200)
      else:
        return web.Response(status=403)
    app.router.add_post(self.url_path, handle)
    app.router.add_post(self.url_path + "/", handle)
    run_kw["app"] = app
    run_kw["host"] = self.host
    run_kw["port"] = self.port
    run_kw["ssl_context"] = self.ssl_context

    def start():
      web.run_app(**run_kw)

    def stop():
      asyncio.run(app.shutdown())
    return app, start, stop

  def flask(self, app_kw={}, run_kw={}):
    from flask import Flask, request, Response
    app = Flask("webhook")

    def handler():
      if request.headers.get("X-Telegram-Bot-Api-Secret-Token") == self.secret_token:
        self.bot.process_new_updates([types.Update.de_json(request.get_data().decode("utf-8"))])
        return Response(status=200)
      else:
        return Response(status=403)
    app.route(self.url_path, methods=["POST"])(handler)
    app.route(self.url_path + "/", methods=["POST"])(handler)
    run_kw = {}
    run_kw["host"] = self.host
    run_kw["port"] = self.port
    run_kw["ssl_context"] = self.ssl_context

    def start():
      app.run(**run_kw)

    def stop():
      func = request.environ.get("werkzeug.server.shutdown")
      if func == None:
        raise RuntimeError("Not running with the Werkzeug Server")
      func()
    return app, start, stop

  def http(whl, app_kw={}, run_kw={}):
    from http.server import BaseHTTPRequestHandler, HTTPServer

    class Handler(BaseHTTPRequestHandler):
      server_version = "Handler/1.0"

      def do_HEAD(self):
        self.send_response(200)
        self.end_headers()

      def do_GET(self):
        self.send_response(200)
        self.end_headers()

      def do_POST(self):
        if (self.path[:-1] if self.path.endswith("/") else self.path) == self.url_path:
          if self.headers.get("X-Telegram-Bot-Api-Secret-Token") == self.secret_token:
            data = self.rfile.read(int(self.headers["content-length"])).decode("utf-8")
            self.send_response(200)
            self.end_headers()
            whl.bot.process_new_messages([types.Update.de_json(data)])
            return
        self.send_error(403)
        self.end_headers()
        HTTPServer.__init__()
    app_kw["server_address"] = (whl.host, whl.port)
    app_kw["RequestHandlerClass"] = Handler
    app = HTTPServer(**app_kw)
    app.socket = whl.ssl_context.wrap_socket(app.socket, server_side=True)

    def start():
      app.serve_forever(**run_kw)

    def stop():
      app.shutdown()
      app.server_close()
    return app, start, stop
