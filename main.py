#!/user/bin/env python3
# -*- coding: utf-8 -*-
import re
from hierarchicalDirichletProcess import hdpProcess
from saoBuilder import process_sao
def contains_letter(s):
    # 使用正则表达式检查字符串中是否包含字母
    return bool(re.search('[a-zA-Z]', s))

def read_file(filename):
	with open(filename, 'r', encoding='utf-8') as file:
		text = file.read()
	return text

def read_data():
	titleI = read_file('inputData/Title1.txt')
	AbstractI = read_file('inputData/Abstract1.txt')
	ClaimsI = read_file('inputData/Claims1.txt')
	DescriptionI = read_file('inputData/Description1.txt')
	return titleI,AbstractI,ClaimsI,DescriptionI

def getS_A_O(A_B_C):
	SList = [rowI[0] for rowI in A_B_C]
	AList = [rowI[1] for rowI in A_B_C]
	OList = [rowI[2] for rowI in A_B_C]
	return SList, AList, OList

def getA_B(A_B):
	AList = []
	BList = []
	try:
		for rowI in A_B:
			AList.append(rowI[0])
			BList.append(rowI[1])
	except:
		pass
	return AList, BList

def remove_short_strings(two_d_list):
	return [[s for s in sublist if len(s) > 2] for sublist in two_d_list]

def flatten(two_d_list):
	return [item for sublist in two_d_list for item in sublist]

def sertTopics2(topicsDown2):
	return [["2-" + str(index)] + sublist for index, sublist in enumerate(topicsDown2, start=1)]

def hebin(topicsUp2, topicsDown2):
	hebingZ=[]
	for i in range(len(topicsUp2)):
		try:
			hebingZ.append(topicsUp2[i] + topicsDown2[i])
		except:
			try:
				hebingZ.append(topicsUp2[i])
			except:
				try:
					hebingZ.append(topicsDown2[i])
				except:
					pass
	return hebingZ

def find_string_index(a, bb):
	for index, sublist in enumerate(bb):
		if a in sublist:
			return index
	return -1

def sertTopics3(topicsUp3, topicsDown3, topicsUp2, topicsDown2):
	topicsUpDown2 = hebin(topicsDown2, topicsUp2)
	for indexI in range(len(topicsDown3)):
		for topicI in topicsUp3[indexI]:
			findI = find_string_index(topicI, topicsUpDown2)+1
			if findI > 0:
				topicsDown3[indexI] = ["2-" + str(findI)] + topicsDown3[indexI]
				break
	return topicsDown3

def process1Paper(titleI, AbstractI, ClaimsI, DescriptionI):
	# Process SAO
	SAO_all = process_sao(titleI + '\n' + AbstractI + '\n' + ClaimsI + '\n' + DescriptionI)

	SList, AList, OList = getS_A_O(SAO_all)

	topicsUp3, topicsDown3 = hdpProcess(SList, OList, 2)
	topicsUp2, topicsDown2 = hdpProcess(getA_B(topicsUp3)[0], getA_B(topicsUp3)[1], 2)
	_, topicsDown1 = hdpProcess(getA_B(topicsUp2)[0], getA_B(topicsUp2)[1], 0)

	topicsDown11 = ['1'] + flatten(remove_short_strings(topicsDown1))
	topicsDown22 = sertTopics2(remove_short_strings(topicsDown2))
	topicsDown33 = sertTopics3(topicsUp3, remove_short_strings(topicsDown3), topicsUp2, topicsDown2)

	zong=[]
	for a in topicsDown11:
		if a in zong:
			pass
		else:
			print(a,end=', ')
			if contains_letter(a):
				zong.append(a)
	print()
	print('-' * 50)
	for i in topicsDown22:
		for a in i:
			if a in zong:
				pass
			else:
				print(a, end=', ')
				if contains_letter(a):
					zong.append(a)
		print()
	print('-' * 50)
	for i in topicsDown33:
		for a in i:
			if a in zong:
				pass
			else:
				if a == i[0]:
					print("3-"+a, end=', ')
				else:
					print(a, end=', ')
				if contains_letter(a):
					zong.append(a)
		print()
	print('-' * 50)

if __name__ == '__main__':

	# Read data from input files
	titleI,AbstractI,ClaimsI,DescriptionI = read_data()
	process1Paper(titleI, AbstractI, ClaimsI, DescriptionI)






