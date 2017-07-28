#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-07-28 11:25:02
# @Author  : 周奇 (2590193099@qq.com)
# @Link    : ……
import json
import urllib, urllib2
'''
参考LTP：http://ltp.readthedocs.io/zh_CN/latest/ltpserver.html
搭载LTP在服务器上，开放指定的端口
提供一个免费使用的中文分词，词性标注，命名实体识别，语义角色标注，依存语法分析的接口
'''

class LTP_MODEL():
    def __init__(self,server_url = "http://IP:port/ltp"):
        #task 任务的具体形式，可以是分词：'ws'，词性标注：'pos',依存语法分析：'dp'，命名实体识别：ner语义角色标注：'srl',或者全部：'all' 
        self.server_url = server_url
        


    def build_xml(self,input_list):
        '''
        功能：根据输入列表，构建输入的xml的具体形式
        '''
        ss_start = '<?xml version="1.0" encoding="utf-8" ?><xml4nlp><note sent="y" word="n" pos="n" ne="n" parser="n" srl="n" /><doc><para><sent cont="'
        ss_middle = '" /></para><para><sent cont="'
        ss_end = '" /></para></doc></xml4nlp>'
        ss = ss_start + ss_middle.join(input_list) + ss_end
        return ss

    def output_json(self,task,input_xml):
        '''
        功能：根据输入的xml，上传服务器，返回指定任务的结果json对象
        '''
        data = {'s': input_xml, 'x': 'y', 't': task}
        try:
            request = urllib2.Request(self.server_url)
            params = urllib.urlencode(data)
            response = urllib2.urlopen(request, params)
            content = response.read().strip()
        except Exception:
            return
        return json.loads(content)
    
    def segment(self,input_list,task='ws'):
        '''
        功能：实现分词文本的分词
        返回值：每个文本的形成一个列表[['word1','word2'],['word1','word3'],……]
        '''
        input_xml = self.build_xml(input_list)
        content = self.output_json(task,input_xml)
        segmented_text_list = []
        for text_other in content:
            sent = text_other[0]
            text =[]
            for word in sent:
                text.append(word['cont'])
            segmented_text_list.append(text)
        return segmented_text_list

    def postagger(self,input_list,task = 'pos'):
        '''
        功能：实现文本中每个词的词性标注
        返回值：每个文本是一个列表，列表中的每个词也是个列表[[['word1',u'O'],['word2',u'O']],[['word2',u'O'],['word5',u'O']],……]
        '''
        input_xml = self.build_xml(input_list)
        content = self.output_json(task,input_xml)
        postagger_text_list = []
        for text_other in content:
            sent = text_other[0]
            text =[]
            for word in sent:
                text.append([word['cont'],word['pos']])
            postagger_text_list.append(text)
        return postagger_text_list

    def NamedEntityRecognizer(self,input_list,task = 'ner',Entity_dist=False,repead=False):
        '''
        功能：识别文本中的命名实体：地名，组织名和机构名
        参数repead：表示是否进行去重处理 ，默认是不去重
        参数Entity_dist：表示每个文本，返回的识别后的列表，还是抽取后的实体字典，默认返回的是列表
        返回值的形式：1.[[['word1',u'O'],['word2',u'O'],['word3',u'O']],[['word2',u'O'],['word3',u'O'],['word4',u'O']],……]
                      2.[{'person':[],'place':[],'organization':[]},{'person':[],'place':[],'organization':[]},{'person':[],'place':[],'organization':[]},……] 
        '''
        input_xml = self.build_xml(input_list)
        content = self.output_json(task,input_xml)
        entity_text_list = []
        #
        for text_other in content:
            sent = text_other[0]
            text =[]
            words_list = []
            entity_note_list = []
            for word in sent:
                text.append([word['cont'],word['ne']])
            entity_text_list.append(text)
        if Entity_dist:
            extract_entity_list = []
            for words_entity_note_list in entity_text_list:
                extract_entity_list.append(self.get_entity_dict(words_entity_note_list,repead))
            return extract_entity_list
        else:
            return entity_text_list

    def get_entity_dict(self,words_entity_note_list,repead):
        '''
        功能：根据实体识别的标志，统计文本中的命名实体
        参数repead：表示是否进行去重处理 ，默认是不去重
        返回值：{'person':[],'place':[],'organization':[]}
        '''
        '''
        O：这个词不是NE
        S：这个词单独构成一个NE
        B：这个词为一个NE的开始
        I：这个词为一个NE的中间
        E：这个词位一个NE的结尾
        Nh：人名
        Ni：机构名
        Ns：地名
        '''
        name_entity_dist = {}
        # 存储不同实体的列表
        name_entity_list = []
        place_entity_list = []
        organization_entity_list = []

        ntag_E_Nh = ""
        ntag_E_Ni = ""
        ntag_E_Ns = ""
        for word, ntag in words_entity_note_list:
            #print word+"/"+ntag,
            if ntag[0]!="O":
                if ntag[0]=="S":
                    if ntag[-2:]=="Nh":
                        name_entity_list.append(word)
                    elif ntag[-2:]=="Ni":
                        organization_entity_list.append(word)
                    else:
                        place_entity_list.append(word)
                elif ntag[0]=="B":
                    if ntag[-2:]=="Nh":
                        ntag_E_Nh =ntag_E_Nh + word
                    elif ntag[-2:]=="Ni":
                        ntag_E_Ni =ntag_E_Ni + word
                    else:
                        ntag_E_Ns =ntag_E_Ns +word
                elif ntag[0]=="I":
                    if ntag[-2:]=="Nh":
                        ntag_E_Nh =ntag_E_Nh + word
                    elif ntag[-2:]=="Ni":
                        ntag_E_Ni =ntag_E_Ni + word
                    else:
                        ntag_E_Ns =ntag_E_Ns +word
                else:
                    if ntag[-2:]=="Nh":
                        ntag_E_Nh =ntag_E_Nh + word
                        name_entity_list.append(ntag_E_Nh)
                        ntag_E_Nh = ""
                    elif ntag[-2:]=="Ni":
                        ntag_E_Ni =ntag_E_Ni + word
                        organization_entity_list.append(ntag_E_Ni)
                        ntag_E_Ni = ""
                    else:
                        ntag_E_Ns =ntag_E_Ns +word
                        place_entity_list.append(ntag_E_Ns)
                        ntag_E_Ns = ""

        if repead:
            name_entity_dist['person'] = list(set(name_entity_list))
            name_entity_dist['organization'] = list(set(organization_entity_list))
            name_entity_dist['place'] = list(set(place_entity_list))
        else:
            name_entity_dist['person'] = name_entity_list
            name_entity_dist['organization'] = organization_entity_list
            name_entity_dist['place'] = place_entity_list
        return name_entity_dist

    def SyntaxParser(self,input_list,task='dp'):
        '''
        # head = parent+1
        # relation = relate  可以从中间抽取head 和 relation 构成LTP 的标准输出，但是为了根据自己的情况，直接输出返回的全部的信息
        功能：实现依存句法分析
        返回值：每个文本的形成一个列表
        [[{u'relate': u'WP', u'cont': u'\uff0c', u'id': 4, u'parent': 3, u'pos': u'wp'},{u'relate': u'RAD', u'cont': u'\u7684', u'id': 1, u'parent': 0, u'pos': u'u'}],……]
        '''
        input_xml = self.build_xml(input_list)
        content = self.output_json(task,input_xml)
        syntaxparser_text_list = []
        for text_other in content:
            sent = text_other[0]
            text =[]
            for word in sent:
                text.append(word)
            syntaxparser_text_list.append(text)
        return syntaxparser_text_list

    
    def triple_extract(self,sentence): 
        '''
        功能: 对于给定的句子进行事实三元组抽取
        Args:
            sentence: 要处理的语句 
                      形式是：'真实的句子'
        '''
        Subjective_guest = [] #主谓宾关系(e1,r,e2)
        Dynamic_relation = [] #动宾关系
        Guest = []  # 介宾关系
        Name_entity_relation = [] # 命名实体之间的关系
        # 分词后词的列表 words，词性列表 postags，实体标志列表 netags，语法分析列表 arcs
        words = []
        postags = []
        netags = []
        arcs = []
        syntaxparser_text_list = self.SyntaxParser([sentence])
        entity_list = self.NamedEntityRecognizer([sentence])
        for words_property_list in syntaxparser_text_list[0]:
            words.append(words_property_list['cont'])
            postags.append(words_property_list['pos'])
            arcs.append({'head':words_property_list['parent']+1,'relation':words_property_list['relate']})
        for words_entity_list in entity_list[0]:
            netags.append(words_entity_list[1])

        child_dict_list = self.build_parse_child_dict(words, postags, arcs)

        for index in range(len(postags)):
            
            # 抽取以谓词为中心的事实三元组
            if postags[index] == 'v':
                child_dict = child_dict_list[index]
                # 主谓宾
                if child_dict.has_key('SBV') and child_dict.has_key('VOB'):
                    e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                    r = words[index]
                    e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                    Subjective_guest.append((e1, r, e2))

                # 定语后置，动宾关系
                if arcs[index]['relation'] == 'ATT':
                    if child_dict.has_key('VOB'):
                        e1 = self.complete_e(words, postags, child_dict_list, arcs[index]['head'] - 1)
                        r = words[index]
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
                        temp_string = r + e2
                        if temp_string == e1[:len(temp_string)]:
                            e1 = e1[len(temp_string):]
                        if temp_string not in e1:
                            Dynamic_relation.append((e1, r, e2))
                            

                # 含有介宾关系的主谓动补关系
                if child_dict.has_key('SBV') and child_dict.has_key('CMP'):
                    #e1 = words[child_dict['SBV'][0]]
                    e1 = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0])
                    cmp_index = child_dict['CMP'][0]
                    r = words[index] + words[cmp_index]
                    if child_dict_list[cmp_index].has_key('POB'):
                        e2 = self.complete_e(words, postags, child_dict_list, child_dict_list[cmp_index]['POB'][0])
                        Guest.append((e1, r, e2))
                        
            

            # 尝试抽取命名实体有关的三元组
            if netags[index][0] == 'S' or netags[index][0] == 'B':
                ni = index
                if netags[ni][0] == 'B':
                    while netags[ni][0] != 'E':
                        ni += 1
                    e1 = ''.join(words[index:ni + 1])
                else:
                    e1 = words[ni]
                #上面是抽取实体，没有判断是什么类型的实体。。
                if arcs[ni]['relation'] == 'ATT' and postags[arcs[ni]['head'] - 1] == 'n' and netags[arcs[ni]['head'] - 1] == 'O':
                    r = self.complete_e(words, postags, child_dict_list, arcs[ni]['head'] - 1)
                    if e1 in r:
                        r = r[(r.index(e1) + len(e1)):]
                    if arcs[arcs[ni]['head'] - 1]['relation'] == 'ATT' and netags[arcs[arcs[ni]['head'] - 1]['head'] - 1] != 'O':
                        e2 = self.complete_e(words, postags, child_dict_list, arcs[arcs[ni]['head'] - 1]['head'] - 1)
                        mi = arcs[arcs[ni]['head'] - 1]['head'] - 1
                        li = mi
                        if netags[mi][0] == 'B':
                            while netags[mi][0] != 'E':
                                mi += 1
                            e = ''.join(words[li + 1:mi + 1])
                            e2 += e
                        if r in e2:
                            e2 = e2[(e2.index(r) + len(r)):]
                        if r + e2 in sentence:
                            Name_entity_relation.append((e1, r, e2))
        return Subjective_guest,Dynamic_relation,Guest,Name_entity_relation
                            


    def build_parse_child_dict(self,words, postags, arcs):
        """
        功能：为句子中的每个词语维护一个保存句法依存儿子节点的字典
        Args:
            words: 分词列表
            postags: 词性列表
            arcs: 句法依存列表
        """
        child_dict_list = []
        for index in range(len(words)):
            child_dict = dict()
            for arc_index in range(len(arcs)):
                if arcs[arc_index]['head'] == index + 1:
                    if child_dict.has_key(arcs[arc_index]['relation']):
                        child_dict[arcs[arc_index]['relation']].append(arc_index)
                    else:
                        child_dict[arcs[arc_index]['relation']] = []
                        child_dict[arcs[arc_index]['relation']].append(arc_index)
            child_dict_list.append(child_dict)
        return child_dict_list


    def complete_e(self, words, postags, child_dict_list, word_index):
        """
        功能：完善识别的部分实体
        """
        child_dict = child_dict_list[word_index]
        prefix = ''

        if child_dict.has_key('ATT'):
            for i in range(len(child_dict['ATT'])):
                prefix += self.complete_e(words, postags, child_dict_list, child_dict['ATT'][i])

        postfix = ''
        if postags[word_index] == 'v':
            if child_dict.has_key('VOB'):
                postfix += self.complete_e(words, postags, child_dict_list, child_dict['VOB'][0])
            if child_dict.has_key('SBV'):
                prefix = self.complete_e(words, postags, child_dict_list, child_dict['SBV'][0]) + prefix

        return prefix + words[word_index] + postfix

    
    def SementicRoleLabeller(self,input_list,task='srl'):
        '''
        功能：语义角色标注
        返回值：文本中存在角色的每个词的具体的标记列表
        词：[u'\u662f', [{u'type': u'A0', u'end': 1, u'beg': 0, u'id': 0}]]
        '''
        input_xml = self.build_xml(input_list)
        content = self.output_json(task,input_xml)
        rolelabeller_text_list = []
        for text_other in content:
            sent = text_other[0]
            text =[]
            for word in sent:
                if word['arg']!=[]:
                    text.append([word['cont'],word['arg']])
            rolelabeller_text_list.append(text)
        return rolelabeller_text_list





if __name__ == '__main__':
    intput_list = ['中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人']
    model = LTP_MODEL()
    input_sentence = "中国，是以华夏文明为源泉、中华文化为基础，并以汉族为主体民族的多民族国家，通用汉语、汉字，汉族与少数民族被统称为“中华民族”，又自称为炎黄子孙、龙的传人"
    print model.segment(intput_list)
    print model.postagger(intput_list)
    print model.NamedEntityRecognizer(intput_list,Entity_dist=True)[0]['place'][0]
    print model.NamedEntityRecognizer(intput_list)
    print model.SyntaxParser(intput_list)
    head = parent+1
    relation = relate 
    Subjective_guest,Dynamic_relation,Guest,Name_entity_relation = model.triple_extract(input_sentence)
    for e in Subjective_guest[0]:
        print e,
    print "\n"
    for e in Dynamic_relation[0]:
        print e,
    print model.SementicRoleLabeller(intput_list)