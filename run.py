#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

from forms import my_drawer_form


def main():
    app, mainForm, window = my_drawer_form.init()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
