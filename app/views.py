from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from app.model import db, User, ArticleType, Atricle
from utils.functions import is_login

back_blue = Blueprint('back', __name__)
 # 文章
@back_blue.route('/article/', methods=['GET','POST'])
@is_login
def article():
    if request.method == 'GET':
        articles = Atricle.query.order_by(Atricle.id).all()
        return render_template('back/article.html',articles=articles)
# 添加文章
@back_blue.route('/add_article/', methods=['GET', 'POST'])
@is_login
def add_article():
    if request.method == 'GET':
        articles = []
        types = ArticleType.query.order_by(ArticleType.id).all()
        return render_template('back/add_article.html', types=types,articles=articles)
    if request.method == 'POST':
        title = request.form.get('title')
        describe = request.form.get('describe')
        content = request.form.get('content')
        category = request.form.get('category')
        if content:
           # 保存
            art = Atricle()
            art.title = title
            art.content = content
            art.type = category
            art.describ = describe
            db.session.add(art)
            db.session.commit()
            return redirect(url_for('back.article'))
        else:
            error='请不要给我一篇没有内容的文章'
            return render_template('back/add_article.html',error=error)
# 删除文章
@back_blue.route('/del_article/<int:id>/', methods=['GET'])
def del_article(id):
    if request.method == 'GET':
        articles = Atricle.query.get(id)
        db.session.delete(articles)
        db.session.commit()
        return redirect(url_for('back.article'))
# 修改文章
@back_blue.route('/update_article/<int:id>', methods=['GET', 'POST'])
def update_article(id):
    if request.method == 'GET':
        types = ArticleType.query.order_by(ArticleType.id).all()
        articles = Atricle.query.get(id)
        return render_template('back/add_article.html', articles=articles,types=types)
    if request.method == 'POST':
        articles = Atricle.query.get(id)
        if articles.content:
           # 保存
            articles.title = request.form.get('title')
            articles.describ = request.form.get('describe')
            articles.content = request.form.get('content')
            articles.type = request.form.get('category')
            db.session.add(articles)
            db.session.commit()
            return redirect(url_for('back.article'))
        else:
            error='请不要给我一篇没有内容的文章'
            return render_template('back/add_article.html',error=error)
 # 报告
@back_blue.route('/index/')
@is_login
def index():
    return render_template('back/index.html')
# 登录
@back_blue.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('back/login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd')
        user = User.query.filter(User.name == username).first()
        if not user:
            error = 'not exist' # 该账号不存在
            return render_template('back/login.html', error=error)
        if not check_password_hash(user.password,password):
            error = 'mistake password' # 密码错误
            render_template('back/login.html', error=error)
        # 匹配成功，登录状态，跳转到首页
        session['user_id'] = user.id
        return redirect(url_for('back.index'))
# 栏目
@back_blue.route('/category/', methods=['GET','POST'])
@is_login
def category():
    if request.method == 'GET':
        alltype = []
        types = ArticleType.query.order_by(ArticleType.id).all()
        return render_template('back/category.html',types= types,alltype=alltype)
    if request.method == 'POST':
        # 判定条目是否存在,计数(？！)
        # 保存分类数据
        atype = request.form.get('atype')
        stype = request.form.get('fid')
        name = ArticleType.query.filter(ArticleType.t_name == atype).first()
        if name:
            error='该栏目已存在'
            return render_template('back/category.html', error=error)
        else:
            type_name = ArticleType()
            type_name.t_name = atype
            type_name.a_name = stype
            db.session.add(type_name)
            db.session.commit()
            return redirect(url_for('back.category'))
# 删除分类
@back_blue.route('/del_type/<int:id>/', methods=['GET'])
def del_type(id):

    atype = ArticleType.query.get(id)
    db.session.delete(atype)
    db.session.commit()
    return redirect(url_for('back.category'))
# # 修改栏目
# @back_blue.route('/update_type/<int:id>/',methods=['GET','POST'])
# def update_type(id):
#     if request.method == 'GET':
#         alltype = ArticleType.query.get(id)
#         return render_template('back/category.html', alltype=alltype)
#     if request.method == 'POST':
#
#         atype = request.form.get('atype')
#         stype = request.form.get('fid')
#         name = ArticleType.query.filter(ArticleType.t_name == atype).first()
#         if name:
#             error = '该栏目已存在'
#             return render_template('back/category.html', error=error)
#         else:
#             type_name = ArticleType()
#             type_name.t_name = atype
#             type_name.a_name = stype
#             db.session.add(type_name)
#             db.session.commit()
#             return redirect(url_for('back.category'))
 # 注册
@back_blue.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('back/register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userpwd')
        password2 = request.form.get('userpwd2')
          # 判断该用户名是否被注册过
        user = User.query.filter(User.name == username).first()
        if user:
            error = '该用户名已被注册'    
            return render_template('back/register.html', error=error)
        else:
            if password2 == password:
                # 保存数据
                user = User()
                user.name = username
                user.password = generate_password_hash(password)
                user.save_update()
                return redirect(url_for('back.login'))
            else:
                error = '两次密码不一致' #
                return render_template('back/register.html', error=error)
# 注销登录
@back_blue.route('/logout/', methods=['GET'])
# 判定账户是否登录
@is_login
def logout():
    del session['user_id']
    return redirect(url_for('back.login'))
            