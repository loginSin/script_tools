#!coding=utf-8

# 检查指定目录下所有 OC .m 文件是否有多余的私有头文件

import os,sys

FILE_SUFFIX=".m" # 文件后缀
KEY_WORD="@interface" # 关键字

def usage():
    print("usage : python %s target_path" % sys.argv[0])

def main(target_path):
	result = get_multi_interface(target_path)
	write_result_to_file(result)


def write_result_to_file(result):
	root_path = os.getcwd()
	file_path = os.path.join(root_path,"check_oc_multi_interface_result.txt")

	f = open(file_path,'w')
	for key in result:
		f.write("%s\n" % key)
		data = result[key]
		for d in data:
			f.write("%s\n" % d)
	f.close()

	print("result will be find at %s" % (file_path)) 	

	pass

def get_multi_interface(target_path):
	result = {}
	for root,dirs,files in os.walk(target_path):
		for name in files:
			file_path = os.path.join(root, name)
			if file_path.find(FILE_SUFFIX) >= len(file_path)-len(FILE_SUFFIX):
				f = open(file_path)
				lines = f.readlines()
				f.close()
				data = []

				for l in lines:
					if KEY_WORD in l:
						data.append(l)
				
				if len(data) > 1:
					print("===================================")
					print(name+"\n")
					for d in data:
						print(d)
					print("===================================")
					result[name] = data

	return result


if __name__ == '__main__':
	arg_len = len(sys.argv)

	target_path = "./"
	if arg_len != 2:
		usage()
		exit()

	target_path = sys.argv[1]

	main(target_path)