import datetime
from flask import Blueprint, render_template, request
from app.models import Space, Category, Page, Link

views_bp = Blueprint('views', __name__)

@views_bp.context_processor
def inject_sidebar_data():
    """Injecte les données nécessaires pour la sidebar de base.html sur toutes les routes."""
    spaces = Space.select().where(Space.deleted_at.is_null()).order_by(Space.order_index, Space.name)
    categories = Category.select().order_by(Category.name)
    return dict(spaces=spaces, categories=categories)

@views_bp.route('/', methods=['GET'])
def index():
    """Route principale de l'application (Dashboard)."""
    # Données pour le dashboard
    total_pages = Page.select().where(Page.deleted_at.is_null()).count()
    total_links = Link.select().count()
    recent_pages = Page.select().where(Page.deleted_at.is_null()).order_by(Page.updated_at.desc()).limit(5)
    
    today_date = datetime.date.today()
    
    return render_template(
        'dashboard.html',
        today=today_date,
        total_pages=total_pages,
        total_links=total_links,
        recent_pages=recent_pages
    )

@views_bp.route('/space/new', methods=['GET', 'POST'])
def new_space():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        color = request.form.get('color', '#10b981')
        
        if name:
            space = Space.create(name=name, description=description, color=color)
            from flask import redirect, url_for
            return redirect(url_for('views.view_space', space_id=space.id))
            
    return render_template('space_form.html')

@views_bp.route('/space/<int:space_id>/edit', methods=['GET', 'POST'])
def edit_space(space_id):
    space = Space.get_or_none((Space.id == space_id) & Space.deleted_at.is_null())
    if not space:
        return "Espace introuvable", 404
        
    if request.method == 'POST':
        space.name = request.form.get('name')
        space.description = request.form.get('description')
        space.color = request.form.get('color', '#10b981')
        space.save()
        from flask import redirect, url_for
        return redirect(url_for('views.view_space', space_id=space.id))
        
    return render_template('space_form.html', space=space)

@views_bp.route('/space/<int:space_id>/delete', methods=['POST'])
def delete_space(space_id):
    space = Space.get_or_none((Space.id == space_id) & Space.deleted_at.is_null())
    if space:
        now = datetime.datetime.now()
        space.deleted_at = now
        space.save()
        # Soft delete en cascade des pages
        Page.update(deleted_at=now).where(Page.space == space).execute()
    from flask import redirect, url_for
    return redirect(url_for('views.index'))

@views_bp.route('/space/<int:space_id>/move_<direction>', methods=['POST'])
def move_space(space_id, direction):
    space = Space.get_or_none((Space.id == space_id) & Space.deleted_at.is_null())
    if space:
        # Trouver l'espace avec lequel échanger
        if direction == 'up':
            other = Space.select().where(Space.deleted_at.is_null(), Space.order_index < space.order_index).order_by(Space.order_index.desc()).first()
        else:
            other = Space.select().where(Space.deleted_at.is_null(), Space.order_index > space.order_index).order_by(Space.order_index.asc()).first()
            
        if other:
            # Swap
            temp = space.order_index
            space.order_index = other.order_index
            other.order_index = temp
            space.save()
            other.save()
            
    from flask import redirect, url_for
    return redirect(request.referrer or url_for('views.index'))

@views_bp.route('/space/<int:space_id>', methods=['GET'])
def view_space(space_id):
    space = Space.get_or_none((Space.id == space_id) & Space.deleted_at.is_null())
    if not space:
        return "Espace introuvable", 404
        
    pages = Page.select().where((Page.space == space) & Page.deleted_at.is_null()).order_by(Page.updated_at.desc())
    return render_template('space_view.html', space=space, pages=pages, categories=Category.select())

@views_bp.route('/space/<int:space_id>/new_page', methods=['POST'])
def new_page_in_space(space_id):
    space = Space.get_or_none(Space.id == space_id)
    if not space:
        return "Espace introuvable", 404
        
    category_id = request.form.get('category_id')
    category = Category.get_or_none(Category.id == category_id)
    if not category:
        from flask import redirect, url_for
        return redirect(url_for('views.view_space', space_id=space.id))
        
    page = Page.create(title="Nouvelle note", category=category, space=space)
    from flask import redirect, url_for
    return redirect(url_for('views.view_page', page_id=page.id))

@views_bp.route('/category/<int:category_id>', methods=['GET'])
def view_category(category_id):
    category = Category.get_or_none(Category.id == category_id)
    if not category:
        return "Catégorie introuvable", 404
        
    # On n'affiche que les pages Globales (space_id is null) de cette catégorie
    pages = Page.select().where((Page.category == category) & (Page.space.is_null()) & Page.deleted_at.is_null()).order_by(Page.updated_at.desc())
    return render_template('category_view.html', category=category, pages=pages)

@views_bp.route('/graph', methods=['GET'])
def global_graph():
    return render_template('graph.html')

@views_bp.route('/page/quick_capture', methods=['POST'])
def quick_capture():
    title = request.form.get('title')
    space_id = request.form.get('space_id')
    category_id = request.form.get('category_id')
    
    if not title or not category_id:
        return "Données manquantes", 400
        
    # Validation du Space
    space = None
    if space_id != 'global':
        space = Space.get_or_none(Space.id == space_id)
        
    category = Category.get_or_none(Category.id == category_id)
    if not category:
        return "Catégorie invalide", 400
        
    # Création de la page (Vide pour l'instant)
    page = Page.create(title=title, category=category, space=space)
    
    from flask import redirect, url_for
    return redirect(url_for('views.view_page', page_id=page.id))

@views_bp.route('/page/<int:page_id>/delete', methods=['POST'])
def delete_page(page_id):
    page = Page.get_or_none((Page.id == page_id) & Page.deleted_at.is_null())
    if page:
        page.deleted_at = datetime.datetime.now()
        page.save()
        from flask import redirect, url_for
        if page.space:
            return redirect(url_for('views.view_space', space_id=page.space.id))
        else:
            return redirect(url_for('views.view_category', category_id=page.category.id))
    return "Page introuvable", 404

@views_bp.route('/page/<int:page_id>', methods=['GET'])
def view_page(page_id):
    page = Page.get_or_none((Page.id == page_id) & Page.deleted_at.is_null())
    if not page:
        return "Page introuvable", 404
    return render_template('page.html', page=page)
