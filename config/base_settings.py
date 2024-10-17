DEBUG = True

if DEBUG:
    from .dev_settings import *
else:
    from .prod_settings import *
