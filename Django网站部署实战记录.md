# Django网站部署记录（Apache+mod_wsgi）

踩坑无数，但总算是又掌握了一门技能

## 0.  环境以及软件版本

- ubantu 16.04
- python 3.5.2
- django 1.11.3
- apache 2.4.18


## 1.  安装软件

下载apache并检查版本

`sudo apt-get install apache2`
`apachectl -v` 

下载mod_wsgi建立apache与django的联系（看清楚自己python版本下载）

 `sudo apt-get install libapache2-mod-wsgi      #Python2`
 `sudo apt-get install libapache2-mod-wsgi-py3  #Python3`

安装pip

`sudo apt install python-pip  # python2`		

`sudo apt install python3-pip # python3`		

安装django

`sudo pip3 install django`

## 2.  建立Django与Apache联系

具体来说，分为以下四步：

1. 将django项目放在/var/www/目录下

2. 修改apache虚拟主机配置文件

3. 配置文件生效

4. 重启apache服务

5. 修改Django的wsgi.py文件

   ​

   **重要事情说三遍**

   **以下配置中{$~~~ $}的内容请根据自己项目填,如果权限不够记得加sudo**

`apache默认网站目录是/var/www/`

### 上传项目

#### git：

`cd /var/www/`
`git clone {yourproject}`

#### ftp + cp：

先通过ftp将项目传输到服务器上个人目录，之后通过cp命令将其复制到目的路径

或者直接用ftp将项目穿到目的路径（权限比上一条要高）

`cp -Rf  源路径  目的路径`

### 修改Apache配置文件

####  Apache默认目录结构

```
# /etc/apache2/
# |-- apache2.conf
# | `-- ports.conf
# |-- mods-enabled
# | |-- *.load
# | `-- *.conf
# |--mods-available
# |-- conf-enabled
# | `-- *.conf
# `-- sites-enabled
# `-- *.conf
#|--site-available
#|--site-enabled
```

#### 在site-available中新建自己项目的配置文件

`sudo vi /etc/apache/site-available/{$projectname$}.conf`

添加以下信息（按实际情况修改）

```bash
<VirtualHost *:80>
#默认监听80端口
ServerName www.yourdomain.com 
#servername 填自己的域名或者ip
#ServerAlias otherdomain.com
#ServerAdmin youremail@gmail.com 

# 存放用户上传图片等文件的位置，注意去掉#号
#Alias /media/ /var/www/{$ProjectName$}/media/ 

# 静态文件(js/css/images)的存放位置
Alias /static/ /var/www/{$ProjectName$}/static/                

# 允许通过网络获取static的内容
<Directory /var/www/{$ProjectName$}/static/>                  
    Require all granted
</Directory>

# 最重要的！通过wsgi.py让Apache识别这是一个Django工程，别漏掉前边的 /
WSGIScriptAlias / /var/www/{$ProjectName$}/{$ProjectName$}/wsgi.py     
# wsgi.py文件的父级目录，第一个ProjectName为Django工程目录，第二个ProjectName为Django自建的与工程同名的目录
<Directory /var/www/{$ProjectName$}/{$ProjectName$}/>                  
<Files wsgi.py>
    Require all granted
</Files>
</Directory>

</VirtualHost>

作者：寒夏凉秋
链接：https://www.jianshu.com/p/b9d7e1f0e97b
來源：简书
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。
```

#### 编辑apache中的wsgi.conf文件

```
vi /etc/apache2/mods-available/wsgi.conf
#在文件中添加以下行:
WSGIPythonPath /var/www/{$projectname$} #项目所在地址
```

#### 激活配置文件

`sudo a2ensite /etc/apache2/ sites-available/{$projectname$}.conf`

#### 重启Apache服务

`service apache2 reload`

#### 修改Django 项目的wsgi.py

`vi /var/www/{$projectname$}/{$projectname$}/wsgi.py`

其实要增加的也就#1.#2.#3 3行代码

```python
import os
from os.path import join,dirname,abspath	#1.
    PROJECT_DIR = dirname(dirname(abspath(__file__)))	#2.

import sys
    sys.path.insert(0,PROJECT_DIR)	#3.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "examsys.settings")

from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

```

##  3. 查看运行情况

用浏览器访问你设置的域名或者IP地址查看网站

不行的话，重启Apache服务，看看情况

`service apache2 reload`

##  4. 调试错误

1. Apache无法restart或者reload

   1. 按照提示输入：`systemctl status apache2.service`
   2. 查看错误信息，一定要有耐心，根据错误信息搜索解决办法
   3. 一般是项目配置文件`{$projectname$}.conf` 某行出错

2. 模块未安装 No Module named xxxx

   1. **No module named xxxx** 依赖库没安装完整,请pip安装一波

   2. **No module named django**或者其他含django的错误。这说明你的环境搭错了。往上翻error.log，找到AH00489开头的错误，看看你到底用的是什么环境。一般都是你第二步Apache的Python解释器安装错误

   3. 查看Apache的错误文档

      ​	`cat /var/log/apache2/error.log`

   4. 我遇到的一个问题

      ​	我的项目用到了mysql，提示没有mysqlDB,需要安装mysqlclient，然后在运行

      ​	`pip3 install mysqlclient`的时候失败

      ​	解决方法：`sudo apt-get install libmysqlclient-dev`

3. Django自带的admin页面无法加载css文件

   1. 修改Django项目中project/setting.py文件

      ​	`STATIC_ROOT={$static文件夹的根目录$}`

      ​	比如我的static目录在 /var/www/music/ , 即修改如下：

      ​	`STATIC_ROOT= /var/www/music/static/`

      ​	`STATIC_URL =  /static/`

   2. 收集静态文件

      ​	`python  manage.py collectstatic      #python2`
      ​	`python3  manage.py collectstatic     #python3`

      会在你的static文件夹中生成admin文件夹,
      问题如果还不解决,请去apache/site-available/project.conf中查看 static配置路径是否正确

4. 数据库显示只读

   1. 如这样
      `sqlite3.OperationalError: attempt to write a readonly database`

      解决办法:
      因为我用python自带的sqlite3数据库
      将数据库权限设置为www-data

      ```
      sudo chgrp www-data project
      sudo chmod g+w blog
      sudo chgrp www-data project/db.sqlite3  # 更改为你的数据库名称
      sudo chmod g+w project/db.sqlite3
      ```

5. template文件无法读取

   ​	在setting.py文件中
   ​	template设置选项中	指明绝对路径	

6. 使用域名或者公网IP的设置后无法访问

   在setting.py中修改allow_host选项：

   ​	`ALLOW_HOST=['{$你的域名或者IP$}']`

   或者

   ​	`ALLOW_HOST=['*']`



## 5.  导入执行mysql文件

​	两种方式：

		>mysql -u root -p -D test < E:\test.sql

//mysql -u账号 -p密码 -D数据库名 < sql文件绝对路径

> 进入MySQL，切换数据库，执行：
>
> source sql文件路径
>
> 例如 ：source E:\test.sql