# -*- coding:UTF-8 -*-

import requests, re
from prettyprinter import cpprint

# demo
# curl 'http://en.wikipedia.org/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://www.wikipedia.org/'  -H 'Connection: keep-alive' --compressed
# curl "https://www.cnblogs.com/zhoug2020/p/9039993.html" -H "authority: www.cnblogs.com" -H "pragma: no-cache" -H "cache-control: no-cache" -H "upgrade-insecure-requests: 1" -H "user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36" -H "accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3" -H "referer: https://www.google.co.jp/" -H "accept-encoding: gzip, deflate, br" -H "accept-language: zh-CN,zh;q=0.9,en;q=0.8" -H "cookie: _ga=GA1.2.577668390.1545921139; __gads=ID=40e2709668d23321:T=1545921142:S=ALNI_Maqy0OtSXqrISxVIGI95fJatdwSOQ; CNZZDATA2634245=cnzz_eid^%^3D486374850-1549946525-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^26ntime^%^3D1549946525; Hm_lvt_4378208a68c9487243e1ff28cc2b7f3c=1550660687; CNZZDATA5897703=cnzz_eid^%^3D574966410-1551415936-https^%^253A^%^252F^%^252Fwww.baidu.com^%^252F^%^26ntime^%^3D1551415936; CNZZDATA1260233382=305447537-1553764057-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^7C1553764057; CNZZDATA1260689952=721449009-1557216220-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^7C1557216220; CNZZDATA4606621=cnzz_eid^%^3D172194260-1558409726-https^%^253A^%^252F^%^252Fwww.baidu.com^%^252F^%^26ntime^%^3D1558409726; CNZZDATA1000322585=44769197-1558533483-^%^7C1558533483; CNZZDATA1683856=cnzz_eid^%^3D1668476591-1558624377-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^26ntime^%^3D1558624377; Hm_lvt_5dd8d6438668e6e79fa6f818cd433df3=1560932881; CNZZDATA1262803054=1981957650-1560932886-https^%^253A^%^252F^%^252Fwww.baidu.com^%^252F^%^7C1560932886; UM_distinctid=16bb7d50f0f2ca-0638f968f89ed2-5f1d3a17-1fa400-16bb7d50f103ab; CNZZDATA1252961619=1339647014-1563375914-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^7C1563375914; CNZZDATA1557464=cnzz_eid^%^3D634534307-1563976778-https^%^253A^%^252F^%^252Fwww.baidu.com^%^252F^%^26ntime^%^3D1563976778; CNZZDATA1272990511=1070075849-1564657868-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^7C1564657868; CNZZDATA1121896=cnzz_eid^%^3D1959876444-1562154679-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^26ntime^%^3D1564714422; CNZZDATA943648=cnzz_eid^%^3D1035949263-1562154148-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^26ntime^%^3D1564714422; CNZZDATA1254128672=1469006085-1549134674-https^%^253A^%^252F^%^252Fwww.google.co.jp^%^252F^%^7C1564735111; _gid=GA1.2.72762212.1565187265" --compressed
# curl 'https://www.cnblogs.com/zhoug2020/p/9039993.html' -H 'authority: www.cnblogs.com' -H 'pragma: no-cache' -H 'cache-control: no-cache' -H 'upgrade-insecure-requests: 1' -H 'user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36' -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3' -H 'referer: https://www.google.co.jp/' -H 'accept-encoding: gzip, deflate, br' -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8' -H 'cookie: _ga=GA1.2.577668390.1545921139; __gads=ID=40e2709668d23321:T=1545921142:S=ALNI_Maqy0OtSXqrISxVIGI95fJatdwSOQ; CNZZDATA2634245=cnzz_eid%3D486374850-1549946525-https%253A%252F%252Fwww.google.co.jp%252F%26ntime%3D1549946525; Hm_lvt_4378208a68c9487243e1ff28cc2b7f3c=1550660687; CNZZDATA5897703=cnzz_eid%3D574966410-1551415936-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1551415936; CNZZDATA1260233382=305447537-1553764057-https%253A%252F%252Fwww.google.co.jp%252F%7C1553764057; CNZZDATA1260689952=721449009-1557216220-https%253A%252F%252Fwww.google.co.jp%252F%7C1557216220; CNZZDATA4606621=cnzz_eid%3D172194260-1558409726-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1558409726; CNZZDATA1000322585=44769197-1558533483-%7C1558533483; CNZZDATA1683856=cnzz_eid%3D1668476591-1558624377-https%253A%252F%252Fwww.google.co.jp%252F%26ntime%3D1558624377; Hm_lvt_5dd8d6438668e6e79fa6f818cd433df3=1560932881; CNZZDATA1262803054=1981957650-1560932886-https%253A%252F%252Fwww.baidu.com%252F%7C1560932886; UM_distinctid=16bb7d50f0f2ca-0638f968f89ed2-5f1d3a17-1fa400-16bb7d50f103ab; CNZZDATA1252961619=1339647014-1563375914-https%253A%252F%252Fwww.google.co.jp%252F%7C1563375914; CNZZDATA1557464=cnzz_eid%3D634534307-1563976778-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1563976778; CNZZDATA1272990511=1070075849-1564657868-https%253A%252F%252Fwww.google.co.jp%252F%7C1564657868; CNZZDATA1121896=cnzz_eid%3D1959876444-1562154679-https%253A%252F%252Fwww.google.co.jp%252F%26ntime%3D1564714422; CNZZDATA943648=cnzz_eid%3D1035949263-1562154148-https%253A%252F%252Fwww.google.co.jp%252F%26ntime%3D1564714422; CNZZDATA1254128672=1469006085-1549134674-https%253A%252F%252Fwww.google.co.jp%252F%7C1564735111; _gid=GA1.2.72762212.1565187265' --compressed
input_str = "curl 'https://en.wikipedia.org/' -H 'Accept-Encoding: gzip, deflate, sdch' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8' -H 'Referer: http://www.wikipedia.org/'  -H 'Connection: keep-alive' --compressed"
# input_str = "curl 'http://fiddle.jshell.net/echo/html/' -H 'Origin: http://fiddle.jshell.net' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'Accept: */*' -H 'Referer: http://fiddle.jshell.net/_display/' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' --data 'msg1=wow&msg2=such' --compressed"
# input_str = "curl 'https://api.guazi.com/clientUc/index/getUserInfo' -X OPTIONS -H 'Access-Control-Request-Method: GET' -H 'Origin: https://uc.guazi.com' -H 'Referer: https://uc.guazi.com/' -H 'User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36' -H 'Access-Control-Request-Headers: client-time,verify-token' --compressed"
input_str = "curl 'https://www.xxx.com/login.php' -H 'Referer: https://m-jr.guazi.com/loan_v2/login?' -H 'Origin: https://m-jr.guazi.com' -H 'User-Agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Mobile Safari/537.36' -H 'Content-Type: application/x-www-form-urlencoded' --data 'phone=13922342320&_hash_=3b096e6c-a5e9-422f-9d0a-5a12d6cdeb87_1913d5fed0397a8c2f126e2b170d94ff&_salt_=e217a9f06c64574f17ded075859ff170' --compressed"

