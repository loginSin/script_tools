#coding=utf-8

#检查给定目录下超过 MAX_LINE 个数的 .m 文件

import sys,os

FILE_SUFFIX=".m"
MAX_LINE=500
RED_PREFIX="\033[1;31m"
RED_SUFFIX="\033[0m"

def usage():
	print("usage : python %s target_path" % sys.argv[0])

def check_code(target_path):
	if not os.path.isdir(target_path):
		print("not a path : %s" % target_path)
		exit()

	#输出超过 MAX_LINE 的结果，并返回
	result = check_result(target_path)
	
	#将结果写入特定文件
	write_result_to_file(result)


def check_result(target_path):
	print("===================================")
	result = {}
	for root,dirs,files in os.walk(target_path):
		for name in files:
			file_path = os.path.join(root, name)
			if file_path.find(FILE_SUFFIX) >= len(file_path)-len(FILE_SUFFIX):
				f = open(file_path)
				num_of_lines = len(f.readlines())
				f.close()
				file_name = os.path.basename(file_path)
				if num_of_lines > MAX_LINE:
					print("%s \t %s %d %s" % (file_name,RED_PREFIX,num_of_lines,RED_SUFFIX))
					result[file_path] = str(num_of_lines)
	print("===================================")

	return result

def write_result_to_file(result):
	root_path = os.getcwd()
	file_path = os.path.join(root_path,"check_code_result.txt")

	f = open(file_path,'w')
	for key in result:
		f.write("%s \t %s \n" % (key,result[key]))
	f.close()

	print("result will be find at %s %s %s" % (RED_PREFIX,file_path,RED_SUFFIX))

if __name__ == '__main__':
	arg_len = len(sys.argv)

	target_path = "./"
	if arg_len == 1 or arg_len > 2:
		usage()
		exit()

	if arg_len == 2:
		target_path = sys.argv[1]
		
	check_code(target_path)
