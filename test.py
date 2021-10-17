# -*- coding: utf-8 -*-

from plugin import Main

if __name__ == "__main__":
    r = Main().query('en cs hello my love')
    print(r)

    r = Main().query('en bflm hello my love')
    print(r)
