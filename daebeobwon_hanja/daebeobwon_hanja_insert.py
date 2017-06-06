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
# File: daebeobwon_hanja_insert.py
# Author: DaeHyun Sung
# Description
# Make sure that the list of hanja for use in personal names(인명용한자,人名用漢字)
# by DaeBeobWon(대법원,大法院,The Supreme Court of Korea[Republic of Korea]) are exist in the HANJA DB Table,
# If not, insert the value into HANJA DB Table
import csv
import sqlite3

FLAG_DEFAULT = 'D'
FLAG_INSERT = 'I'
FLAG_MODIFY = 'F'
FLAG_REMOVE = 'R'

if __name__ == '__main__':
    # SQLite database open
    # file open
    print('open csv file & db file')
    conn = sqlite3.connect('./data/hanja.db')
    cur = conn.cursor()
    csvfile = open('./data/daebeobwon_hanjalist.csv', newline='')
    daebeobwon_hanja_list = csv.reader(csvfile)
    for row in daebeobwon_hanja_list:
        print('Hangul: %s, Hanja: %s' % (row[0], row[1]))
        # select
        hangul = row[0]
        hanja = row[1]
        cur.execute("select count(*) from HANJA WHERE hangul=:hangul and hanja=:hanja",
                    {"hangul": hangul, "hanja": hanja})
        dbSelCount = cur.fetchone()[0]
        if dbSelCount == 0:
            # not found, then insert daebeobwon hanja data
            print('not found. insert Hangul: %s, Hanja: %s' % (hangul, hanja))
            cur.execute(
                "insert into HANJA(hangul, hanja, note, flag)  "
                "VALUES "
                "(:hangul, :hanja, :note, :flag )",
                {"hangul": hangul, "hanja": hanja, "note":"", "flag": FLAG_INSERT})
        else:
            print("found!")

    conn.commit()
    csvfile.close()
    #close db file
    conn.close()