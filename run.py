#!/usr/bin/env python3
from conf import CFG
from app import app

if __name__ == '__main__':
    # run app
    app.debug = False
    host = '0.0.0.0'
    port = CFG['port']

    app.run(host=host, port=port)
