from MainShortcuts2 import ms


def id_bot2client(id: int):
  id = str(id)
  if id.startswith("-100"):
    return int(id[4:])
  elif id.startswith("-"):
    return int(id[1:])
  else:
    return int(id)


async_download_file = ms.utils.async_download_file
async2sync = ms.utils.async2sync
download_file = ms.utils.sync_download_file
riot = ms.utils.riot
sync_download_file = ms.utils.sync_download_file
sync2async = ms.utils.sync2async
