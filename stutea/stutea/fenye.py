import math
class pages:
    def __init__(self):
        pass

    def fenye(self,total, curr_page, url,items=4):
        str = '''<a href="%s?page=0" style="padding:10px">首页</a>
            ''' % (url)
        up = curr_page - 1 if curr_page - 1 > 0 else 0
        str += '''<a href="%s?page=%s" style="padding:10px">上一页</a>
                ''' % (url, up)
        before = curr_page if curr_page < math.floor(items/2) else math.floor(items/2)
        for item in range(before, 0, -1):
            num = before - item
            if num == curr_page:
                str += '''<a href="%s?page=%s" style="color:red;padding:10px">%s</a>
                ''' % (url, num, num + 1)
            else:
                str += '''<a href="%s?page=%s" style="padding:10px">%s</a>
                            ''' % (url, before - item, curr_page - item + 1)
        after = items - before
        for item in range(after):
            num = curr_page + item
            if (num < total):
                if num == curr_page:
                    str += '''<a href="%s?page=%s" style="color:red;padding:10px">%s</a>
                ''' % (url, num, num + 1)
                else:
                    str += '''<a href="%s?page=%s" style="padding:10px">%s</a>
                                ''' % (url, num, num + 1)
        next = curr_page + 1 if curr_page + 1 < total else curr_page
        str += '''<a href="%s?page=%s" style="padding:10px">下一页</a>
                    ''' % (url, next)
        str += '''<a href="%s?page=%s" style="padding:10px">尾页</a>
            ''' % (url, total - 1)
        return str