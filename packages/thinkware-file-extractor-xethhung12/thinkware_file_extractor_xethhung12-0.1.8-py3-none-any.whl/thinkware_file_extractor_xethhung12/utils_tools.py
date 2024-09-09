import json
import os

width_for_4k="3840"
width_for_2k="2560"

def get_scale(val) -> str:
  if val == width_for_4k:
    return "940"
  elif val == width_for_2k:
    return "740"
  else:
    return "UNKNOWN"

def  get_x(val) -> str:
  if val == width_for_4k:
    return "420"
  elif val == width_for_2k:
    return "350"
  else:
    return "UNKNOWN"

def get_y(val) -> str:
  if val == width_for_4k:
    return "1500"
  elif val == width_for_2k:
    return "980"
  else:
    return "UNKNOWN"


class MP4View:
  def __init__(self, map):
    self.map = map

  def get_width(self)->int:
    return self.map["width"]

  def get_height(self)->int:
    return self.map["height"]

  def get_codec(self)->str:
    return self.map["codec_name"]

  def get_codec_long_name(self)->str:
    return self.map["codec_long_name"]

def mp4view(f_name)->MP4View:
  abs_file_name = str(os.path.abspath(f_name))
  cmd = f"ffprobe -v error -select_streams v -show_streams -of json {abs_file_name}"
  out = os.popen(cmd).read()
  d = json.loads(out)
  return MP4View(d["streams"][0])


# if __name__ == "__main__":
#   if sys.argv[1] == "scale":
#     print(get_scale())
#   elif sys.argv[1] == "x":
#     print(get_x())
#   elif sys.argv[1] == "y":
#     print(get_y())
#   else:
#     sys.exit(1)
