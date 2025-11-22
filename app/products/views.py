from flask import render_template
from app.products import bp

@bp.route('/')
def products():
    items = ["Яблуко", "Апельсин", "Банан"]
    return render_template('products/info.html', title="Продукти", items=items)
