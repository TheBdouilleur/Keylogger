import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
# Created by pyminifier (https://github.com/liftoff/pyminifier)