import socket
import subprocess
from urllib.parse import urlparse, parse_qs
import requests
import platform


def get_wifi_ssid():
    if platform.system() == "Windows":
        command = "netsh wlan show interfaces"
        output = subprocess.check_output(command, shell=True).decode('gbk')
        for line in output.split("\n"):
            if "SSID" in line:
                ssid = line.split(" : ")[1].strip()
                return ssid
    elif platform.system() == "Linux":
        command = "iwgetid -r"
        output = subprocess.check_output(command, shell=True).decode("utf-8").strip()
        return output
    else:
        raise NotImplementedError("此功能暂不支持此操作系统。")


def login(username, password, operator):
    session = requests.Session()
    ssid = get_wifi_ssid()
    print(ssid)
    if ssid != "Njtech-Home":
        return False, "尚未连接wifi"

    local_ip = get_local_ip()

    data = {
        "DDDDD": ",0," + username + "@" + operator,
        "upass": password,
        "R1": "0",
        "R2": "0",
        "R3": "0",
        "R6": "0",
        "para": "00",
        "0MKKey": "123456",
        "buttonClicked": "",
        "redirect_url": "",
        "err_flag": "",
        "username": "",
        "password": "",
        "user": "",
        "cmd": "",
        "Login": "",
        "v6ip": "",
    }

    url = "http://10.50.255.11:801/eportal/?c=ACSetting&a=Login&protocol=http:&hostname=10.50.255.11&iTermType=1&wlanuserip=" + local_ip + "&wlanacip=null&wlanacname=null&mac=00-00-00-00-00-00&ip=" + local_ip + "&enAdvert=0&queryACIP=0&jsVersion=2.4.3&loginMethod=1"

    response = session.post(url, data=data, allow_redirects=False)


    if response.status_code in (301, 302):
        redirect_url = response.headers['Location']
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)

        ret_code = int(query_params.get('RetCode', [0])[0])

        if ret_code == 1:
            return False, "账号或密码错误"
        elif ret_code == 2:
            return True, "已经登录......"
        else:
            return True, "登录成功！"

    else:
        return False, "出现错误，请等待更新~"


def get_local_ip():
    try:
        # 通过连接到一个外部服务器，我们可以获取本机的IP地址
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('10.50.255.11', 80))
        local_ip = s.getsockname()[0]
    except Exception as e:
        print(f"无法获取本机IP地址: {e}")
        local_ip = "127.0.0.1"
    finally:
        s.close()
    return local_ip
