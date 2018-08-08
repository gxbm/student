from django.views import View
from django.shortcuts import HttpResponse,redirect,render
from .sqlfenzhung import sql
class shiti(View):
    def get(self,req):
        db=sql()
        date = db.select(
            "select shiti.id,shiti.shitiid,shiti.tigan,shiti.opt,shiti.answer,grade.gname,stage.staname,types.tyname from shiti left join stage on shiti.staid=stage.staid left join types on shiti.tyid=types.tyid left join grade on shiti.gid=grade.gid")
        result = db.select("select * from grade")
        tixingres = db.select("select * from types")
        return render(req, "shiti.html", {"date": date, "result": result, "tixingres": tixingres})
    def post(self,req):
        pass
class shitiadd(View):
    def get(self,req):
        db = sql()
        date = db.select(
            "select shiti.id,shiti.shitiid,shiti.tigan,shiti.opt,shiti.answer,grade.gname,stage.staname,types.tyname from shiti left join stage on shiti.staid=stage.staid left join types on shiti.tyid=types.tyid left join grade on shiti.gid=grade.gid")
        result = db.select("select * from grade")
        tixingres = db.select("select * from types")
        return render(req, "shitiadd.html", {"date": date, "result": result, "tixingres": tixingres})
    def post(self,req):
        shitiid=req.POST.get("shitiid")
        gid=req.POST.get("gid")
        staid=req.POST.get("staid")
        tyid=req.POST.get("tyid")
        tigan=req.POST.get("tigan")
        answer=req.POST.get("answer")
        opt=req.POST.get("option")
        db=sql()
        db.exec("insert into shiti (shitiid,gid,staid,tyid,tigan,opt,answer) values (%s,%s,%s,%s,%s,%s,%s)",[shitiid,gid,staid,tyid,tigan,opt,answer])
        db.close()
        return redirect("/shiti/")
class shitisearch(View):
    def get(self,req):
        gid=req.GET.get("gid")
        staid=req.GET.get("staid")
        tyid=req.GET.get("tyid")
        con=req.GET.get("con")
        print(gid,staid,tyid,con)
        db=sql()
        contion=''' where 1=1 '''
        contion+=''' and shiti.gid='%s' '''%(gid) if gid else ""
        contion +=''' and shiti.staid= '%s' '''%(staid) if staid else ""
        contion += ''' and shiti.tyid='%s' '''%(tyid) if tyid else ""

        contion += '''and shiti.tigan like "%%{0}%%" '''.format(con) if con else ""

        result1=db.select("select shiti.id,shiti.shitiid,shiti.tigan,shiti.opt,shiti.answer,grade.gname,stage.staname,types.tyname from shiti left join stage on shiti.staid=stage.staid left join types on shiti.tyid=types.tyid left join grade on shiti.gid=grade.gid "+contion )
        result = db.select("select * from grade")
        tixingres = db.select("select * from types")
        return render(req, "shiti.html", {"date": result1,"result":result,"tixingres":tixingres})
