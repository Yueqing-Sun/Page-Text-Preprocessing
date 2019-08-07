#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from pyltp import Segmentor
import json
import time

LTP_DATA_DIR = 'D:/ltp_data_v3.4.0'  # ltp模型目录的路径
cws_model_path = os.path.join(LTP_DATA_DIR, 'cws.model')  # 分词模型路径，模型名称为`cws.model`

add_punc = ['[', ']', ':', '【', ' 】', '（', '）', '‘', '’', '{', '}', '⑦', '(', ')', '%', '^', '<', '>', '℃', '.', '-',
            '——', '—', '=', '&', '#', '@', '￥', '$']  # 定义要删除的特殊字符


def stopwordslist():
    stopwords = [line.strip() for line in open('stopwords(new).txt', encoding='UTF-8').readlines()]
    stopwords = stopwords + add_punc
    return stopwords


def seg_part(sentence):
    segmentor = Segmentor()  # 初始化实例
    segmentor.load(cws_model_path)  # 加载模型
    words = segmentor.segment(sentence)  # 分词
    # print('\t'.join(words))
    segmentor.release()  # 释放模型
    return '\t'.join(words)


def segment():
    stopwords = stopwordslist()
    with open('D:/news/file_new/segmented.json', 'w', encoding='utf-8') as fin, \
            open('D:/news/file_new/data_new.json', 'r', encoding='utf-8') as fout:
        read_results = [json.loads(line) for line in fout]
        for result in read_results:
            title = seg_part(result['title'])
            titlelist = []
            for item in title.split('\t'):
                if item not in stopwords:
                    if item != '\t':
                        titlelist.append(item)
            text = seg_part(result['parapraghs'])
            textlist = []
            for item2 in text.split('\t'):
                if item2 not in stopwords:
                    if item2 != '\t':
                        textlist.append(item2)
            data = {
                "url": result['url'],
                "segmented_title": titlelist,
                "segmented_parapraghs": textlist,
                "file_name": result['file_name']
            }
            # print(data)
            json_str = json.dumps(data, ensure_ascii=False)
            fin.write(json_str + '\n')


if __name__ == '__main__':
    start = time.time()
    segment()
    end = time.time()
    print('Total time: %.1f s' % (end - start,))
