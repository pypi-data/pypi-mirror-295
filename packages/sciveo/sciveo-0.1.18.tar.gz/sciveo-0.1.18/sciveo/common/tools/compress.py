import json
import gzip
import base64

from sciveo.common.tools.logger import *


class CompressJsonData:
  def __init__(self) -> None:
    pass

  def compress(self, data):
    json_data = json.dumps(data).encode('utf-8')
    compressed_data = gzip.compress(json_data)
    encoded_data = base64.b64encode(compressed_data).decode('utf-8')
    debug(type(self).__name__, "compress", len(json_data), "->", len(encoded_data))
    return encoded_data

  def decompress(self, encoded_data):
    compressed_data = base64.b64decode(encoded_data)
    decompressed_data = gzip.decompress(compressed_data)
    json_data = decompressed_data.decode('utf-8')
    data = json.loads(json_data)
    debug(type(self).__name__, "decompress", len(encoded_data), "->", len(json_data))
    return data

