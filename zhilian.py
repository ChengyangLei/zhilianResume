#-*- coding:utf-8 -*-
_author_ = 'gyz'
import re

def open_html_file(file_name):
	# 打开html文档的函数，返回文本内容，做下一步匹配
	# 如果文件不存在，则返回 NULL
	all_the_text = ''
	try:
		html_object = open(file_name)
		all_the_text = html_object.read()
		html_object.close()
	except IOError:
		print 'Html File not EXIST!'
		all_the_text = 'NULL'	
	return all_the_text

def find_zhilian_ID(input_content):
	# 这个是简历的ID号，还是比较容易找到的
	pattern = re.compile('<span class="resume-left-tips-id">ID:(.*?)</span>',re.S)
	items = re.findall(pattern,input_content)
	return items[0]

def find_zhilian_personal_INFO(input_content):
	# 从html中提取简历的个人信息栏中的内容
	# 函数返回一个列表，该列表里面有两项
	# 列表的两项都是个人的描述信息，字符串形式
	list_of_person_INFO = []
	# 写一个列表的原因是信息有两行，网页中用<br />隔离开了
	str_1 = '''<div class="summary-top">.*?<span>(.*?)</span>'''
	pattern_1 = re.compile(str_1,re.S)
	items = re.findall(pattern_1,input_content)
	# print items[0]
	info_1 = items[0].replace('&nbsp;',' ')
	list_of_person_INFO.append(info_1.replace('\r\n',''))
	str_2 = '<div class="summary-top">.*?<br />(.*?)</div>'
	pattern_2 = re.compile(str_2,re.S)
	items = re.findall(pattern_2,input_content)
	info_2 = items[0].replace('\t','')
	list_of_person_INFO.append(info_2.replace('\r\n',''))
	# print list_of_person_INFO[0]
	# print list_of_person_INFO[1]
	# print list_of_person_INFO
	final_str = ''
	for i in list_of_person_INFO:
		final_str += i
		final_str +='\n'
	return final_str[:-1]
	# 这个函数写的估计效率低，因为开始打算返回列表，后来又打算返回字符串
	# 这么改就是因为返回字符串后续处理方便
	# 有点影响执行速度，不过反正python执行就很慢，有空再改吧

def find_zhilian_update_time(input_content):
	pattern = re.compile('<strong id="resumeUpdateTime">(.*?)</strong>',re.S)
	items = re.findall(pattern,input_content)
	return items[0]
	pass

def find_zhilian_intention(input_content):
	# 返回一个字符串，字符串按照页面中的格式，每条一行
	# 思路是先找到“求职意向”的一整块内容，再从这一整块内容里面挖出小块的内容
	# 现在先找出整块内容
	# pattern = re.compile('<div class="resume-preview-all">.*?</div>',re.S)
	pattern = re.compile('求职意向</h3>.*?</table>',re.S)
	# .*? 是最小匹配，这里发挥了很好的作用
	items = re.findall(pattern,input_content)
	if not items == []:
		pending_content = items[0]
	else:
		# return ['该用户没有填写“求职意向”栏目。'] 
		# \-> 此处发现一个以前写的bug，现在不返回，返回字符串
		return ['该用户没有填写“求职意向”栏目。']
	# print pending_content
	# pending_content 变量中存储的就是求职意向的内容，现在再从这里面抠出小块的的内容
	# 求职意向内容是个表格，两列
	pattern = re.compile('<td.*?>(.*?)</td>',re.S)
	items = re.findall(pattern,pending_content)
	length = len(items)
	# length 变量存储的是列表的长度
	# print length
	list_of_intention = []
	for i in range(0,length,2):
		# range设置步长为2
		each_str = items[i] + items[i+1]
		# print each_str 
		list_of_intention.append(each_str)
	final_str = ''
	for i in list_of_intention:
		final_str += i
		final_str += '\n'
	return final_str[:-1]
	# 这里用了字符串切片操作，去掉了最后一个'\n'

def find_zhilian_self_evaluation(input_content):
	# !!有些简历没有自我评价
	# 该函数用来找自我评价部分，返回一个字符串
	# 字符串按照页面中的格式，每条一行
	# 思路与判断求职意向类似，先找大块内容，再从表格里面找
	# pattern = re.compile('<div class="resume-preview-all">.*?</div>',re.S)
	pattern = re.compile('自我评价</h3>.*?<div class="resume-preview-all">',re.S)
	# .*? 是最小匹配
	items = re.findall(pattern,input_content)
	if not items == []:
		pending_content = items[0]
	else:
		pending_content = ''
	# print pending_content
	# 下面该找小块的内容了
	# 其实这里的程序还可以更佳简化的！！！
	# 现在的程序可以实现功能，简化有空再说吧
	pattern = re.compile('</h3>.*?<div.*?>(.*?)</div>',re.S)
	if not items == []:
		items = re.findall(pattern,pending_content)
		self_evaluation = items[0].replace('<br />','\n')
	else:
		self_evaluation = '该用户没有填写“自我评价”栏目。'
	# print self_evaluation
	return self_evaluation
	pass

