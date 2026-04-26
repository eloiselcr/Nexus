import datetime
from flask import Blueprint, render_template, request
from app.models import Space, Category, Page, Link

views_bp = Blueprint('views', __name__)

@views_bp.context_processor
def inject_sidebar_data():
    """Injecte les données nécessaires pour la sidebar de base.html sur toutes les routes."""
    spaces = Space.select().order_by(Space.name)
    categories = Category.select().order_by(Category.name)
    return dict(spaces=spaces, categories=categories)

@views_bp.route('/', methods=['GET'])
def index():
    """Route principale de l'application (Dashboard)."""
    # Données pour le dashboard
    total_pages = Page.select().count()
    total_links = Link.select().count()
    recent_pages = Page.select().order_by(Page.updated_at.desc()).limit(5)
    
    today_str = datetime.date.today().strftime('%A %d %B %Y')
    
    return render_template(
        'dashboard.html',
        today=today_str,
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

@views_bp.route('/space/<int:space_id>', methods=['GET'])
def view_space(space_id):
    space = Space.get_or_none(Space.id == space_id)
    if not space:
        return "Espace introuvable", 404
        
    pages = Page.select().where(Page.space == space).order_by(Page.updated_at.desc())
    return render_template('space_view.html', space=space, pages=pages)

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

@views_bp.route('/page/<int:page_id>', methods=['GET'])
def view_page(page_id):
    page = Page.get_or_none(Page.id == page_id)
    if not page:
        return "Page introuvable", 404
        
    # On récupérera les propriétés plus tard
    return render_template('page.html', page=page)


