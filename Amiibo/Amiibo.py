#!/usr/bin/env python
"""
@author: N3evin
@copyright: Copyright 2017, AmiiboAPI
@license: MIT License
"""

class amiibo(object):

    # Constructor
    def __init__(self, name, head, tail):
        self.name = name
        self.head = head
        self.tail = tail

    # Get the name of the amiibo.
    def getName(self):
        return self.name

    # Get the head value of the amiibo.
    def getHead(self):
        return self.head

    # Get the tail value of the amiibo.
    def getTail(self):
        return self.tail

