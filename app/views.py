from flask import Blueprint, redirect, url_for, request, render_template
from flask_admin import AdminIndexView, expose, BaseView
from flask_admin.contrib.mongoengine import ModelView
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from flask_login import current_user, login_user, logout_user
from app.forms import LoginForm
from app.models import Post

class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()

bp = Blueprint('blog', __name__)

@bp.route('/')
@bp.route('/<int:page>')
def index(page=1):
    paginator = Post.objects.paginate(page=page, per_page=5)
    return render_template("index.html", paginator=paginator)

@bp.route('/posts/<string:post_id>')
def get_post(post_id):
    post = Post.objects(id=post_id).first()
    return render_template("post.html", post=post)


class MyIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        #logout_user()
        print "entering index"
        if not current_user.is_authenticated:
            print "current user is not authenticated"
            return redirect(url_for('.login'))
        return super(MyIndexView, self).index()

    @expose('/login', methods=['GET', 'POST'])
    def login(self):
        form = LoginForm(request.form)
        if request.method == 'POST' and form.validate():
            user = form.get_user()
            login_user(user)
            print "login_user"
            redirect(url_for('.index'))

        self._template_args['form'] = form

        return super(MyIndexView, self).index()

    @expose('/logout')
    def logout_view(self):
        logout_user()
        return redirect(url_for('.index'))

class UserView(ModelView):
    def is_accessible(self):
        print "in UserView, current_user is", current_user
        return current_user.is_authenticated

class PostView(ModelView):
    column_display_pk = True
    form_overrides = dict(content=CKTextAreaField)
    create_template = 'admin/ckeditor.html'
    edit_template = 'admin/ckeditor.html'

    column_choices = {
            'status': [
                (0, 'draft'),
                (1, 'published')
            ]
    }

    column_filters = ('title', )
    column_searchable_list = ('content', )
    column_sortable_list = ('create_time', 'modify_time')

    def is_accessible(self):
        return current_user.is_authenticated
