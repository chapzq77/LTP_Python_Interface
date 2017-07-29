# LTP的 python 接口
>自己在服务器上搭载 LTP 的程序，并开放端口供LTP_MODEL使用，根据自己的情况，实现了：分词，词性标注，命名实体识别，依存句法分析，语义角色标注。同时，基于该接口，我实现了，**命名实体的抽取和事实三元组的抽取工作**

### LTP_MODEL的优点
- LTP的 Python 接口，不需要安装其他额外的库
- 可以根据自己的需要更改代码，实现不同的输入和输出形式
- 实现了命名实体的抽取：人名，地名，机构名
- 实现了三元组的抽取：主谓宾，动宾关系，介宾关系，（实体，关系，实体）

### LTP_MODEL的用法
- 分词

```
input_list = ['中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人。']
model = LTP_MODEL()
print model.segment(input_list)
```
- 词性标注

```
input_list = ['中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人。']
model = LTP_MODEL()
print model.postagger(input_list)
```
- 命名实体识别

```
input_list = ['中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人。']
model = LTP_MODEL()
print model.NamedEntityRecognizer(input_list,Entity_dist=True)[0]['place'][0]
print model.NamedEntityRecognizer(input_list)
```

- 依存句法分析

```
input_list = ['中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人。']
model = LTP_MODEL()
print model.SyntaxParser(input_list)
```
- 三元组抽取

```
input_sentence = "中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人"
model = LTP_MODEL()
Subjective_guest,Dynamic_relation,Guest,Name_entity_relation = model.triple_extract(input_sentence)
for e in Subjective_guest[0]:
    print e,
print "\n"
for e in Dynamic_relation[0]:
    print e,
```
- 语义角色分析

```
input_list = ["中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人"]
model = LTP_MODEL()
print model.SementicRoleLabeller(input_list)
```
### 后期还将添加关键字抽取功能

