import os
import sys

# Ajouter le path pour les imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app.models import Space, Page

def remove_global_space():
    global_space = Space.get_or_none(Space.name == 'Global')
    if global_space:
        print("Found Global Space. Updating pages...")
        Page.update(space=None).where(Page.space == global_space).execute()
        global_space.delete_instance()
        print("Global Space deleted.")
    else:
        print("Global Space not found.")

if __name__ == '__main__':
    remove_global_space()
