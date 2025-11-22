from flask import render_template, redirect, url_for, flash, request
from app.posts import bp
from app import db
from app.models import Post
from app.forms import PostForm
import sqlalchemy as sa
from app.models import Post, Tag, User, Category

@bp.route('/')
def posts():
    query = db.select(Post).order_by(Post.posted.desc())
    all_posts = db.session.execute(query).scalars().all()
    return render_template('posts/posts.html', posts=all_posts)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    form = PostForm()
    
    form.tags.choices = [(t.id, t.name) for t in db.session.scalars(db.select(Tag))]
    
    form.category.choices = [(c.id, c.name) for c in db.session.scalars(db.select(Category))]

    if form.validate_on_submit():
        author_name = form.author.data
        user = db.session.scalar(db.select(User).where(User.username == author_name))
        
        if not user:
            flash(f'Користувача "{author_name}" не знайдено!', 'danger')
            return render_template('posts/create.html', form=form, title="Новий пост")

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            author=user,
            category_id=form.category.data
        )
        
        selected_tags = []
        for tag_id in form.tags.data:
            tag = db.session.get(Tag, tag_id)
            if tag:
                selected_tags.append(tag)
        new_post.tags = selected_tags
        
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
        return redirect(url_for('posts.posts'))
    
    form = PostForm()
    form.tags.choices = [(t.id, t.name) for t in db.session.scalars(db.select(Tag))]
    
    form.category.choices = [(c.id, c.name) for c in db.session.scalars(db.select(Category))]
    
    if form.validate_on_submit():
        user = db.session.scalar(db.select(User).where(User.username == form.author.data))
        if user:
            post.author = user
            
        post.title = form.title.data
        post.content = form.content.data
        post.category_id = form.category.data
        
        selected_tags = []
        for tag_id in form.tags.data:
            tag = db.session.get(Tag, tag_id)
            if tag:
                selected_tags.append(tag)
        post.tags = selected_tags
        
        db.session.commit()
        flash('Оновлено!', 'success')
        return redirect(url_for('posts.post_detail', id=post.id))
    
    if request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.author.data = post.author.username if post.author else ""
        form.tags.data = [t.id for t in post.tags]
        form.category.data = post.category_id

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