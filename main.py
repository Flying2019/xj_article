from flask import Flask,render_template,request,redirect,send_from_directory,abort
from flask_bootstrap import Bootstrap
from file import read,write
from forms import AddNormal,AddType,GetRequire,AddQry

app=Flask(__name__)
bootstrap=Bootstrap(app)

import random

app.secret_key = '112233'

def add_to_dic(s):
    print('add',s)
    for v in s['type']:
        if v in dic:
            dic[v].append(s)
        else:
            dic[v]=[s]

def remove_from_dic(id):
    w=texts[id]
    rec.append(w)
    print('remove',w)
    for v in w['type']:
        for i in range(len(dic[v])):
            if dic[v][i]==w:
                dic[v].pop(i)
                break

def Write():
    write(types,texts,tags,qrys,ip_whitelist,rec)

types,texts,tags,qrys,ip_whitelist,rec=read()
inputs={}
dic,have,const={},[],{}
tag1,tag2=[],[]
for s in texts:
    add_to_dic(s)

def same(x,y):
    s,t=[],1
    for i in x:
        s.append(i)
    for i in y:
        if i in s:
            t*=10
    return t

def get_choice(s,ex):
    tag=[]
    if ex=='all':
        tag=tag1+tag2
    if ex=='tag1':
        tag=tag1
    if ex=='tag2':
        tag=tag2
    if ex=='const':
        if s in const:
            return const[s]
    for u,v in types:
        if u==s:
            if v==0:
                for x in range(5):
                    t=random.choice(dic[s])['text']
                    if not t in have:
                        have.append(t)
                        if ex=='const':
                            const[s]=t
                        return t
            else:
                al=0
                for t in dic[s]:
                    if not t['text'] in have:
                        al+=same(tag,t['tag'])
                        # print(same(tag,t['tag']),end=' ')
                # print()
                c=random.randint(1,al)
                for t in dic[s]:
                    if not t['text'] in have:
                        c-=same(tag,t['tag'])
                        if c<=0:
                            have.append(t['text'])
                            return t['text']
                return '[Error %s]'%s
    return '[Error %s]'%s

def get_article(s):
    # print(s,have)
    s=s.strip()
    text=''
    for t in s.split('['):
        if t.find(']')!=-1:
            r,t=t.split(']')
            ex=''
            r=r.strip()
            if r.find('|')!=-1:
                r,ex=r.split('|')
            if r in inputs:
                text+=inputs[r]
            elif r in dic and len(dic[r])!=0:
                text+=get_article(get_choice(r,ex))
        text+=t
    return text

@app.route('/',methods=['GET','POST'])
def main():
    global tag1,tag2,inputs,have,const
    form=GetRequire()
    form.标签1.choices=[(v,tags[v]) for v in range(len(tags))]
    form.标签2.choices=[(v,tags[v]) for v in range(len(tags))]
    if form.validate_on_submit():
        inputs['对立关键词1']=form.data['对立关键词1']
        inputs['对立关键词2']=form.data['对立关键词2']
        inputs['定义关键词1']=form.data['定义关键词1']
        inputs['定义关键词2']=form.data['定义关键词2']
        if inputs['定义关键词1']=='':
            inputs['定义关键词1']=inputs['对立关键词1']
        if inputs['定义关键词2']=='':
            inputs['定义关键词2']=inputs['对立关键词2']
        tag1=[tags[v] for v in form.data['标签1']]
        tag2=[tags[v] for v in form.data['标签2']]
        print(tag1,tag2)
        have,const=[],{}
        res=get_article('[base]').split('$')
        return render_template('show.html',res=res,head=f'%s'%get_article('[标题|const]'))
    return render_template('main.html',form=form)

