from django.shortcuts import HttpResponse,render,redirect
import pymysql
from .sqlfenzhung import sql
db = pymysql.connect("localhost", "root", "123456", "stusys", charset="utf8",cursorclass=(pymysql.cursors.DictCursor))
from .hash import *
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import json
import math
import hashlib
def login(request):
    if request.method == 'GET':
        if request.session.get("login")=="yes":
            return redirect(studentIndex)
        else:
            return render(request,"login.html")
    elif request.method == 'POST':
        name=request.POST.get("user")
        pass1=request.POST.get("pass")
        sign=request.POST.get("sign")
        save=request.POST.get("save")
        cursor=db.cursor()
        sql="select * from user where userName='%s'and pass='%s'and sign='%s'"%(name,md5(pass1),sign)
        cursor.execute(sql)
        result=cursor.fetchall()
        print(result)
        if len(result)>0:
            if save:
                obj = redirect(studentIndex)
                request.session['login'] = "yes"
                request.session['name'] = name
                request.session.set_expiry(7*12*60*60)
                return obj
            else:
                obj = redirect(studentIndex)
                request.session['login'] = "yes"
                request.session['name'] = name
                request.session.set_expiry(0)
                return obj
                # obj.set_signed_cookie("login","yes",salt='migedan')
        else:
            status = 1
            return HttpResponse(json.dumps({
                "status": status,
            }))
def reg(request):
    if request.method=="GET":
        return render(request,"reg.html")
    elif request.method=="POST":
        name1 = request.POST.get("user")
        pass1 = request.POST.get("pass")
        sign = request.POST.get("sign")
        cursor = db.cursor()
        sql="insert into user (userName,pass,sign) values ('%s','%s','%s') " %(name1,md5(pass1),sign)
        cursor.execute(sql)
        db.commit()
        return redirect(login)
def out(request):
    del request.session["login"]
    del request.session["name"]
    return render(request,"login.html")
def studentIndex(request):
    if request.session.get("login")=="yes":
        return render(request, "StudentIndex.html")
    else:
        return redirect(login)
def studentInfo(request):
    cur_page = int(request.GET.get("page")) if request.GET.get("page") else 0
    num=10
    cursor = db.cursor()
    sql = "select stu.snum,stu.snuion,stu.sname,stu.ssex,classr.cname,group_concat(teacher.tname) as tname from stu left join classr on stu.cnum=classr.cnum left join classtea on classtea.cnum=stu.cnum left join teacher on teacher.tnum=classtea.tnum group by stu.snum limit %s,%s"%(cur_page*num,num)
    cursor.execute(sql)
    date = cursor.fetchall()
    #arr={}
    # for item in date:
    #     if not item["snum"] in arr:
    #         arr[item["snum"]]=item
    #         arr[item["snum"]]["tname"]=[item["tname"]]
    #     else:
    #         arr[item["snum"]]["tname"].append(","+item["tname"])
    # Contacts=arr.values()
    count = "select count(*) from stu left join classr on stu.cnum=classr.cnum left join classtea on classtea.cnum=stu.cnum left join teacher on teacher.tnum=classtea.tnum group by stu.snum"
    cursor.execute(count)
    count = math.ceil(len(cursor.fetchall())/num)
    str = pages(count, cur_page, "/studentInfo/")
    return render(request, "studentInfo.html", {"date": date, "str": str})
def add(request):
    if request.method=="GET":
        cursor = db.cursor()
        sql = "select * from classr"
        cursor.execute(sql)
        date = cursor.fetchall()
        return render(request,"add.html",{"date":date})
    elif request.method=="POST":
        sname = request.POST.get("sname")
        snuion = request.POST.get("snuion")
        ssex = request.POST.get("ssex")
        date = request.POST.get("date")
        cnum = request.POST.get("cnum")
        cursor = db.cursor()
        sql = "insert into stu (snuion,sname,ssex,date,cnum) values ('%s','%s','%s','%s',%s) " %(snuion,sname, ssex, date,cnum)
        cursor.execute(sql)
        db.commit()
        return redirect(studentInfo)
def addCon(request):
    attr= request.GET.get("attr")
    val= request.GET.get("val")
    snum= request.GET.get("snum")
    cursor = db.cursor()
    print(attr,val)
    if attr=="sname":
        sql = "update stu set %s='%s'where snum=%s" %(attr, val,snum)
    elif attr=="ssex":
        if val=="女":
            sql="update stu set %s='%s' where snum=%s" %(attr,'0',snum)
        else:
            sql = "update stu set %s='%s' where snum=%s" % (attr, '1',snum)
    elif attr=="cname":
        sql1="select * from classr where cname='%s'"%(val)
        cursor.execute(sql1)
        result=cursor.fetchone()["cnum"]
        sql="update stu set %s='%s'" %(attr, result)
    cursor.execute(sql)
    db.commit()
    return redirect(studentInfo)
