from flask import render_template, redirect, url_for, flash, request
from app.posts import bp
from app import db
from app.models import Post
from app.forms import PostForm
import sqlalchemy as sa

@bp.route('/')
def posts():
    query = db.select(Post).order_by(Post.posted.desc())
    all_posts = db.session.execute(query).scalars().all()
    return render_template('posts/posts.html', posts=all_posts)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            author=form.author.data
        )
        db.session.add(new_post)
        db.session.commit()
        flash('Пост успішно створено!', 'success')
        return redirect(url_for('posts.posts'))
    return render_template('posts/create.html', form=form, title="Новий пост")

@bp.route('/<int:id>')
def post_detail(id):
    post = db.session.get(Post, id)
    if post is None:
        flash('Пост не знайдено.', 'danger')
        return redirect(url_for('posts.posts'))
    return render_template('posts/post_detail.html', post=post)

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    post = db.session.get(Post, id)
    if post is None:
        flash('Пост не знайдено.', 'danger')
        return redirect(url_for('posts.posts'))

    form = PostForm(obj=post) 
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.author = form.author.data
        db.session.commit()
        flash('Пост успішно оновлено!', 'success')
        return redirect(url_for('posts.post_detail', id=post.id))

    return render_template('posts/create.html', form=form, title="Редагувати пост")

@bp.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    post = db.session.get(Post, id)
    if post is None:
        flash('Пост не знайдено.', 'danger')
        return redirect(url_for('posts.posts'))
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Пост видалено.', 'success')
    return redirect(url_for('posts.posts'))

@bp.route('/<int:id>/delete_confirm')
def delete_confirm(id):
    post = db.session.get(Post, id)
    if post is None:
        flash('Пост не знайдено.', 'danger')
        return redirect(url_for('posts.posts'))
    return render_template('posts/delete.html', post=post)