import requests
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import logging

#签到表单
def get_post_data(qid):
	post_data = {
		"questionnairePublishEntityId": qid,
		"answerInfoList": [
		{
			"subjectId": "1001635817858477001050000000001",
			"subjectType": "multiSelect",
			"multiSelect": {
			"optionAnswerList": [
			{
				"beSelectValue": "NotThing",
				"fillContent": ""
			}
			]
			}
		},
		{
			"subjectId": "1001635817858481001050000000001",
			"subjectType": "location",
			"location": {
			"deviationDistance": 2178,
			"locationRangeId": "1001638329492314001090000000001",
			"address": "长沙市岳麓区人民政府(含光路)",
			"city": "长沙市",
			"province": "湖南省",
			"area": "岳麓区",
			"latitude": 28.23529,
			"longitude": 112.93134,
			"street": "望岳街道"
			}
		},
		{
			"subjectId": "1001637746058450004920000000001",
			"subjectType": "signleSelect",
			"signleSelect": {
			"beSelectValue": "1",
			"fillContent": ""
			}
		},
		{
			"subjectId": "1001647263047076012720000000001",
			"subjectType": "simpleFill",
			"simpleFill": {
			"inputContent": "36.7",
			"imgList": []
			}
		}
		]
	}
	return post_data

#请求头
def get_header_with_token(token):
	header = {
		'Content-Type': 'application/json',
		'accessToken': '',
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6500',
		'referer': 'https://servicewechat.com/wx217628c7eb8ec43c/104/page-frame.html',
		'Connection': 'keep-alive',
		'Host': 'yfd.ly-sky.com',
		'Sec-Fetch-Mode': 'cors',
		'Sec-Fetch-Site': 'cross-site',
		'Sec-Fetch-Dest': 'empty',
		'xweb_xhr': '1',
		'userAuthType': 'MS',
		'Accept-Language': 'zh-CN,zh',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept': '*/*'
	}
	header['accessToken'] = token
	return header

# 第三方 SMTP 服务

class MailSender:
	def __init__(self,mail_host, mail_pass, sender, receivers = []):
		self.mail_host = mail_host
		self.mail_pass = mail_pass
		self.receivers = receivers
		self.sender = sender

	def sendMail(self, subject='Title', content='Content'):
		'''
		@param:
		receivers	list	邮件接收方的邮箱列表， eg. ['****@qq.com', '*****@163.com']
		subject		str		发送的邮件主题
		content		str		发送的邮件内容 
		'''
		sender = self.sender
		message = MIMEText(content, 'plain', 'utf-8')
		message['From'] = Header("yfd_attendance", 'utf-8')
		message['To'] =  Header("Manager", 'utf-8')
		
		message['Subject'] = Header(subject, 'utf-8')
		
		
		try:
		    smtpObj = smtplib.SMTP()
		    smtpObj.connect(self.mail_host, 25)    # 25 为 SMTP 端口号
		    smtpObj.login(self.sender,self.mail_pass)
		    smtpObj.sendmail(sender, self.receivers, message.as_string())
		    print("邮件发送成功")
		except smtplib.SMTPException:
		    print("Error: 无法发送邮件")

def read_user_config():
	with open('user_config.json', encoding = 'utf-8') as f:
		users_token = json.load(f)
	return users_token

def init():
	LOG_FORMAT = '[%(asctime)s][%(levelname)s][- %(message)s]'
	logging.basicConfig(filename='attendance.log',level=logging.DEBUG, format = LOG_FORMAT)

def run():
	user_config = read_user_config()
	users_token = user_config['tokens']
	mail_enable = user_config['mail']['mail_enable']
	if mail_enable:
		mail_host = user_config['mail']['mail_host']
		mail_recer = user_config['mail']['mail_recer']
		mail_pass = user_config['mail']['mail_pass']
		mail_sender = user_config['mail']['mail_sender']
		mailsender = MailSender(mail_host, mail_pass, mail_sender, mail_recer)
	url = 'https://yfd.ly-sky.com/ly-pd-mb/form/api/answerSheet/saveNormal'
	url_id = 'https://yfd.ly-sky.com/ly-pd-mb/form/api/healthCheckIn/client/student/indexVo'
	
	for k,v in users_token.items():
		header = get_header_with_token(v)
		#获取当天问卷 id
		res_id = requests.get(url_id, headers=header, verify=False)
		res_id_j = json.loads(res_id.text)
		qid = res_id_j['data']['questionnairePublishEntityId']
		#print(qid)

		#修改请求头，并发送签到表单
		header['Content-Length'] = '845'
		post_data = get_post_data(qid)
		res = requests.post(url, data=json.dumps(post_data),headers=header, verify=False)
		res_j = json.loads(res.text)
		code = res_j['code']
		if code != 200:
			#print('[Error]Request Error! Ready to send email')
			err_title = k + "签到失败，错误码：" + str(code)
			logging.error(err_title + ',' + res.text)
			if mail_enable:
				mailsender.sendMail(err_title, res.text)
			break # 只要一个失败了后面就不继续了
		else:
			#print('Attendence Success')
			success_info = k + "," + res.text
			#print(success_info)
			logging.info(success_info)


if __name__ == "__main__":
	init()
	run()