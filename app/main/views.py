from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_user, current_user, logout_user, login_required
from . import main
from app.models import Post, User , Comment
from .forms import PostForm, UpdateProfile , UpdatePostForm ,CommentsForm
from ..import db, photos
from ..requests import get_quote

@main.route('/')
def index():
    quote=get_quote()
    posts= Post.query.all()
    return render_template('index.html',posts=posts,quote=quote)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route("/post/new", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data , user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('create_post.html',
                           create_post_form=form)

@main.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@main.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('main.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('update_post.html',
                           create_post_form=form)


@main.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.index'))


@main.route('/pitch/comments/new/<int:id>',methods = ['GET','POST'])
@login_required
def new_comment(id):
    form = CommentsForm()
    if form.validate_on_submit():
        new_comment = Comment(post_id =id,comment=form.comment.data,username=current_user.username)
        new_comment.save_comment()
        return redirect(url_for('main.view_comments' , id= id))
    return render_template('new_comment.html',comment_form=form,comments=comments)


@main.route('/delComment/<int:id>')
@login_required
def delComment(id):
  '''
  view function that deletes a comment if only the comment belongs to the current user
  '''
  
  comment=Comment.query.filter_by(id=id).first()

  comment.delete_comment()

  return redirect(url_for('main.comments',id=comment.post_id))

@main.route('/view/comments/<int:id>')
def view_comments(id):
    '''
    Function that returs  the comments belonging to a particular pitch
    '''
    comments = Comment.get_comments(id)
    return render_template('comments.html',comments = comments, id=id)
