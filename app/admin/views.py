from flask.ext.admin import Admin, BaseView, expose

class IndexView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/index.jinja')
