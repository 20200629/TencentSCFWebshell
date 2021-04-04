# -*- coding:utf-8 -*-
import json
import requests
from urllib.parse import urlsplit 
from qcloud_cos_v5 import CosConfig
from qcloud_cos_v5 import CosS3Client
from qcloud_cos_v5 import CosServiceError

secret_id = ''     # 替换为用户的secret_id
secret_key = ''     # 替换为用户的secret_key
region = 'ap-guangzhou'    # 替换为用户的region
token = None               # 使用临时密钥需要传入Token，默认为空,可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)  # 获取配置对象
client = CosS3Client(config)
bucket =''





def geturl(urlstr):
    jurlstr = json.dumps(urlstr)
    dict_url = json.loads(jurlstr)
    return dict_url['u']



def FileExistsBool(host):
    # 获取存储桶下文件名包含marker的文件列表
    resp = client.list_objects(
         Bucket=bucket)
    flag = host in json.dumps(resp)
    return flag

def write_session(target,temp=b'{"a":"b"}'):

    response = client.put_object(
        Bucket=bucket,
        Body= temp,
        Key=target+".txt"
    )
    return response

def get_gession(target):
    response = client.get_object(
    Bucket=bucket,
    Key=target+".txt",
    ResponseContentType='text/html; charset=utf-8'
)
    fp = response['Body'].get_raw_stream()
    return fp.readline()

def handler (event, context):
    
    #godzilla add cookies
    #antsword just do it
    #to do behinder
    url = geturl(event['queryString'])
    host = urlsplit(url).netloc
    if "body" in event:
        postdata=event['body']
    else:
        postdata="f=1"
    headers=event['headers']
    headers["HOST"] = host
    flag = FileExistsBool(host)
    #如果有cookie则不进行这一步
    if(not flag):
        s = requests.session()
        s.get(url)
        cookies = s.cookies
        write_session(host,json.dumps(cookies.get_dict()).encode())
    else:
        cookies=json.loads(str(get_gession(host),encoding="utf-8"))
    resp=requests.post(url,data=postdata,headers=headers,cookies=cookies,verify=False)
    response={
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html;charset=ascii;'+json.dumps(cookies)} ,
        "body": resp.text
    }

    return response
