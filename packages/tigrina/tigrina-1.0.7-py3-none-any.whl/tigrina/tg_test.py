import re
from tigrina.tg_main import Tigrina_words as tigrina_words
# array=['ግደ', 'ጸጋይ', 'ዝፋን', 'ሂወት']
# get_family_info =tigrina_words.get_family("ኣሲራቶም")
# print("get_family_info:",get_family_info)
code=tigrina_words.code_translation("ግደ","code")
print("code:",code)
decode=tigrina_words.code_translation(code,"decode")
print("decode:",decode)
# sample to test fetching data
# result_select=tigrina_words.Data.select("SELECT * from adjectives where word_tigrina='መበቈልhh'")
# print("result_select:",len(result_select))
# normalize_data=tigrina_words.pandas_data_frame_to_object(result_select)
# print("normalize_data:",normalize_data)
# sample to test data fetching from encode data tables
# first code the word
# code=tigrina_words.code_translation("መበቈል","code","")
# query=f"SELECT * from tokenized_data where tg_code like '%{code}%'"
# get_result=tigrina_words.Data.select(query)
# print("get_result:",get_result)
# object_list = [tigrina_words.pandas_data_frame_to_object(**row.to_dict()) for _, row in get_result.iterrows()]
# print(object_list)
# result_insert=tigrina_words.Data.insert("insert into tb1 (id, name, age, city) values(1,'xegay segid', 38, 'Germany')")
# print("result_insert:",result_insert)

# result_update=tigrina_words.Data.update("update tb1 set name='gide segid test', age=578 where name='gide segid test'")
# print("result_update:",result_update)

# result_delete=tigrina_words.Data.delete("delete * from tb1")
# print("result_delete:",result_delete)

# result_tables=tigrina_words.Data.get_tables("show tables")
# print("result_tables:",result_tables)

# result_fields=tigrina_words.Data.get_fields("describe verbs")
# print("result_fields:",result_fields)

