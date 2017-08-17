# API接口文档 

## 认证模块
* 登陆接口
	* 请求地址：/api/login/
	* 请求方式：POST
	* 请求参数：
	
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		username    | string | 账号 | 1
		password    | string | 密码 | 5
	* 返回值：

			```
   			{
   				'c': 0,
   				'm': '',
   				'd': {'redirect_url': 'xxxxx'}
   			}
	   		```

* 退出接口
	* 请求地址：/api/logout/
	* 请求方式：POST
	* 请求参数：无
	* 返回值：HTTP跳转

## 日程表模块
* 日程列表接口
	* 请求地址：/api/schedules/ 
	* 请求方式：GET 
	* 请求参数：
    
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		p    | int | 页码 | 1
		n    | int | 每页数量 | 5
	* 返回参数
	
		```sql
		{
			'c': 0,
			'm': '',
			'd': [
				{
					'id': 1,
					'stype': 'keepfit',
					'subject': 'XXXXXX',
					'sdate': '2017-08-18',
					'created_at': '2017-08-18 10:10:10',
					'update_at': '2017-08-18 12:12:12',
					'targets': [
						{'content': 'XXXXX', 'done': 0},
						{'content': 'XXXXX', 'done': 1},
						...
					]
				},
				...
			]
		}
		```
		
*  日程创建接口
	* 请求地址：/api/schedule/new/
	* 请求方式：POST
	* 请求参数
	
		名称 | 类型 | 说明 | 默认值
       --- | ----| -----|-----
       stype| string | 日程类型 | 无
       sdate | string | 日程需处理的日期 | 无
       subject | string | 日程主题 | 无
       targets | json字串 ``` [{'content':'xxxx', done: 0}, ...] ```| 日程事件| 无	
	       
   * 返回值：

   		```
   			{
   				'c': 0,
   				'm': '',
   				'd': {'id': 1}
   			}
   		```
	   		
* 日程删除接口
	* 请求地址：/api/schedule/:id/delete/
	* 请求方式：POST
	* 请求参数： 无
	* 返回值：
		
		```
   			{
   				'c': 0,
   				'm': '',
   				'd': {'id': 1}
   			}
   		```
* 日程更新接口
	* 请求地址：/api/schedule/:id/update/
	* 请求方式：POST
	* 请求参数：
	
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		stype    | string | 日程类型 | 无
		sdate    | string | 日程处理的日期 | 无
		subject  | string | 日程主题 | 无
		targets  | json字串 ``` [{'content':'xxxx', done: 0}, ...] ```| 日程具体事项 | 无
		
* 日程详情接口
	* 请求地址：/api/schedule/:id/
	* 请求方式：GET
	* 请求参数：无
	* 返回值：
		
		```sql
		{
			'c': 0,
			'm': '',
			'd': {
				'id': 1,
				'stype': 'keepfit',
				'subject': 'XXXXXX',
				'sdate': '2017-08-18',
				'created_at': '2017-08-18 10:10:10',
				'update_at': '2017-08-18 12:12:12',
				'targets': [
					{'content': 'XXXXX', 'done': 0},
					{'content': 'XXXXX', 'done': 1},
					...
				]
			}
		}
		```

* 日程配置详情接口
	* 请求地址：/api/schedule/:schedule_id/configs/
	* 请求方式：GET
	* 请求参数：无
	* 返回值：
		
		```sql
		{
			'c': 0,
			'm': '',
			'd': [
				{
					'id': 1,
					'schedule_id': 1,
					'key': 'XXXXX',
					'value': 'XXXXXX'
				},
				...
			]
		}
		```
		
* 日程配置创建接口
	* 请求地址：/api/schedule/:schedule_id/config/new/
	* 请求方式：POST
	* 请求参数：
		
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		key    | string | 日程配置类型 | 无
		value    | string | 配置值 | 无
	* 返回值：
	
		```sql
		{
			'c': 0,
			'm': '',
			'd': {
				'id': 1,
				'schedule_id': 1
			}
		}
		```
		
* 日程配置更新接口
	* 请求地址：/api/schedule/:schedule_id/config/:id/update/
	* 请求方式：POST
	* 请求参数：
		
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		key    | string | 日程配置类型 | 无
		value    | string | 配置值 | 无
	* 返回值：
		
		```sql
		{
			'c': 0,
			'm': '',
			'd': {
				'id': 1,
				'schedule_id': 1
			}
		}
		```

* 日程配置删除接口
	* 请求地址：/api/schecule/:schedule_id/config/:id/delete/
	* 请求方式：POST
	* 请求参数：无
	* 返回值：
	
		```sql
		{
			'c': 0,
			'm': '',
			'd': {
				'id': 1,
				'schedule_id': 1
			}
		}
		```

## 代码备忘录模块
* 代码备忘录列表接口
	* 请求地址：/api/code-memo/codes/
	* 请求方式：GET
	* 请求参数：
	
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		p    | int | 页码 | 1
		n    | int | 每页数量 | 10
	* 返回值：
	
		```javascript
			{
				'c': 0,
				'm': '',
				'd': [
					{
						'id': 1,
						'ctype': 'linux',
						'description': 'XXXXX',
						'content': 'XXXXXX'
					}
				]
			}
		```
		
* 代码备忘录创建接口
	* 请求地址：/api/code-memo/new/
	* 请求方式：POST
	* 请求参数：
		
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		ctype    | string | 类型 | 无
		description    | string | 代码的简单描述 | 无
		content  | string | 代码OR命令 | 无
	* 返回值：
	
		```sql
			{
				'c': 0,
				'm': 'XXXXX',
				'd': {'id': 1}
			}
		```

* 代码备忘录更新接口
	* 请求地址：/api/code-memo/:id/update/
	* 请求方式：POST
	* 请求参数：
		
		名称  | 类型 | 说明 | 默认值
		-----| ----| ---- | ----
		ctype    | string | 类型 | 无
		description    | string | 代码的简单描述 | 无
		content  | string | 代码OR命令 | 无
	* 返回值
	
		```sql
			{
				'c': 0,
				'm': 'XXXXX',
				'd': {'id': 1}
			}
		```

* 代码备忘录删除接口
	* 请求地址：/api/code-memo/:id/delete/
	* 请求方式：POST
	* 请求参数：无
	* 返回值：
	
		```sql
			{
				'c': 0,
				'm': 'XXXXX',
				'd': {'id': 1}
			}
		```