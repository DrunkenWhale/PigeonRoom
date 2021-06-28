import os


# import random
# from markdown import markdown
# linux 特供版 sqlite3没有-md的导出指令 我真是吐了 直接导出html不就好了..
# 好吧不是没有 是redhat系列更新慢的离谱 用的居然是13年的sqlite

class markdown_sqlite(object):
    def __init__(self, path, database, order="SELECT * FROM MESSAGE"):
        self.content = None
        self.head = None
        self.body = None
        self.path = path
        self.head = "<thead>"
        self.database = database
        self.temp_file = "ababababababababababab"
        self.order = order
        self.check()
        self.derive()
        self.read_file()
        self.to_md()

    def check(self):  # check the file exist .if the file is exist pass,unless raise EOFError
        if os.path.exists(path=self.path + os.sep + self.database):
            pass
        else:
            raise EOFError

    def derive(self):
        os.system("sqlite3 -html " + self.database + ' "' + self.order + '" > ' + self.temp_file + ".html")

    def read_file(self):
        with open(self.temp_file + ".html", 'r', encoding='utf-8') as file:
            self.body = file.read()

    def to_md(self):
        # self.content = markdown(self.body, output_format='html', extensions=['tables'])
        if self.order.replace('from', "~").split("~")[0].split()[-1] == "*":
            schema = self.order.split("from")[-1].strip().split()[0]
            os.system("sqlite3 " + self.database + " .schema > temp.txt")
            with open('temp.txt', 'r') as f:
                body = f.read()
            temp = body.split('CREATE ')
            for i in temp:
                if (schema + " (\n") in i:
                    body = i.split("\n")[1:-2]
                    break
            for i in body:
                if i.split()[0] == "PRIMARY" or i.split()[0] == "FOREIGN":
                    break
                self.head += "<th>" + i.split()[0] + "</th>"
            self.head += "</thead>"
            os.remove(self.path + os.sep + "temp.txt")
        else:
            string = self.order.replace('from', "~").split("~")[0].split()[-1]
            for i in string.split(","):
                self.head += "<th>"+i+"</th>"
            self.head += "</thead>"
        self.content = "<table>" + self.head + "<tbody>" + self.body + "</tbody></table>"
        os.remove(self.path + os.sep + self.temp_file + ".html")
