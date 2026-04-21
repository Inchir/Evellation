# импортируем все blueprintы
from .user_routes import user_bp
from .evellation_routes import evellation_bp

# массив blueprints
blueprints = [user_bp, evellation_bp]
