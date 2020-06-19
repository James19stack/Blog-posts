import secrets
import os
from flask import render_template,redirect,url_for,flash,request,abort
from . import main
from .forms import UploadBlog,Comments,UpdateSettings
from ..models import User,Blogs,Comment
from ..request import get_quote
from PIL import Image

@main.route('/')
def index():
    quotes=get_quote()
    page=request.args.get('page',1,type=int)
    blogs=Blogs.query.order_by(Blogs.posted_date.desc()).paginate(page=page,per_page=10)
    return render_template('index.html',blogs=blogs ,page='index',quotes=quotes,title='Blog | Arena')

@main.route('/new/blog', methods=['GET','POST'])
@login_required
def uplaod_blog():
    form=UploadBlog()
    if form.validate_on_submit():
        blog=Blogs(category=form.category.data,blog=form.blog.data,user=current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Blog Posted!')
        return redirect(url_for('main.index'))

    return render_template('new_blog.html',form=form,title='New Blog' ,legend='Upload Blog',page='upload')

@main.route('/<int:blog_id>/comment', methods=['GET','POST'])
@login_required
def comment(blog_id):
    form_comment=Comments()
    image=url_for('static',filename='profile/'+current_user.profile_pic_path)
    blog=Blogs.query.filter_by(id=blog_id).first()
    comment_query=Comment.query.filter_by(blog_id=blog.id).all()
    if form_comment.validate_on_submit():
        comment=Comment(comment=form_comment.comment.data,blog_id=blog.id,user_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('main.comment',blog_id=blog.id))
    print(image)
    return render_template('blog.html',form=form_comment,blog=blog,comments=comment_query,image=image,title='Comments')

@main.route('/user/<string:user>' ,methods=['GET','POST'])
@login_required
def profile(user):
    image=url_for('static',filename='profile/'+current_user.profile_pic_path)
    user=User.query.filter_by(username=user).first_or_404()
    page=request.args.get('page',1,type=int)
    blogs=Blogs.query.filter_by(user=user)\
        .order_by(Blogs.posted_date.desc())\
        .paginate(page=page,per_page=10)
    return render_template('user_profile.html',page='profile',image=image,user=user,blogs=blogs)

#BLOGGER DETAILS
@main.route('/blogger/<string:user>' ,methods=['GET','POST'])
@login_required
def blogger_profile(user):
    user=User.query.filter_by(username=user).first_or_404()
    image=url_for('static',filename='profile/'+ user.profile_pic_path)
    page=request.args.get('page',1,type=int)
    blogs=Blogs.query.filter_by(user=user)\
        .order_by(Blogs.posted_date.desc())\
        .paginate(page=page,per_page=10)
    return render_template('blogger_profile.html',page='profile',image=image,user=user,blogs=blogs,title=user.username)




@main.route('/update/blog/<int:blog_id>', methods=['GET','POST'])
@login_required
def update_blog(blog_id):
    update=UploadBlog()
    blog=Blogs.query.filter_by(id=blog_id).first_or_404()
    if blog.user !=current_user:
        abort(403)

    if update.validate_on_submit():
        blog.category=update.category.data
        blog.blog=update.blog.data
        db.session.commit()
        return redirect(url_for('main.profile',user=blog.user.username))
        flash('Blog updated!')

    elif request.method=='GET':
        update.category.data=blog.category
        update.blog.data=blog.blog
        
    return render_template('update_blog.html',update=update,legend='Update Blog',title='Update Blog')

@main.route('/delete/blog/<int:blog_id>', methods=['POST'])
@login_required
def delete_blog(blog_id):
    blog=Blogs.query.filter_by(id=blog_id).first_or_404()
    if blog.user !=current_user:
        abort(403)

    db.session.delete(blog)
    db.session.commit()
    flash('Blog deleted!')
    return redirect(url_for('main.profile',user=blog.user.username))


def save_picture(data):
    random_hex=secrets.token_hex(7)
    f_name,f_extention=os.path.splitext(data.filename)
    picture_filename=random_hex+f_extention
    pic_path=os.path.join('/home/dynamo/Desktop/projects/PYTHON PROJECTS/blog/app/static/profile/'+ picture_filename)
    print(pic_path)
    image_size=(500,500)
    image=Image.open(data)
    image.thumbnail(image_size)
    image.save(pic_path)

    return picture_filename


@main.route('/update/<string:user>', methods=['GET','POST'])
@login_required
def update_settings(user):
    update_form=UpdateSettings()
    user=User.query.filter_by(username=user).first_or_404()
    if user.username !=current_user.username:
        abort(403)

    if update_form.validate_on_submit():
        if update_form.picture.data:
            profile_pic=save_picture(update_form.picture.data)
            user.profile_pic_path=profile_pic

        user.email=update_form.email.data
        user.username=update_form.username.data
        user.bio=update_form.bio.data
        db.session.commit()
        return redirect(url_for('main.profile',user=user.username))

    elif request.method=='GET':
        update_form.username.data=user.username
        update_form.email.data=user.email
        update_form.bio.data=user.bio

    return render_template('setting_update.html', update=update_form,title='Settings Update')
    
@main.route('/delete/comment/<int:comment_id>', methods=['GET','POST'])
@login_required
def delete_comment(comment_id):
    comment=Comment.query.filter_by(id=comment_id).first_or_404()
    blog=Blogs.query.filter_by(id=comment.blogs.id).first()
    if blog.user !=current_user:
        abort(403)

    db.session.delete(comment)
    db.session.commit()
    flash('Blog deleted!')
    return redirect(url_for('main.comment',blog_id=blog.id))


