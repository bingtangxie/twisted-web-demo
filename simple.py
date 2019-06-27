# from twisted.web import server, resource
# from twisted.internet import reactor, endpoints
#
#
# # class Simple(resource.Resource):
# #     isLeaf = True
# #
# #     def render_GET(self, request):
# #         return b"<html>Hello, world!</html>"
#
# class Hello(resource.Resource):
#     isLeaf = True
#
#     def getChild(self, name, request):
#         print(name)
#         if name == '':
#             return self
#         return resource.Resource.getChild(self, name, request)
#
#     def render_GET(self, request):
#         return b"Hello, world! I am located at %r." % (request.prepath,)
#
# # site = server.Site(Simple())
# root = Hello()
# root.putChild(b'fred', root)
# root.putChild(b'bob', root)
# site = server.Site(root)
# endpoint = endpoints.TCP4ServerEndpoint(reactor, 8080)
# endpoint.listen(site)
# reactor.run()

from twisted.internet import reactor
from twisted.web.resource import Resource, NoResource
from twisted.web.server import Site

from calendar import calendar


class YearPage(Resource):
    isLeaf = True  # 只要有数字就行，也就是最后一个了

    def __init__(self, year):
        super(YearPage, self).__init__()
        self.year = year

    def render_GET(self,request):
        data="<html><body><pre>%s</pre></body></html>"%calendar(self.year)
        return data.encode('ascii')


class CalendarHome(Resource):
    # isLeaf = True 有isLeaf，getChild就永远不会调用
    # 如果我们希望这个类既有分支又有方法，必须重写getChild

    def getChild(self, name, request):
        name = name.decode('ascii')

        if name == "":
            return self
        if name.isdigit():
            return YearPage(int(name))
        else:
            return NoResource()

    def render_GET(self,request):
        data="<h1>welcome</h1>"
        return data.encode('ascii')


root = CalendarHome()
factory = Site(root)
reactor.listenTCP(8005, factory)
reactor.run()
