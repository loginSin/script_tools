#coding=utf-8

#该脚本用来检查某个 ipa 包的过期时间，并生成以过期时间为名的 txt 放到指定目录

import sys,os,shutil,zipfile

def check_ipa(fp,target_path):
	root_path = os.getcwd()

	#1.把目标路径的 ipa copy 到当前路径
	copy_file_to_current_path(fp,root_path)

	#2.把当前路径的 ipa 重命名为 zip
	target_file = rename_file_at_current_path(fp,root_path)

	#3.解压 zip
	unzip_file(target_file)

	#4.打印 .app 中的证书过期时间
	expiration_date = print_expiration_date(root_path)

	#5.删除 2，3 步产生的临时文件
	remove_temp_file(root_path,target_file)

	#6.创建以过期时间为名的文件
	create_expiration_date_file(root_path,expiration_date,target_path)


def copy_file_to_current_path(src_dir,target_dir):
	shutil.copy(src_dir,target_dir)
	print("copy %s to %s " % (src_dir,target_dir))

def rename_file_at_current_path(fp,root_path):
	file_full_name = os.path.basename(fp)
	file_name = os.path.splitext(file_full_name)[0]
	origin_file = os.path.join(root_path,file_full_name)
	target_file = os.path.join(root_path,file_name+'.zip')
	os.rename(origin_file,target_file)
	print("rename %s to %s" % (origin_file,target_file))
	return target_file

def unzip_file(target_file):
	print("unzip %s to ./temp/" % target_file)
	f = zipfile.ZipFile(target_file,'r')
	for file in f.namelist():
		f.extract(file,"temp")

def print_expiration_date(root_path):
	# temp/Payload/RongEnterpriseApp.app/embedded.mobileprovision
	sep = os.path.sep
	cer_path = os.path.join(root_path,"temp"+sep+"Payload"+sep+"RongEnterpriseApp.app"+sep+"embedded.mobileprovision")
	print("check expiration date in %s" % cer_path)
	f = open(cer_path,'r')
	expiration_date = ""
	flag = 0
	for line in f.readlines():
		if flag == 1:
			expiration_date = line
			break

		if line.find("ExpirationDate") >= 0:
			flag = 1

	f.close()
	expiration_date = expiration_date.replace("<date>","ExpirationDate").replace("</date>","").strip()
	print("===============================================")
	print("该安装包的过期时间为:")
	print("%s" % expiration_date)
	print("===============================================")

	return expiration_date

def remove_temp_file(root_path,target_file):
	os.remove(target_file)
	temp_path = os.path.join(root_path,"temp")
	for root,dirs,files in os.walk(temp_path):
		for name in files:
			del_file = os.path.join(root,name)
			os.remove(del_file)
	shutil.rmtree(temp_path)
	print("remove %s" % target_file)
	print("remove %s" % temp_path)

def create_expiration_date_file(root_path,expiration_date,target_path):
	# f = open(os.path.join(root_path,expiration_date+".txt"),'rw')
	txt_file = expiration_date+".txt"
	f = open(txt_file,'w')
	f.close()
	shutil.move(os.path.dirname(txt_file),target_path)


def useage():
	print("python %s source_file_path target_path" % sys.argv[0])
	exit()

if __name__ == '__main__':
	arg_len = len(sys.argv)
	print(arg_len)
	if arg_len < 2:
		useage()

	target_path = os.getcwd()
	if arg_len < 3:
		pass

	if arg_len == 3:
		target_path = os.argv[2]

	fp = sys.argv[1]
	check_ipa(fp,target_path)