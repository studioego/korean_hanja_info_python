# 대법원 인명용한자추가 프로젝트 daebeobwon_hanja

(English follows Korean)

### 실행순서
1. 우선 `hanjadata_createdb.py` then create hanja.db
2. 그다음 `daebeobwon_hanja_rawtextprocess.py` then 
3. 이후 `daebeobwon_hanja_insert.py`
4. 이제 `hanjadb_output.py`를 실행하여, `hanja.txt`파일을 얻을수잇습니다

`hanja_add.txt`은 `hanja.txt`파일 규격인 `한글:한자:주석` 으로 구성되어 있으며, 가나다순(順)으로 정렬되었습니다.


----

## Korea Hanja Data by DaeBeonWon(대법원,大法院,The Supreme Court of Korea[Republic of Korea])

the list of hanja for use in personal names(인명용한자,人名用漢字) by DaeBeobWon(대법원,大法院,The Supreme Court of Korea[Republic of Korea]) are exist in the HANJA DB Table,
If not, insert the value into HANJA DB Table 

### Execution Order 
1. run `hanjadata_createdb.py` then create hanja.db
2. run `daebeobwon_hanja_rawtextprocess.py` then 
3. run `daebeobwon_hanja_insert.py`
4. run `hanjadb_output.py`