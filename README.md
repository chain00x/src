src漏洞通过通知

目前支持asrc，tsrc（如果只需要一个另一个不填即可）

通过src的主页漏洞数，如果漏洞数有变化钉钉通知

有两处需要配置钉钉群机器人

<img width="685" alt="image" src="https://user-images.githubusercontent.com/90015694/205229124-ef1fa2db-840c-490b-b85d-d1fbdf46e3b1.png">

在vps上输入

crontab -e

添加定时任务（src修改为下载下来的文件夹文件路径，一分钟一次）
*/1 * * * * cd src && python3 src.py > src.log
