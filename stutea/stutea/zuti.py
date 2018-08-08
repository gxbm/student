from django.views import View
from django.shortcuts import HttpResponse,redirect,render
from .sqlfenzhung import sql
from django import forms
import xlrd
from .fenye import pages
import math
import json
class mycheck(forms.Form):
    # name=forms.CharField(error_messages={"required":"此项必填"})
    file=forms.FileField(error_messages={"required":'上传文件'})
class zuti(View):
    def get(self,req):
        return render(req, "zuti.html")
class zutiadd(View):
    def get(self,req):
        curr_page = req.GET.get("page") if req.GET.get("page") else 0
        num = 4
        curr_page = int(curr_page)
        db = sql()
        date = db.select(
            "select shiti.id,shiti.shitiid,shiti.tigan,shiti.opt,shiti.answer,grade.gname,stage.staname,types.tyname,types.tyid from shiti left join stage on shiti.staid=stage.staid left join types on shiti.tyid=types.tyid left join grade on shiti.gid=grade.gid limit %s,%s",[curr_page*num,num])
        result=db.select("select * from grade")
        tixingres=db.select("select * from types")
        count = db.select("select count(*) from shiti left join stage on shiti.staid=stage.staid left join types on shiti.tyid=types.tyid left join grade on shiti.gid=grade.gid")
        total = math.ceil(count[0]['count(*)'] / num)
        print(count,total,curr_page)
        page=pages()
        str=page.fenye(total, curr_page,"/zutiadd/")
        return render(req,"zutiadd.html",{"date":date,"result":result,"tixingres":tixingres,"str":str})
class zutisearch(View):
    def get(self,req):
        curr_page = req.GET.get("page") if req.GET.get("page") else 0
        num = 4
        curr_page = int(curr_page)
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
        contion+= '''limit %s,%s'''%(curr_page*num,num)

        result1=db.select("select shiti.id,shiti.shitiid,shiti.tigan,shiti.opt,shiti.answer,grade.gname,stage.staname,types.tyname from shiti left join stage on shiti.staid=stage.staid left join types on shiti.tyid=types.tyid left join grade on shiti.gid=grade.gid "+contion)
        result = db.select("select * from grade")
        tixingres = db.select("select * from types")

        count = db.select("select count(*) from shiti left join stage on shiti.staid=stage.staid left join types on shiti.tyid=types.tyid left join grade on shiti.gid=grade.gid "+contion)
        total = math.ceil(count[0]['count(*)'] / num)
        print(count, total, curr_page)
        page = pages()
        print(result1)
        return render(req, "zutiadd.html", {"date": result1,"result":result,"tixingres":tixingres,"str":page.fenye(total, curr_page, "/zutisearch/"),"gid":gid,"pid":staid,"tyid":tyid})
class fileload(View):
    def get(self,req):
        db=sql()
        result = db.select("select * from grade")
        db.close()
        return render(req,"fileload.html",{"date":result})
    def post(self,req):
        obj=mycheck(req.POST,req.FILES)
        gid=req.POST.get("gid")
        staid=req.POST.get("staid")
        if  obj.is_valid():
            file = req.FILES["file"]
            sheet=xlrd.open_workbook(filename=None,file_contents=file.read())
            date=sheet.sheet_by_index(0)
            arrs=[]
            for item in range(1,date.nrows):
                arr=date.row_values(item)
                db=sql()
                arr[0]=db.one("select tyid from types where tyname=%s",[arr[0]])["tyid"]
                arr[2] = "|".join(arr[2].split("\n"))
                arr.insert(0, gid)
                arr.insert(1, staid)
                arrs.append(arr)
            db.exec_many("insert ignore into shiti (gid,staid,tyid,tigan,opt,answer) values (%s,%s,%s,%s,%s,%s)",arrs)
            db.close()
        else:
            abc = obj.errors
            return render(req, "fileload.html", {"file": abc})







