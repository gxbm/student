from django.views import View
from django.shortcuts import HttpResponse,render,redirect
from .sqlfenzhung import sql
import json
class stage(View):
    def get(self,req):
        db=sql()
        result=db.select("select * from stage")
        db.close()
        return render(req,"stageInfo.html",{"date":result})
    def post(self,req):
        staid=req.POST.get("staid")
        db=sql()
        result=db.select("select tunion,tname from teacher where find_in_set(%s,staid)",[staid])
        return HttpResponse(json.dumps(result))
class stageadd(View):
    def get(self,req):
        return render(req,"stageadd.html")
    def post(self,req):
        staid=req.POST.get("staid")
        staname=req.POST.get("staname")
        db=sql()
        db.exec("insert into stage (staid,staname) values (%s,%s)",[staid,staname])
        db.close()
        return redirect("/stage/")
class stagedel(View):
    def get(self,req):
        staid=req.GET.get("id")
        db=sql()
        db.delete("delete from stage where staid=%s", [staid])
        date=db.select("select teacher.tunion,teacher.staid from teacher where find_in_set('%s',staid)"%(staid))
        arr=[]
        for item in date:
            arr=item["staid"].split(",")
            arr.remove(staid)
            arr=",".join(arr)
            db.update("update teacher set staid=%s where tunion=%s",[arr,item['tunion']])
        #年级表
        date1 = db.select("select gid,staid from grade where find_in_set('%s',staid)" % (staid))
        arr = []
        for item in date1:
            arr = item["staid"].split(",")
            arr.remove(staid)
            arr = ",".join(arr)
            db.update("update grade set staid=%s where gid=%s", [arr, item['gid']])
        db.delete("delete from classtea where staid=%s",[staid])
        db.close()
        return redirect("/stage/")
class stagedit(View):
    def get(self,req):
        staid=req.GET.get("id")
        db=sql()
        date=db.one("select * from stage where staid=%s",[staid])
        return render(req,"stagedit.html",{"date":date})
    def post(self,req):
        id = req.GET.get("id")
        staid=req.POST.get("staid")
        staname=req.POST.get("staname")
        print(id,staid,staname)
        db=sql()
        db.update("update stage set staid=%s,staname=%s where staid=%s",[staid,staname,id])
        date = db.select("select teacher.tunion,teacher.staid from teacher where find_in_set('%s',staid)" % (id))
        arr = []
        for item in date:
            arr = item["staid"].split(",")
            arr.remove(id)
            arr.append(staid)
            arr = ",".join(arr)
            db.update("update teacher set staid=%s where tunion=%s", [arr, item['tunion']])
        # 年级表
        date1 = db.select("select gid,staid from grade where find_in_set('%s',staid)" % (id))
        arr = []
        for item in date1:
            arr = item["staid"].split(",")
            arr.remove(id)
            arr.append(staid)
            arr = ",".join(arr)
            db.update("update grade set staid=%s where gid=%s", [arr, item['gid']])
        db.update("update classtea set staid=%s where staid=%s", [staid,id])
        db.close()
        return redirect("/stage/")
class stagetype(View):
    def get(self,req):
        gid=req.GET.get("gid")
        db=sql()
        date=db.select("select stage.staid,stage.staname from grade left join stage on find_in_set(stage.staid,grade.staid) where grade.gid=%s",[gid])
        print(date)
        db.close()
        return HttpResponse(json.dumps(date))
