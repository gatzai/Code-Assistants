
### 说明
---
奕辅导自动打卡脚本

### 功能
---
* 多用户打卡
* 失败邮箱提醒
* 日志记录

### 代办
---
- [ ] 自动获取token

### 配置文件填写范例
---


```json
{
	"tokens":
	{
		"用户名1": "token1",  //用户名仅仅作为邮件发送标题
		"用户名2": "token2"
	},
	"mail":
	{
		"mail_enable": 0,			  //是否开启邮箱提醒
		"mail_host":"smtp.qq.com", 	  //邮件服务
		"mail_recer": ["xxx@qq.com"], //接收者邮箱
		"mail_pass": "xxxxxx...",	  //发送者邮箱口令
		"mail_sender": "xxx@qq.com"   //发送者邮箱
	}
}
```