request_method = ""
request_url = ""
request_header = {}
request_data = {}
if re.match("curl", input_str, re.I):

    # region 判断提交方法
    x_option = re.search(r"-X (.*?) ", input_str, re.I)
    d_option = re.search(r"--data", input_str, re.I)
    if x_option != None:
        request_method = x_option.group(1)
    elif d_option != None:
        request_method = 'POST'
    else:
        request_method = 'GET'
    # endregion

    # region 匹配请求url
    try:
        request_url = re.search(r"curl ['\"]((http|https).*?)['\"]", input_str, re.I).group(1)
    except AttributeError as e:
        print("请求URL不合法")
        quit()
    # endregion

    #region 匹配请求头
    try:
        for header in re.finditer(r"-H ['\"](.*?: (?!\s).*?)['\"]", input_str, re.I):
            x = re.split(r":", header.group(1), maxsplit=1, flags=re.I)
            request_header[x[0]] = x[1].strip()
    except Exception as e:
        print("报文头不合法")
        quit()
    # endregion

    # region匹配数据
    data = re.search(r"--data ['\"](.*?)['\"]", input_str, re.I)
    if data != None:
        data = re.split(r"&", data.group(1), flags=re.I)
        for x in data:
            y = re.split(r"=", x, maxsplit=1, flags=re.I)
            request_data[y[0]] = y[1]

cpprint(request_method)
cpprint(request_url)
print(request_header)
cpprint(request_data)

# response = requests.request(request_method, request_url, headers=request_header, data=request_data, timeout=10)
# print(response.text)