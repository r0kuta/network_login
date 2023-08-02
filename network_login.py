import requests
import time
import logging
import execjs
import codecs

def main():

    # 创建一个日志记录器
    logger = logging.getLogger('network_login')
    logger.setLevel(logging.INFO)

    # 创建一个输出到文件的日志处理程序
    file_handler = logging.FileHandler('network_login.log') #文件路径注意修改
    file_handler.setLevel(logging.DEBUG)

    # 创建一个格式化程序，并将其添加到处理程序
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler.setFormatter(formatter)

    # 将处理程序添加到日志记录器
    logger.addHandler(file_handler)


    number = '' #学号
    password = '' #密码
    ps=1
    pid='2'
    calg='12345678'
    
    js_file = "a41.js"  #文件路径注意修改
    with codecs.open(js_file, "r", "utf-8") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)

    upass = ctx.call('calcMD5', pid+password+calg ) #调用js的calcMD5函数
    upass = upass+calg+pid #根据js文件的逻辑计算编码的密码。


    # 构造请求头部信息和 POST 请求参数
    cookie = "" #可根据自己浏览器设置，也可以空置
    headers = {
        "cookie": cookie,
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    data = {
        'DDDDD': number, #学号
        'upass': upass, #编码的密码，根据本地js计算。
        'R1': '0',
        'R2': '1',
        'para': '00',
        '0MKKey': '123456',
        'v6ip': '',
        'hid1': '',
        'hid2': '',
    }

    # 延迟登录
    time.sleep(10)

    logger.info('正在登录...')
    # 发送 POST 请求进行登录
    response = requests.post("http://drcom.nbu.edu.cn/0.htm", data=data, headers=headers)

    # 检查登录是否成功
    success_msg = "您已经成功登录"
    if success_msg in response.text:
        logger.info(success_msg)
    else:
        # 登录失败，进行重试
        logger.warning('登录失败，正在进行重试...')
        for i in range(3):
            time.sleep(60)
            response = requests.post("http://drcom.nbu.edu.cn/0.htm", data=data, headers=headers)
            if success_msg in response.text:
                logger.info(success_msg)
                break
            else:
                logger.warning(f'第 {i+1} 次重试登录失败')
        else:
            logger.error('登录失败，重试次数用完')

if __name__ == '__main__':
    main()