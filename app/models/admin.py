from sqladmin import ModelView
from app.models.user import User


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id,
        User.username,
        User.email,
        User.is_active,
        User.is_admin,
        User.created_at,
        User.updated_at
    ]
    column_searchable_list = [User.username, User.email]
    column_sortable_list = [User.id, User.username, User.email, User.is_active, User.is_admin]
    column_default_sort = ("created_at", True)
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