def find_zhilian_work_experience(input_content):
	# 这个函数用来找到工作经历的内容
	# 从这个栏目开始都要考虑加入没找到的情况了
	final_str = ''
	pattern = re.compile('工作经历</h3>.*?<div class="resume-preview-all">',re.S)
	items = re.findall(pattern,input_content)
	if not items == []:
		pending_content = items[0]
	else:
		return '该用户没有填写“工作经历”栏目。'
	# print pending_content
	# 这里pending_content 是工作经历的全部内容，下面需要从 pending_content中抽取每一次工作经历
	pattern = re.compile('<h2>.*?</table>',re.S)
	# 我发现项目经历那里，也可以用<h2>到</table>这种方式来匹配！-> 3/10/2016
	list_of_experience = re.findall(pattern,pending_content)
	# print len(list_of_experience) ＃代表有几段个人经历
	# print list_of_experience[0]
	for each_experience in list_of_experience:
		# 找 <h2>
		tmp_pattern = re.compile('<h2>(.*?)</h2>',re.S)
		tmp_items = re.findall(tmp_pattern,each_experience)
		final_str += (tmp_items[0].replace('&nbsp;',' ') + '\n')
		# 找 <h5>
		tmp_pattern = re.compile('<h5>(.*?)</h5>',re.S)
		tmp_items = re.findall(tmp_pattern,each_experience)
		final_str += (tmp_items[0].replace('&nbsp;',' ') + '\n')
		# 找 工作描述
		final_str += '工作描述：\n'
		tmp_pattern = re.compile('工作描述.*?<td>(.*?)</td>',re.S)
		tmp_items = re.findall(tmp_pattern,each_experience)
		tmp_str = tmp_items[0].replace('<br />','\n')
		final_str += (tmp_str.replace('&nbsp;',' ') + '\n\n')
	# print final_str
	return final_str[:-2]
	pass


def find_zhilian_project_experience(input_content):
	# 本函数来查找项目经历的内容
	# 并不是每份简历中，都有项目经历的内容
	# 思路也是先挖出大块，再找小块，和上面的一样 -> 3/22/2016
	final_str = ''
	pattern = re.compile('项目经历</h3>.*?<div class="resume-preview-all">',re.S)
	items = re.findall(pattern,input_content)
	if not items == []:
		pending_content = items[0]
	else:
		return '该用户没有填写“项目经历”栏目。'
	# print pending_content
	pattern = re.compile('<h2>.*?</table>',re.S)
	list_of_experience = re.findall(pattern,pending_content)
	# print list_of_experience[5] # For Test
	# len(list_of_experience) -> 代表有几段个人经历
	for each_experience in list_of_experience:
		# 找 <h2>
		tmp_pattern = re.compile('<h2>(.*?)</h2>',re.S)
		tmp_items = re.findall(tmp_pattern,each_experience)
		final_str += (tmp_items[0].replace('&nbsp;',' ') + '\n')
		# 找 责任描述
		tmp_pattern = re.compile('责任描述.*?</td>.*?<td>(.*?)</td>',re.S)
		tmp_items = re.findall(tmp_pattern,each_experience)
		final_str += '责任描述：\n'
		final_str += (tmp_items[0].replace('&nbsp;',' ') + '\n')
		# 找 项目描述
		tmp_pattern = re.compile('项目描述.*?</td>.*?<td>(.*?)</td>',re.S)
		tmp_items = re.findall(tmp_pattern,each_experience)
		final_str += '项目描述：\n'
		tmp_str = tmp_items[0].replace('<br />','\n')
		final_str += (tmp_str.replace('&nbsp;',' ') + '\n\n')
	# print final_str
	return final_str[:-2]
	pass


def main():
	html_content = open_html_file('example/1.html')
	resume_ID = find_zhilian_ID(html_content)
	person_INFO = find_zhilian_personal_INFO(html_content)
	resume_update_time = find_zhilian_update_time(html_content)
	intention = find_zhilian_intention(html_content)
	self_evaluation =find_zhilian_self_evaluation(html_content)
	work_experience = find_zhilian_work_experience(html_content)
	project_experience = find_zhilian_project_experience(html_content)

	#下面是打印到屏幕的部分
	print '简历ID：\n'+resume_ID 
	print '\n个人信息：\n'+person_INFO
	print '\n简历更新时间：\n' + resume_update_time
	print '\n求职意向:\n' + intention
	print '\n自我评价：\n'+ self_evaluation
	print '\n工作经历：\n' + work_experience
	print '\n项目经历：\n' + project_experience

	# 这里是测试板块
	
	



if __name__ == '__main__':
	main()
