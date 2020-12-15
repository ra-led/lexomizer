#!/usr/bin/env python3
from conf import CFG
from app import app

def main():
    app.debug = True
    host = '0.0.0.0'
    port = CFG['port']

    app.run(host=host, port=port)


if __name__ == '__main__':
    # run app
    main()