def dele(request):
    id = request.GET.get("id")
    cursor = db.cursor()
    sql = "delete from stu where snum=" + id
    cursor.execute(sql)
    db.commit()
    return redirect(studentInfo)
def edit(request):
    snum=request.GET.get("id")
    if request.method=="GET":
        cursor = db.cursor()
        sql="select * from stu,classr where stu.cnum=classr.cnum and snum="+snum
        cursor.execute(sql)
        date=cursor.fetchall()
        sql1 = "select * from classr "
        cursor.execute(sql1)
        date1 = cursor.fetchall()
        date[0]["date"]=str(date[0]["date"])
        return render(request,"edit.html",{"date":date,"date1":date1})
    elif request.method=="POST":
        snum = request.GET.get("id")
        sname = request.POST.get("sname")
        snuion = request.POST.get("snuion")
        ssex = request.POST.get("ssex")
        date = request.POST.get("date")
        cnum = request.POST.get("cnum")
        cursor = db.cursor()
        sql = "update stu set snuion='%s',sname='%s',ssex='%s',date='%s',cnum='%s' where snum='%s'" % (snuion,sname, ssex, date, cnum,snum)
        cursor.execute(sql)
        db.commit()
        return redirect(studentInfo)
def search(request):
    sname=request.GET.get("aa")
    cursor = db.cursor()
    sql = "select * from stu where sname='%s'"%(sname)
    cursor.execute(sql)
    result = cursor.fetchall()
    return render(request, "studentInfo.html", {"date": result})

# 教师信息的设置
def teacherInfo(request):
    curr_page=int(request.GET.get("page")) if request.GET.get("page") else 0
    num=10
    cursor = db.cursor()
    # sql = "select teacher.tnum,teacher.tname,classr.cnum from teacher left join classr on teacher.tnum=classr.cnum"
    sql = "select *,group_concat(stage.staname) as stanames from teacher left join stage on find_in_set(stage.staid,teacher.staid) group by teacher.tunion  order by teacher.tnum asc limit %s,%s "%(curr_page*num,num)
    cursor.execute(sql)
    date = cursor.fetchall()
    print(date)
    # arr={}
    # for item in date:
    #     if not item["tnum"] in arr:
    #         arr[item["tnum"]]=item
    #         arr[item["tnum"]]["cname"]=[item["cname"]]
    #     else:
    #         arr[item["tnum"]]["cname"].append(","+item["cname"])
    # date=arr.values()
    # 分页
    count="select count(*) from teacher left join classtea on teacher.tnum=classtea.tnum left join classr on classtea.cnum=classr.cnum group by teacher.tnum "
    cursor.execute(count)
    count=math.ceil(len(cursor.fetchall())/num)
    str=pages(count,curr_page,"/teacherInfo/")
    return render(request, "teacherInfo.html", {"date": date,"str":str})
def teadele(request):
    tunion = request.GET.get("id")
    cursor = db.cursor()
    sql = "delete from teacher where tunion=%s"
    cursor.execute(sql,[tunion])
    # sql1="delete from classtea where tnum="+id
    #sql = "delete teacher,classtea from teacher left join classtea on teacher.tnum=classtea.tnum where teacher.tnum=%s"
    sql1="update classtea set tnum='' where tnum=%s"
    cursor.execute(sql1,[tunion])
    db.commit()
    return redirect(teacherInfo)
def teasearch(request):
    sname = request.GET.get("aa")
    cursor = db.cursor()
    sql = "select * from teacher where tname='%s'" % (sname)
    cursor.execute(sql)
    result = cursor.fetchall()
    return render(request, "teacherInfo.html", {"date": result})
def teacheradd(request):
    if request.method == "GET":
        cursor = db.cursor()
        # sql="select * from classr"
        # cursor.execute(sql)
        # date=cursor.fetchall()
        sql="select * from stage"
        cursor.execute(sql)
        date=cursor.fetchall()
        return render(request, "teacheradd.html",{"date":date})
    elif request.method == "POST":
        tname = request.POST.get("tname")
        tunion = request.POST.get("tunion")
        tsex=request.POST.get("tsex")
        date=request.POST.get("date")
        staid=request.POST.getlist("staid")
        # staids为列表，[1,2,3]  "1,2,3"( FIND_IN_SET("跑步",love))
        staids=""
        for item in staid:
            staids+=item+","
        staids=staids[:-1]
        cursor = db.cursor()
        sql = "insert into teacher ( tname,tsex,date,tunion,staid) values (%s,%s,%s,%s,%s) "
        cursor.execute(sql,[tname,tsex,date,tunion,staids])
        tnum=db.insert_id()
        db.commit()
        # arr=[]
        # for item in cnums:
        #     yz=(tnum,item)
        #     arr.append(yz)
        # sql="insert into classtea(tnum,cnum) values ('%s',%s)"
        # cursor.executemany(sql,arr)
        # db.commit()
        return redirect(teacherInfo)
