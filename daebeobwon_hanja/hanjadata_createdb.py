#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# File: handa_createdb.py
# Author: DaeHyun Sung
# Description:
# libhangul's hanja.txt text data to sqlite db "HANJA" table
import sqlite3

# Make some fresh tables using executescript()
first_executescript ='''
DROP TABLE IF EXISTS HANJA;

CREATE TABLE HANJA (
    idx  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    hangul    TEXT,
    hanja     TEXT,
    note      TEXT,
    flag      TEXT
);'''

FLAG_DEFAULT = 'D'
FLAG_INSERT = 'I'
FLAG_MODIFY = 'F'
FLAG_REMOVE = 'R'

def chomp(s):
    return s[:-1] if s.endswith('\n') else s

def trim_newlines(slist):
    for i in range(len(slist)):
        slist[i] = chomp(slist[i])
    return slist

if __name__ == '__main__':
    # SQLite database open
    conn = sqlite3.connect('./data/hanja.db')
    cur = conn.cursor()
    # db default
    cur.executescript(first_executescript)

    # read hanja.txt file
    f = open('./data/hanja.txt', 'r')

    lines = f.readline()
    while True:
        hanja_text_line = f.readline()
        if not hanja_text_line:
            break
        if len(hanja_text_line) < 1:
            continue
        elif hanja_text_line[0] == '' or hanja_text_line[0] == '#' or hanja_text_line[0] == '\n':
            continue
        else:
            hanja_item = hanja_text_line.split(':')
            trim_newlines(hanja_item)
            print("Hangul:%s|Hanja: %s|Note: %s" % (hanja_item[0], hanja_item[1], hanja_item[2]))
            cur.execute('''INSERT OR IGNORE INTO HANJA (hangul, hanja, note, flag)
                    VALUES ( ?, ?, ?, ? )''', (hanja_item[0], hanja_item[1], hanja_item[2], FLAG_DEFAULT, ))
    conn.commit()
    f.close()