@app.route('/upd',methods=['GET','POST'])
def upd():
    id=int(request.args.get('id','-1'))
    form=AddNormal()
    form.type.choices=[(v,types[v][0]) for v in range(len(types))]
    form.tag.choices=[(v,tags[v]) for v in range(len(tags))]
    if form.validate_on_submit():
        a={'text':form.data['text'],'tag':[tags[v] for v in form.data['tag']],'type':[types[v][0] for v in form.data['type']]}
        # print(a)
        if id != -1:
            remove_from_dic(id)
            texts[id]=a
            add_to_dic(a)
        else:
            texts.append(a)
            add_to_dic(a)
        Write()
        return redirect('/upd')
    if id != -1:
        form.type.data,form.text.data,form.tag.data=[],"",[]
        for v in range(len(types)):
            if types[v][0] in texts[id]['type']:
                form.type.data.append(v)
        form.text.data=texts[id]['text']
        for v in range(len(tags)):
            if tags[v] in texts[id]['tag']:
                form.tag.data.append(v)
        # print(form.type.data,form.text.data,form.tag.data)
    return render_template('upd.html',texts=texts,form=form)

@app.route('/backup',methods=['GET'])
def backup():
    return send_from_directory('','data')

@app.route('/backup/log',methods=['GET'])
def backup_log():
    return send_from_directory('','log.txt')

@app.route('/erase',methods=['GET'])
def erase():
    id=int(request.args.get('id'))
    if id<0 or id>len(texts):
        return redirect('/upd')
    remove_from_dic(id)
    texts.pop(id)
    Write()
    return redirect('/upd')

@app.route('/tag/erasetag',methods=['GET'])
def erasetag():
    id=int(request.args.get('id'))
    tags.pop(id)
    Write()
    return redirect('/tag')

@app.route('/tag/erasetype',methods=['GET'])
def erasetype():
    id=int(request.args.get('id'))
    types.pop(id)
    Write()
    return redirect('/tag')

@app.route('/tag',methods=['GET','POST'])
def gettag():
    form=AddType()
    if form.validate_on_submit():
        print(form.data)
        if form.data['type']=='0':
            types.append([form.data['text'],0])
        if form.data['type']=='1':
            types.append([form.data['text'],1])
        if form.data['type']=='2':
            tags.append(form.data['text'])
        Write()
        return redirect('/tag')
    return render_template('tag.html',tags=tags,types=types,form=form)

@app.route('/about',methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/qry',methods=['GET','POST'])
def qry():
    form=AddQry()
    if form.validate_on_submit():
        print(form.data)
        ip=request.remote_addr.split('.')
        ip='%s.%s.%s.*'%(ip[0],ip[1],ip[2])
        qrys.append({'text':form.data['text'],'ip':ip,'now':'未读'})
        Write()
    return render_template('qry.html',qrys=qrys,form=form)

P=['未读','正在鸽子','已处理','']
@app.route('/change',methods=['GET'])
def change():
    global qrys
    id,op=int(request.args.get('id',0))-1,int(request.args.get('opt',3))
    if id != -1 and id < len(qrys):
        if op<0 or op>3:
            qrys.pop(id)
        else:
            qrys[id]['now'] = P[op]
        Write()
    return redirect('/qry')

@app.route('/recover',methods=['GET'])
def recover():
    id = int(request.args.get('id',-1))
    if id>=0 and id<len(rec):
        op = int(request.args.get('opt',-1))
        if op == 0:
            texts.append(rec[id])
            add_to_dic(rec[id])
        if op != -1:
            rec.pop(id)
        Write()
        return redirect('/recover')
    return render_template('recover.html',texts=rec)

PWD=''

@app.before_request
def before():
    url = request.path
    ip = request.remote_addr
    if url == '/':
        pass
    elif url == '/need':
        return render_template('need.html')
    elif ip in ip_whitelist:
        pass
    else:
        pwd = request.args.get('pwd','0')
        if pwd==PWD:
            ip_whitelist.append(ip)
            Write()
            return redirect('/')
        else:
            return render_template('need.html')

# @app.route('/reset',methods=['GET'])
# def reset():
#     global texts
#     for v in texts:
#         v['text']=v['text'].replace('[标题]','[标题|const]')
#     Write()
#     return redirect('/upd')

if __name__=='__main__':
    app.run('0.0.0.0')