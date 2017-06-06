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
# Example] 가:家:집 가
import sqlite3

FLAG_DEFAULT = 'D'
FLAG_INSERT = 'I'
FLAG_MODIFY = 'F'
FLAG_REMOVE = 'R'

if __name__ == '__main__':
    # SQLite database open
    # file open
    print('open csv file & db file')
    f = open("./data/hanja_add.txt", 'w+')
    conn = sqlite3.connect('./data/hanja.db')
    cur = conn.cursor()
    cur.execute('select hangul, hanja, note from HANJA order by hangul asc')
    for row in cur:
        print(row)
        f.write("%s:%s:%s\n" % (row[0], row[1], row[2]))
    conn.close()
    f.close()