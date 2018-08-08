import hashlib
def md5(data):
    m=hashlib.md5()
    m.update(data.encode(encoding="utf8"))
    return m.hexdigest()
