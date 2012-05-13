#!/usr/bin/env python
#coding=utf-8

template = '<option value="%s">%s</option>'

def fromMysql(output):
    lines = output.split('\n')
    for line in lines:
        if line:
             i = line.split()[1]
             # print '__' + line.split('|')[1] + '__'
             print template % (i, i)


if __name__ == '__main__':
    output1 = u'''
|  1-3年       |
|  不限        |
|  3-5年       |
|  1-2年       |
|  2年以上     |
|  1年以上     |
|  4年以上     |
|  5-10年      |
|  3年以上     |
|  无经验      |
|  1年以下     |
|  1-5年       |
|  1-6年       |
|  2-5年       |
|  5年以上     |
|  2-3年       |
|  2-7年       |
|  2-4年       |
|  10年以上    |
|  8年以上     |
|  7年以上     |
|  3-10年      |
|  2-10年      |
|  1-10年      |
|  2年         |
|  1-8年       |
|  3年         |
'''    
    output2 = u'''
|       1000 |
|       1500 |
|       2000 |
|       2001 |
|       3000 |
|       4000 |
|       4001 |
|       5000 |
|       6000 |
|       6001 |
|       8000 |
|       8001 |
|      10000 |
|      10001 |
|      15000 |
'''    

    fromMysql(output2)
    