def teacheredit(request):
    tnum = request.GET.get("id")
    if request.method == "GET":
        cursor = db.cursor()
        sql = "select * from teacher where tunion=%s"
        cursor.execute(sql,[tnum])
        date = cursor.fetchall()
        sql1 = "select * from stage "
        cursor.execute(sql1)
        date1 = cursor.fetchall()
        date[0]["date"] = str(date[0]["date"])
        return render(request, "teacheredit.html", {"date": date, "date1": date1})
    elif request.method == "POST":
        tnum = request.GET.get("id")
        tname = request.POST.get("tname")
        tunion = request.POST.get("tunion")
        tsex = request.POST.get("tsex")
        date = request.POST.get("date")
        staid = request.POST.getlist("staid")
        staids=""
        for item in staid:
            staids+=item+","
        staids=staids[:-1]
        cursor = db.cursor()
        sql = "update teacher set tunion='%s',tname='%s',tsex='%s',date='%s',staid='%s' where tunion='%s'" % (
        tunion,tname, tsex, date,staids,tnum)
        cursor.execute(sql)
        sql1 = "update classtea set tnum=%s where tnum=%s"
        cursor.execute(sql1, [tunion,tnum])
        db.commit()
        # # 删除
        # cursor = db.cursor()
        # sql2 = "delete from classtea where tnum=" + tnum
        # cursor.execute(sql2)
        # db.commit()
        # #插入
        # arr = []
        # for item in cnums:
        #     yz = (tnum, item)
        #     arr.append(yz)
        # sql = "insert into classtea(tnum,cnum) values (%s,%s)"
        # cursor.executemany(sql, arr)
        # db.commit()
        # cursor = db.cursor()
        # sql1="select * from classtea where tnum="+tnum
        # cursor.execute(sql1)
        # ids=cursor.fetchall()
        # print(ids)
        return redirect(teacherInfo)
# 班级信息
def classInfo(request):
    curr_page=request.GET.get("page") if request.GET.get("page") else 0
    num = 10
    curr_page =int(curr_page)
    cursor = db.cursor()
    sql = "select classr.cnum,classr.cname,grade.gname,group_concat(stage.staname) as staname,group_concat(teacher.tname) as tname from classr left join grade on classr.gid=grade.gid left join classtea on classr.cnum=classtea.cnum left join teacher on classtea.tnum=teacher.tunion left join stage on classtea.staid=stage.staid  group by grade.gname,classr.cnum limit %s,%s"%(curr_page*num,int(num))
    cursor.execute(sql)
    date = cursor.fetchall()
    #arr={}
    # for item in date:
    #     if not item["cnum"] in arr:
    #         arr[item["cnum"]]=item
    #         arr[item["cnum"]]["tname"]=[item["tname"]]
    #     else:
    #         arr[item["cnum"]]["tname"].append(","+item["tname"])
    #         arr[item["cnum"]]["sumtea"] =len(arr[item["cnum"]]["tname"])
    # date=arr.values()
    # for item in date:
    #     sql1="select * from stu where cnum=%s"
    #     cursor.execute(sql1,[item["cnum"]])
    #     item["sumstu"]=len(cursor.fetchall())
    # 分页
    count="select count(*) from classr left join classtea on classr.cnum=classtea.cnum  left join teacher on classtea.tnum=teacher.tnum group by classr.cnum"
    cursor.execute(count)
    count=math.ceil(len(cursor.fetchall())/num)
    str=pages(count,curr_page,"/classInfo/",items=4)
    return render(request, "classInfo.html", {"date": date,"str":str})

def classdele(request):
    id = request.GET.get("id")
    cursor = db.cursor()
    # sql = "delete from classr where cnum=" + id
    # cursor.execute(sql)
    # sql1 = "delete from classtea where cnum=" + id
    sql = "delete classr,classtea from classr left join classtea on classr.cnum=classtea.cnum where classr.cnum=%s"
    cursor.execute(sql,[id])
    db.commit()
    return redirect(classInfo)
def classsearch(request):
    cname=request.GET.get("aa")
    cursor = db.cursor()
    sql = "select * from classr where cname='%s'"%(cname)
    cursor.execute(sql)
    result = cursor.fetchall()
    return render(request, "classInfo.html", {"date": result})
