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
# File: hanjadb_output.py
# Author: DaeHyun Sung
# Description:
# Convert saved DB "HANJA" table's contents to text file.
# format] hangul:hanja:note
# Example] 가:家:

import sqlite3


if __name__ == '__main__':
    # SQLite database open
    # file open
    print('open csv file & db file')
    f = open("./data/hhc_char.txt", 'w+')
    conn = sqlite3.connect('./data/libreoffice_hanja.db')
    cur = conn.cursor()
    # 가-U+AC00, 힣-U+D7A3
    hangul_syllable_list = list(range(0xAC00,0xD7A4))
    for i in hangul_syllable_list:
        cur.execute('select hanja from HANJA_CHAR WHERE hangul=:hangul order by idx asc', {"hangul": chr(i)})
        hanjaitem_list = cur.fetchall()
        if len(hanjaitem_list) > 0:
            print("%s:" % (chr(i)), end='', flush=True)
            f.write("%s:" % (chr(i)))
            for hanja_item in hanjaitem_list:
                print("%s" % (hanja_item), end='', flush=True)
                f.write("%s" % ((hanja_item)))
            print("", flush=True)
            f.write("\n")
    conn.close()
    f.close()