import json
def read():
    types,texts,tags,qrys,whitelist,rec=[],[],[],[],[],[]
    try:
        with open('data','r',encoding='UTF-8') as f:
            a=json.loads(f.read())
            types,texts,tags,qrys,whitelist,rec=a['types'],a['texts'],a['tags'],a['qrys'],a['whitelist'],a['recover']
            f.close()
    except FileNotFoundError:
        with open('data','w',encoding='UTF-8') as f:
            f.write('\n\n')
            f.close()
    return (types,texts,tags,qrys,whitelist,rec)

def write(types,texts,tags,qrys,whitelist,rec):
    with open('data','w',encoding='UTF-8') as f:
        f.write(json.dumps({'types':types,'texts':texts,'tags':tags,'qrys':qrys,'whitelist':whitelist,'recover':rec}))
        f.close()
