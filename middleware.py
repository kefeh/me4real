from werkzeug.wrappers import Request, Response

class Middleware():
    """ this class is to ensure that we are properly handling every request made to our app """

    def __init__(self, app, w_app):
        self.app = w_app
        self.my_app = app

    def __call__(self, environ, start_response):
        request = Request(environ)

        print('thhis is for the request')
        print(request.path)
        print(request.method)

        for rule in self.my_app.url_map.iter_rules():
            print(rule)
            print(rule.methods)
            if str(rule) == str(request.path) and request.method in rule.methods:
                return self.app(environ, start_response)

        res = Response(u'Bad Request', mimetype='text/plain', status=400)
        return res(environ, start_response)