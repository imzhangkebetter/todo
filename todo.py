# -*- coding: utf-8 -*-
import web, json, os
render = web.template.render("templates")
from web.template import ALLOWED_AST_NODES
ALLOWED_AST_NODES.append('Constant')
from web.contrib.template import render_jinja

app_root = os.path.dirname(__file__)
templates_path = os.path.join(app_root, 'templates').replace('\\', '/')

render = render_jinja(
    templates_path,          # 设置模板路径
    encoding='utf-8',     # 编码
)

db = web.database(dbn='mysql', user='root', pw='12345678', db='todo', port=3388, buffered=True)

urls = (
    '/', 'index',
    '/addz', 'addz',
    '/addx/(\d+)', 'addx',
    '/list/(\d+)', 'list',
    '/delete/(\d+)', 'delete'
)


class index:
    def GET(self):
        zhuti = db.select("zhuti", order="id")
        return render.index(zhuti=zhuti)


class addz:
    def GET(self):
        zhuti = db.select("zhuti", order="id")
        return render.addz(zhuti=zhuti)

    def POST(self):
        i = web.input()
        db.insert('zhuti', name=i.name)
        return web.seeother('addz')


class addx:
    def GET(self, id):
        return render.addx(id=id)

    def POST(self, id):
        zid = id
        print(zid)
        data = web.data()
        json_data = json.loads(data)
        for da in json_data['data']:
            db.insert('xuanxiang', name=da['value'], x_id=zid)


class list:
    def GET(self, xid):
        title = db.select('zhuti', where="id="+xid)
        toupiao = db.select('xuanxiang', where="x_id="+xid)
        return render.list(title=title, toupiao=toupiao)

    def POST(self, xid):
        data = json.loads(web.data())
        myvars = dict(id=data['id'], x_id=data['xid'])
        num = db.select('xuanxiang', vars=myvars, where='id=$id and x_id=$x_id', what='num')
        number = num[0]['num']+1
        db.update('xuanxiang', vars=myvars, where='id=$id and x_id=$x_id', num=number)


class delete:
    def POST(self, id):
        id = id
        db.delete('zhuti', where='id=$id', vars=locals())


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
