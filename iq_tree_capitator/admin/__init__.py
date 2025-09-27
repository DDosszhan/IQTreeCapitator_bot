from .add_tree import get_add_tree_handler


def get_admin_handlers():
    yield get_add_tree_handler()
