import requests
import re

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Host': 'jhc.sunnysport.org.cn',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'Origin': 'http://jhc.sunnysport.org.cn',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Referer': 'http://jhc.sunnysport.org.cn/login/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'
}


def spawn_data(user_name, user_pwd, vrf):
    return {
        'username': user_name,
        'vrf': vrf,
        'password': user_pwd,
        "userType": "person",
        "agency": "体育部"
    }


def get_mid_text(text, start_str, end_str):
    start_index = text.index(start_str)
    if start_index >= 0:
        start_index += len(start_str)
    end_index = text.index(end_str)
    return text[start_index:end_index]


if __name__ == '__main__':
    session = requests.session()
    res = session.get("http://jhc.sunnysport.org.cn/login/", data={}, headers=header)
    header['Cookie'] = res.headers['Set-Cookie'].split(";")[0]
    html = res.text
    vrf = re.search('name="vrf" value="(.*?)">', html).group(1)
    data = spawn_data("账号", "密码", vrf)
    res = session.post('http://jhc.sunnysport.org.cn/login/', headers=header, data=data, allow_redirects=False)
    response_header = res.headers
    session_id = response_header['set-cookie'].split(";")[0]
    header['Cookie'] = session_id
    print(requests.get("http://jhc.sunnysport.org.cn/runner/data/speed.json",headers=header).text)
