from pypinyin import pinyin, Style

# 待转换的字符串
d = '架构设计一组'

# 假设已存在的字段列表
existing_fields = ['jgsjyz', 'jgsjyz1', 'jgsjyz2']

# 转换为拼音首字母
pinyin_list = pinyin(d, style=Style.FIRST_LETTER)

pinyin = ''.join([x[0] for x in pinyin_list])

# 追加递增的数字来确保唯一性
suffix = 1

while True:
    result = ''
    if pinyin in existing_fields:
        suffix += 1
        # 将转换后的拼音添加到结果字符串
        result += pinyin + str(suffix)
        pinyin = result
    else:
        break

print(pinyin)
