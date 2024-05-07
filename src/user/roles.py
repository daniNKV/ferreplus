from rolepermissions.roles import AbstractUserRole


class User(AbstractUserRole):
    available_permissions = {
        "create_product": True,
        "modify_product": True,
        "delete_product": True,
        "publish_product": True,
        "unpublish_product": True,
    }

class Owner(AbstractUserRole):
    available_permissions = {
        "create_shop_product": True,
        "modify_shop_product": True,
        "delete_shop_product": True,
        "create_employee": True,
        "delete_employee": True,
        "create_branch": True,
        "delete_branch": True,                
        "modify_branch": True,
    }


class Employee(AbstractUserRole):
    available_permissions = {
    }
