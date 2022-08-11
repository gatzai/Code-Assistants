#把当前目录下所有文件内容复制到一个目录(hhh)下
import os
from shutil import copyfile

mpath = "./"
uniform_path = "./hhh/"


def travel_f(path):
	for item in os.scandir(path):
		if item.is_dir() and item.name != "hhh":
			travel_f(item.path)
			pass
		elif item.is_file():
			#print(item.name)
			filename = item.name
			if not filename.endswith(".py") and not filename.endswith(".md") and not filename.endswith(".mp4"):
				fpath = uniform_path + filename
				repeat_index = 0
				for i in range(100):
					if os.path.exists(fpath):
						repeat_index = repeat_index + 1
						fpath = uniform_path + str(repeat_index) + filename
						print("repeat: " + fpath)
					else:
						copyfile(item.path, fpath)
						break;

if not os.path.exists(uniform_path):
	os.mkdir(uniform_path)
travel_f(mpath)
