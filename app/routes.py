from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Resource, Tag, Comment
from app.forms import ResourceForm

main = Blueprint('main', __name__)

@main.route("/")
def index():
    search_query = request.args.get('q')
    if search_query:
        resources = Resource.query.join(Resource.tags).filter(
            (Resource.title.contains(search_query)) |
            (Tag.name.contains(search_query))
        ).distinct().all()
    else:
        resources = Resource.query.all()
    return render_template('index.html', resources=resources)

@main.route("/create", methods=['GET', 'POST'])
@login_required
def create_resource():
    form = ResourceForm()
    if form.validate_on_submit():
        tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
        tags = []
        for name in tag_names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            tags.append(tag)
        
        resource = Resource(
            title=form.title.data,
            url=form.url.data,
            description=form.description.data,
            type=form.type.data,
            tags=tags,
            author=current_user
        )
        db.session.add(resource)
        db.session.commit()
        flash('Recurso criado com sucesso!', 'success')
        return redirect(url_for('main.index'))
    return render_template('create.html', title='Novo Recurso', form=form)

@main.route("/resource/<int:resource_id>", methods=['GET', 'POST'])
def resource_detail(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Faça login para comentar.', 'info')
            return redirect(url_for('auth.login'))
        
        content = request.form.get('content')
        if content:
            comment = Comment(content=content, author=current_user, resource=resource)
            db.session.add(comment)
            db.session.commit()
            flash('Comentário adicionado!', 'success')
            return redirect(url_for('main.resource_detail', resource_id=resource.id))
            
    return render_template('resource.html', title=resource.title, resource=resource)

@main.route("/resource/<int:resource_id>/like")
@login_required
def like_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    resource.likes += 1
    db.session.commit()
    return redirect(url_for('main.resource_detail', resource_id=resource.id))

@main.route("/resource/<int:resource_id>/delete", methods=['POST'])
@login_required
def delete_resource(resource_id):
    resource = Resource.query.get_or_404(resource_id)
    if resource.author != current_user:
        abort(403)
    db.session.delete(resource)
    db.session.commit()
    flash('Recurso removido.', 'success')
    return redirect(url_for('main.index'))
