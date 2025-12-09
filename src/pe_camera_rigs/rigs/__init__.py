# rigs/__init__.py

from . import isometric
from . import orbit
from . import vr180
from . import vr360mono
# ... etc

# All rig modules that should be registered.
rig_modules = [
    isometric,
    orbit,
    vr180,
    vr360mono,
]

def register():
    for module in rig_modules:
        module.register()

def unregister():
    for module in reversed(rig_modules):
        module.unregister()
