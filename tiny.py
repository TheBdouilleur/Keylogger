import zlib, base64
exec(zlib.decompress(base64.b64decode('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')))
# Created by pyminifier (https://github.com/liftoff/pyminifier)