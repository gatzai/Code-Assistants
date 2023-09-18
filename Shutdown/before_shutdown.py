import subprocess
import os
import datetime
#import requests
import socket

content_dir = 'D:/Projects/GitRepo/Notes/knowledge2.0'
#content_dir = 'D:\\Projects\\GitRepo\\Code-Assistants'

def is_net_on():
	host = 'www.baidu.com'
	port = 80
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(5)
	neton = False
	try:
		s.connect((host, port))
		print('connect success')
		neton = True
	except socket.error as e:
		print('connect fail')
	finally:
		s.close()
	return neton

def run():
	os.chdir(content_dir)
	#git_root = subprocess.run(['git', 'rev-parse', '--show-toplevel'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
	#print(git_root)
	updated_files = subprocess.run(['git', 'diff', '--name-only'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
	print(updated_files)
	cur_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if updated_files:
		subprocess.run(['git', 'pull'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
		subprocess.run(['git', 'add', '.'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
		subprocess.run(['git', 'commit', '-m','[auto_update]'+cur_time], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
	# 有网才能push
	if is_net_on():
		subprocess.run(['git', 'push'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
	#os.system('dir')

if __name__ == "__main__":
	run()
