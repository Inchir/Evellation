# импортируем формы
from src.app.forms import RegisterForm, LoginForm

# импортируем сессию
from src.models import db_session

# импортируем модели
from src.models.users import User

# импортируем все blueprintы
from src.app.routes.user_routes import user_bp

# массив blueprints
blueprints = [user_bp]
