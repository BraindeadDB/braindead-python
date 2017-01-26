import os

from braindeaddb import config
from braindeaddb.app import app

if __name__ == '__main__':
    if not os.path.isdir(config.store):
        os.mkdir(config.store)
    app.run()
