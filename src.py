# encoding: utf-8
from asyncore import write
import requests
from lxml import etree
import json
import hashlib
import base64
import hmac
import os
import time
import requests
from urllib.parse import quote_plus

def get_num(srcname):
	vul_num=json.load(open("src.json"))[srcname]
	return vul_num

def get_web_content_ali():
	try:
		url = ""//asrc个人主页（如：https://security.alibaba.com/api/asrc/pub/people.json?&secretUid=e4196ff8cddac7c13b599125cd11dda0）
		header = {
			"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
			"AppleWebKit/537.36 (KHTML, like Gecko) "
							"Chrome/75.0.3770.100 Safari/537.36 "}
		response = requests.request(method="Get", url=url, headers=header)
		json_str=json.loads(response.text)
		num = (str(json_str["data"]["finishedLeakNum"]))
		return num
	except TimeoutError as e:
		return None

def get_web_content():
    try:
        url = ""//tsrc个人主页（如：https://security.tencent.com/index.php/user/p/46259CBEF9A26602E3A7AFF83B44C952）
        header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64)"
            "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/75.0.3770.100 Safari/537.36 "}
        response = requests.request(method="Get", url=url, headers=header)
        result = response.text
        return result
    except TimeoutError as e:
        return None

class Messenger:
    def __init__(self, token=os.getenv("DD_ACCESS_TOKEN"), secret=os.getenv("DD_SECRET")):
        self.timestamp = str(round(time.time() * 1000))
        self.URL = "https://oapi.dingtalk.com/robot/send"
        self.headers = {'Content-Type': 'application/json'}
        secret = secret
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(self.timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        self.sign = quote_plus(base64.b64encode(hmac_code))
        self.params = {'access_token': token, "sign": self.sign}
 
    def send_text(self, content):
        data = {"msgtype": "text", "text": {"content": content}}
        self.params["timestamp"] = self.timestamp
        return requests.post(
            url=self.URL,
            data=json.dumps(data),
            params=self.params,
            headers=self.headers
        )

def tsrcparsing():
    result = get_web_content()
    if result is not None:
        html = etree.HTML(result)
        ii = html.xpath('/html/body/div[2]/div/div[1]/div/div/div[2]/div[1]/p[1]/text()')
        num="".join(str(i) for i in ii).strip()
        print("tsrc: "+num)
        if num!=get_num("tsrc") and num.isdigit():
            m = Messenger(
            token="",
            secret=""//钉钉配置
            )
            m.send_text("tsrc！")
            with open('src.json','a') as tsrctxt:
                old_json=json.load(open("src.json"))
                old_json["tsrc"]=num
                new_json=json.dumps(old_json)
                tsrctxt.truncate(0)
                tsrctxt.write(new_json)
    else:
        raise Exception("Failed to get page information, please check！")
    
    return None

def asrcparsing():
    print("asrc: "+get_web_content_ali())
    if get_web_content_ali()!=get_num("asrc"):
        m = Messenger(
        token="",
        secret=""//钉钉配置
        )
        m.send_text("asrc！")
        with open('src.json','a') as tsrctxt:
            old_json=json.load(open("src.json"))
            old_json["asrc"]=get_web_content_ali()
            new_json=json.dumps(old_json)
            tsrctxt.truncate(0)
            tsrctxt.write(new_json)
if __name__ == "__main__":
    tsrcparsing()
    asrcparsing()
