import requests,json
#进入扇贝单词量测试页面后打开F12查看XHR文档，获取选择level界面的json数据连接
link = requests.get('https://www.shanbay.com/api/v1/vocabtest/category/')
js_link = json.loads(link.text)
print(js_link)
bianhao = int(input('''请输入你选择的词库编号，按Enter确认
1，GMAT  2，考研  3，高考  4，四级  5，六级
6，英专  7，托福  8，GRE  9，雅思  10，任意
>'''))
ciku = js_link['data'][bianhao-1][0]
#print (ciku)
#根据用户选择获取相应level单词的json数据
link2 = requests.get('https://www.shanbay.com/api/v1/vocabtest/vocabularies/?category=' + ciku)
js_link2 = json.loads(link2.text)
#print(js_link2['data'][0]['content'])

print ('测试现在开始。如果你认识这个单词，请输入Y，否则直接敲Enter：')
n = 0
count_know = 0
know = []
know_index = []
not_know = []
for x in js_link2['data']:
    n = n + 1
    answer = input('\n' + '第'+ str(n) + '个单词是' + x['content'] + ', 是否认识?Y/N: ').upper()
    if answer == 'Y':
        know.append(x['content'])
        know_index.append(n-1)
        count_know += 1
    else:
        not_know.append(x['content'])
print('在刚才测试的'+ str(len(js_link2['data'])) + '个单词中，有' + str(count_know) +'个是你觉得认识的它们是：\n')

for d in know:
    print(d)

print('接下来我们来检测一下你是否真的认识这些单词，请从A，B，C，D中选择单词正确的意思')

zimu = ['A', 'B', 'C', 'D']
correct_num = 0
wrong_word = []
for i in know_index:
    print('\n'+js_link2['data'][i]['content'] + '\n')
    meaning =  js_link2['data'][i]['definition_choices']
    correct =  js_link2['data'][i]['pk']
    alpha = 0
    pk_dict = dict()
    for mean in meaning: 
        print(zimu[alpha] + ': '+ mean['definition'] + '\n')
        pk_dict[zimu[alpha]] = mean['pk']
        alpha += 1
    try:
        answer2 = input('请选择：').upper()
        #自动将输入内容变为大写
        if pk_dict[answer2] == correct:
            correct_num += 1
            print('回答正确')
        else:
            print('回答错误')
            wrong_word.append(js_link2['data'][i]['content'])
    except KeyError: 
        #防止用户输入ABCD以外的内容而报错
        print('回答错误')
        wrong_word.append(js_link2['data'][i]['content'])
        

#结果反馈
print ('\n现在，到了公布成绩的时刻:')
print ('在'+str(len(js_link2['data']))+'个'+js_link['data'][bianhao-1][1]+'词汇当中，你认识其中'+str(count_know)+'个，实际掌握'+str(correct_num)+'个，错误'+str(len(wrong_word))+'个。')

#保存至生词本
is_save = input('是否将生词保存至生词本？Y/N：').upper()
if is_save == 'Y':
    with open('生词本.txt', 'w', encoding = 'utf-8') as f:
        f.write('不认识的单词有：\n')
        for word in not_know:
            f.write(word + '\n')
        f.write('记错的单词有： \n')
        for wrong in wrong_word:
            f.write(wrong + '\n')
else:
    print('下次见')