def classadd(request):
    if request.method == "GET":
        cursor = db.cursor()
        sql="select * from grade"
        cursor.execute(sql)
        date= cursor.fetchall()
        return render(request, "classadd.html",{"date":date})
    elif request.method == "POST":
        info = request.POST.get("info")
        cname = request.POST.get("cname")
        gid = request.POST.get("gid")
        cursor = db.cursor()
        sql = "insert into classr (cname,gid) values ('%s','%s') " % (cname,gid)
        cursor.execute(sql)
        cid=db.insert_id()
        db.commit()
        info=json.loads(info)
        result=info.values()
        arr=[]
        for item in result:
            yz=(item["tnum"],cid,item["staid"])
            arr.append(yz)
        sql="insert into classtea (tnum,cnum,staid) values (%s,%s,%s)"
        cursor.executemany(sql,arr)
        db.commit()
        return redirect(classInfo)
def classedit(request):
    cnum = request.GET.get("id")
    if request.method == "GET":
        cursor = db.cursor()
        sql = "select classr.cnum,classr.gid,classr.cname,group_concat(teacher.tunion) as tunion,group_concat(teacher.tname) as tname,group_concat(stage.staid) as staid,group_concat(stage.staname) as staname from classr left join classtea on classr.cnum=classtea.cnum left join teacher on classtea.tnum=teacher.tunion left join  stage on classtea.staid=stage.staid where classr.cnum=%s group by classr.cnum "%(cnum)
        cursor.execute(sql)
        date = cursor.fetchall()
        sql1 = "select * from grade"
        cursor.execute(sql1)
        date1 = cursor.fetchall()
        return render(request, "classedit.html", {"date": date,"date1":date1})
    elif request.method == "POST":
        cnum = request.GET.get("id")
        info = request.POST.get("info")
        cname = request.POST.get("cname")
        gid = request.POST.get("gid")
        cursor = db.cursor()
        sql = "update classr set cname='%s',gid='%s' where  cnum='%s'" % (cname,gid,cnum)
        cursor.execute(sql)
        db.commit()
        sql1="delete from classtea where cnum='%s'"%(cnum)
        cursor.execute(sql1)
        db.commit()
        info = json.loads(info)
        result = info.values()
        arr = []
        for item in result:
            yz = (item["tnum"], cnum, item["staid"])
            arr.append(yz)
        sql = "insert into classtea (tnum,cnum,staid) values (%s,%s,%s)"
        cursor.executemany(sql, arr)
        db.commit()
        return redirect(classInfo)
def pages(total,curr_page,url,items=4):
    str = '''<a href="%s?page=0" style="padding:10px">首页</a>
        '''%(url)
    up=curr_page-1 if curr_page-1>0 else 0
    str += '''<a href="%s?page=%s" style="padding:10px">上一页</a>
            ''' % (url,up)

    before= curr_page if curr_page<math.floor(items/2) else math.floor(items/2)
    for item in range(before,0,-1):
        num=before-item
        if  num==curr_page:
            str+='''<a href="%s?page=%s" style="color:red;padding:10px">%s</a>
            '''%(url,num,num+1)
        else:
            str += '''<a href="%s?page=%s" style="padding:10px">%s</a>
                        ''' % (url, before - item, curr_page - item + 1)
    after = items-before
    for item in range(after):
        num=curr_page+item
        if (num<total):
            if num==curr_page:
                str += '''<a href="%s?page=%s" style="color:red;padding:10px">%s</a>
            ''' % (url,num, num+1)
            else:
                str += '''<a href="%s?page=%s" style="padding:10px">%s</a>
                            ''' % (url, num, num + 1)
    next = curr_page + 1 if curr_page + 1 < total else curr_page
    str += '''<a href="%s?page=%s" style="padding:10px">下一页</a>
                ''' % (url,next)
    str += '''<a href="%s?page=%s" style="padding:10px">尾页</a>
        ''' % (url, total - 1)
    return str
# 异步验证
def ajax(request):
    cursor = db.cursor()
    tunion = request.GET.get("tunion")
    sql = "select * from teacher where tunion=%s"
    cursor.execute(sql,[tunion])
    result=cursor.fetchone()
    if result:
        return HttpResponse("false")
    else:
        return HttpResponse("true")
def sajax(request):
    cursor = db.cursor()
    snuion = request.GET.get("snuion")
    sql = "select * from stu where snuion=%s"
    cursor.execute(sql,[snuion])
    result=cursor.fetchone()
    if result:
        return HttpResponse("false")
    else:
        return HttpResponse("true")