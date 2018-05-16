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
# HANJA_LIST.csv file data to sqlite db "HANJA_CHAR" table
import sqlite3
import csv

FLAG_DEFAULT = 'D'
FLAG_INSERT = 'I'
FLAG_MODIFY = 'F'
FLAG_REMOVE = 'R'
FLAG_LIBREOFFICEHANJA = 'L'

# Make some frash tables using executescript()
first_executescript = '''
DROP TABLE IF EXISTS HANJA_CHAR;

CREATE TABLE HANJA_CHAR (
    idx  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    hangul  TEXT,
    hanja   TEXT,
    flag	TEXT,
    date	TEXT,
    note    TEXT
);'''


def chomp(s):
    return s[:-1] if s.endswith('\n') else s


def trim_newlines(slist):
    for i in range(len(slist)):
        slist[i] = chomp(slist[i])
    return slist


if __name__ == '__main__':
    # SQLite database open
    conn = sqlite3.connect('./data/libreoffice_hanja.db')
    cur = conn.cursor()
    # db default
    cur.executescript(first_executescript)
    line_counter = 0 # 첫 줄

    with open('./data/HANJA_LIST.csv', newline='') as csvfile:
        hanjacsvreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in hanjacsvreader:
            if line_counter == 0:
                line_counter += 1
                continue
            else:
                print(row[0],row[1], row[2], row[3], row[4])
                cur.execute('''INSERT OR IGNORE INTO HANJA_CHAR (hangul, hanja, flag, date, note)
                                   VALUES ( ?, ?, ?, ?, ? )''',
                            (row[0], row[1], row[2], row[3], row[4]))
            line_counter += 1
    csvfile.close()
    conn.commit()

    # read hhc_char.dic file
    f = open('./hhc_char.dic', 'r')

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
            hanja_sound = hanja_item[0]
            for hanja_element in list(hanja_item[1]):
                #print("%s:%s" % (hanja_sound, hanja_element))
                # 한자 검색
                # select
                cur.execute("select count(*) from HANJA_CHAR WHERE hangul=:hangul and hanja=:hanja",
                            {"hangul": chomp(hanja_sound), "hanja": chomp(hanja_element)})
                dbSelCount = cur.fetchone()[0]
                if dbSelCount == 0:
                    # not found, then insert  hanja data
                    print("hangul: %s, Hanja: %s, CodePoint: U+%04X | http://hanja.naver.com/hanja?q=%s&cp_code=0&sound_id=0" %
                          (hanja_sound, hanja_element, ord(hanja_element), hanja_element))
                    cur.execute('''INSERT OR IGNORE INTO HANJA_CHAR (hangul, hanja, note, flag, date)
                                        VALUES ( ?, ?, ?, ?, ? )''',
                                (hanja_sound, hanja_element, "", FLAG_LIBREOFFICEHANJA, "2018-05-16",))
                    conn.commit()
    # 乒 - 물건 부딪치는 소리 '병', 물건 부딪치는 소리 '핑'
    # 乓 - 물건을 부딪치는 소리 '병', 물건을 부딪치는 소리 '팡'
    cur.execute('''INSERT OR IGNORE INTO HANJA_CHAR (hangul, hanja, note, flag, date)
                                            VALUES ( ?, ?, ?, ?, ? )''',
                ('핑', '乒', '', FLAG_LIBREOFFICEHANJA, '2018-05-16',))
    cur.execute('''INSERT OR IGNORE INTO HANJA_CHAR (hangul, hanja, note, flag, date)
                                                VALUES ( ?, ?, ?, ?, ? )''',
                ('병', '乓', '', FLAG_LIBREOFFICEHANJA, '2018-05-16',))
    cur.execute('''INSERT OR IGNORE INTO HANJA_CHAR (hangul, hanja, note, flag, date)
                                                VALUES ( ?, ?, ?, ?, ? )''',
                ('팡', '乓', '', FLAG_LIBREOFFICEHANJA, '2018-05-16',))
    conn.commit()
    f.close()
    conn.close()
