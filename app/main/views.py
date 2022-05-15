from . import main
from flask import render_template, redirect, url_for, abort, flash, request
from .. import db
from ..models import Role, User, Post,Category, Comment
from ..request import get_quotes
from flask_login import login_required, current_user
from .forms import ProfileForm, CategoryForm, CommentForm,PasswordForm


#index page
@main.route('/')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    categories = Category.query.all()
    quote = get_quotes()
    latest_posts = Post.query.order_by(Post.created_at.desc()).limit(2)
    return render_template('index.html', posts=posts, categories=categories, quote=quote, latest_posts=latest_posts)


#profile page
@main.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username):
    # get user posts
    user = User.query.filter_by(username=username).first()
    posts = Post.get_user_posts(
        user.id).order_by(Post.created_at.desc()).all()

    # get comments created by other users
    comments = Comment.get_my_posts_comments(user.id)
    if user is None:
        abort(404)

    # get all categories
    categories = Category.query.all()

    # update profile form
    form = ProfileForm()
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.name = form.name.data
        user.email = form.email.data
        user.username = form.username.data
        db.session.commit()

        flash('Profile updated.', category='success')
        return redirect(url_for('main.profile', username=user.username))
    form.name.data = user.name
    form.email.data = user.email
    form.username.data = user.username
    form.bio.data = user.bio

    #updatepassword
    password_form = PasswordForm()
    if password_form.validate_on_submit():
        if current_user.verify_password(password_form.old_password.data):
            current_user.password = password_form.password.data
            db.session.commit()
            flash('Password updated.', category='success')
            return redirect(url_for('main.profile', username=user.username))
        else:
            flash('Invalid password', category='error')
    title = 'Account Profile'

    #category form
    category_form = CategoryForm()
    if category_form.validate_on_submit():
        category = Category(name=category_form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('New category added successfully', category='success')
        return redirect(url_for('main.profile', username=user.username))
    return render_template("profile/profile.html",title=title,user=user,form=form,categories=categories,posts=posts,comments=comments,password_form=password_form,category_form=category_form)


#blogpost
@main.route('/post/<int:id>', methods=['GET', 'POST'])
def single_post(id):
    post = Post.get_post(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(user_id=current_user.id,post_owner_id=post.user_id,content=form.content.data,post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', category='success')
        return redirect(url_for('.single_post', id=post.id))
    # get comments
    comments = Comment.get_comments_by_post(post.id)
    return render_template('single_post.html', post=post,form=form,comments=comments)


#update blogpost
@main.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.get_post(id)
    title = request.args.get('title')
    category_id = request.args.get('category_id')
    content = request.args.get('content')
    user_id = request.args.get('user_id')
    # update post
    post.title = title
    post.content = content
    post.category_id = category_id
    post.user_id = user_id
    db.session.commit()
    return redirect(url_for('main.profile', username=current_user.username))

#create new blogpost
@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    title = request.args.get('title')
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')
    content = request.args.get('content')
    post = Post(title=title,user_id=user_id,category_id=category_id,content=content)
    db.session.add(post)
    db.session.commit()
    flash('New post created successfully.', category='success')
    return redirect(url_for('main.profile', username=current_user.username))


#search blogpost
@main.route('/search', methods=['GET', 'POST'])
def search():
    query = request.args.get('query')
    posts = Post.get_posts_by_query(query)
    return render_template('search.html', posts=posts, query=query)


#delete blogpost
main.route('/post/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(id):
    post = Post.get_post(id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', category='success')
    return redirect(url_for('main.profile', username=current_user.username))


#get post by category
@main.route('/category/<int:id>')
def filter_posts(id):
    category = Category.query.filter_by(id=id).first()
    posts = Post.get_post_by_category(category.id)
    return render_template('posts.html', posts=posts, category=category)


#delete comments
@main.route('/comment/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete_comment(id):
    comment = Comment.get_comment(id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', category='success')
    return redirect(url_for('main.profile', username=current_user.username))


#uploading profile image
@main.route('/profile/<username>/update/pic', methods=['POST'])
@login_required
def update_pic(username):
    user = User.query.filter_by(username=username).first()
    if 'photo' in request.files:
        image_url = upload(request.files['photo'])['url']
        user.profile_pic_path = image_url
        db.session.commit()
        flash('Image upload successful', category='success')
        return redirect(url_for('main.profile', username=username))
    else:
        flash('Image upload not successful', category='error')
        return redirect(url_for('main.profile', username=username))


#update blogpost image
@main.route('/post/<int:id>/update/image', methods=['GET', 'POST'])
@login_required
def update_post_image(id):
    post = Post.query.filter_by(id=id).first()
    if 'photo' in request.files:
        image_url = upload(request.files['photo'])['url']
        post.image_path = image_url
        db.session.commit()
        flash('Blogpost image uploaded', category='success')
        return redirect(url_for('main.profile', username=current_user.username))
