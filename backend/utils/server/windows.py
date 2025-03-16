"""
Time:     2023/11/30 17:04
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     windows
Describe: windows系统命令工具类封装
"""
import sys
import platform
import os, time
import psutil
import winreg
from django.core.cache import cache
from pathlib import Path

from application.settings import EXEC_LOG_PATH

BASE_DIR = Path(__file__).resolve().parent


def ReadReg(path, key):
    """
    读取注册表
    @path 注册表路径
    @key 注册表键值
    """
    import winreg
    try:
        newKey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
        value, type = winreg.QueryValueEx(newKey, key)
        return value
    except:
        return False


def get_mac_address():
    """
    获取mac
    """
    import uuid
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e + 2] for e in range(0, 11, 2)])


def md5(strings):
    """
    @name 生成md5
    @param strings 要被处理的字符串
    @return string(32)
    """
    if type(strings) != bytes:
        strings = strings.encode()
    import hashlib
    m = hashlib.md5()
    m.update(strings)
    return m.hexdigest()


def to_size(size):
    """
    字节单位转换
    @size 字节大小
    return 返回带单位的格式(如：1 GB)
    """
    if not size: return '0.00 b'
    size = float(size)

    d = ('b', 'KB', 'MB', 'GB', 'TB')
    s = d[0]
    for b in d:
        if size < 1024: return ("%.2f" % size) + ' ' + b
        size = size / 1024
        s = b
    return ("%.2f" % size) + ' ' + b


def is_64bitos():
    """
    判断是否x64系统(windows\linux都适用)
    利用platform.uname()
    windows:uname_result(system='Windows', node='xxxxx', release='10', version='10.0.19042', machine='AMD64')
    linux:uname_result(system='Linux', node='xxxx', release='5.10.134-12.2.al8.x86_64', version='#1 SMP Thu Oct 27 10:07:15 CST 2022', machine='x86_64', processor='x86_64')
    """
    info = platform.uname()
    return info.machine.endswith('64')


def get_registry_value(key, subkey, value):
    """
    读取注册表信息
    @key 注册表类型
    @subkey 注册表路径
    @value 注册表具体key值
    """
    key = getattr(winreg, key)
    handle = winreg.OpenKey(key, subkey)
    (value, type) = winreg.QueryValueEx(handle, value)
    return value


def WriteLog(logMsg):
    """
    写入LOG日志
    """
    try:
        with open(EXEC_LOG_PATH, 'w+') as f:
            f.write(logMsg)
            f.close()
    except:
        pass


def GetSystemVersion():
    """
    取操作系统版本
    """
    key = 'pao_sys_version'
    try:
        version = cache.get(key)
        if version: return version
        bit = 'x86'
        if is_64bitos(): bit = 'x64'

        def get(key):
            return get_registry_value("HKEY_LOCAL_MACHINE", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", key)

        os = get("ProductName")
        build = get("CurrentBuildNumber")

        version = "%s (build %s) %s (Py%s)" % (os, build, bit, platform.python_version())
        cache.set(key, version, 10000)
        return version
    except Exception as ex:
        WriteLog(f'获取系统版-获取系统版本失败,注册表无法打开,报错信息：{str(ex)}', )
        version = "未知系统版本"
        cache.set(key, version, 10000)
        return version


def GetLoadAverage():
    """
    取负载信息
    """
    data = {}
    data['one'] = 0
    data['five'] = 0
    data['fifteen'] = 0
    data['max'] = psutil.cpu_count() * 2
    data['limit'] = data['max']
    data['safe'] = data['max'] * 0.75
    data['percent'] = 0
    return data


def GetMemInfo():
    """
    取内存信息
    """
    mem = psutil.virtual_memory()
    memInfo = {}
    memInfo['percent'] = mem.percent
    memInfo['total'] = round(float(mem.total) / 1024 / 1024 / 1024, 2)
    memInfo['free'] = round(float(mem.free) / 1024 / 1024 / 1024, 2)
    memInfo['used'] = round(float(mem.used) / 1024 / 1024 / 1024, 2)
    return memInfo


def GetNetWork():
    """
    获取网卡信息
    """

    cache_timeout = 86400
    otime = cache.get("otime")
    ntime = time.time()
    networkInfo = {}
    networkInfo['network'] = {}
    networkInfo['upTotal'] = 0
    networkInfo['downTotal'] = 0
    networkInfo['up'] = 0
    networkInfo['down'] = 0
    networkInfo['downPackets'] = 0
    networkInfo['upPackets'] = 0
    networkIo_list = psutil.net_io_counters(pernic=True)

    for net_key in networkIo_list.keys():
        if net_key.find('Loopback') >= 0 or net_key.find('Teredo') >= 0 or net_key.find('isatap') >= 0: continue

        networkIo = networkIo_list[net_key][:4]
        up_key = "{}_up".format(net_key)
        down_key = "{}_down".format(net_key)
        otime_key = "otime"

        if not otime:
            otime = time.time()

            cache.set(up_key, networkIo[0], cache_timeout)
            cache.set(down_key, networkIo[1], cache_timeout)
            cache.set(otime_key, otime, cache_timeout)

        networkInfo['network'][net_key] = {}
        up = cache.get(up_key)
        down = cache.get(down_key)
        if not up:
            up = networkIo[0]
        if not down:
            down = networkIo[1]
        networkInfo['network'][net_key]['upTotal'] = networkIo[0]
        networkInfo['network'][net_key]['downTotal'] = networkIo[1]
        try:
            networkInfo['network'][net_key]['up'] = round(float(networkIo[0] - up) / 1024 / (ntime - otime), 2)
            networkInfo['network'][net_key]['down'] = round(float(networkIo[1] - down) / 1024 / (ntime - otime), 2)
        except:
            networkInfo['up'] = 0
            networkInfo['down'] = 0

            networkInfo['network'][net_key]['up'] = 0
            networkInfo['network'][net_key]['down'] = 0

        networkInfo['network'][net_key]['downPackets'] = networkIo[3]
        networkInfo['network'][net_key]['upPackets'] = networkIo[2]

        networkInfo['upTotal'] += networkInfo['network'][net_key]['upTotal']
        networkInfo['downTotal'] += networkInfo['network'][net_key]['downTotal']
        networkInfo['up'] += networkInfo['network'][net_key]['up']
        networkInfo['down'] += networkInfo['network'][net_key]['down']
        networkInfo['downPackets'] += networkInfo['network'][net_key]['downPackets']
        networkInfo['upPackets'] += networkInfo['network'][net_key]['upPackets']

        cache.set(up_key, networkIo[0], cache_timeout)
        cache.set(down_key, networkIo[1], cache_timeout)
        cache.set(otime_key, time.time(), cache_timeout)

    networkInfo['up'] = round(float(networkInfo['up']), 2)
    networkInfo['down'] = round(float(networkInfo['down']), 2)
    networkInfo['iostat'] = {}

    return networkInfo


def GetBootTime():
    """
    取系统启动时间
    """
    key = 'pao_sys_time'
    sys_time = cache.get(key)
    if sys_time: return sys_time
    import math
    tStr = time.time() - psutil.boot_time()
    min = tStr / 60
    hours = min / 60
    days = math.floor(hours / 24)
    hours = math.floor(hours - (days * 24))
    min = math.floor(min - (days * 60 * 24) - (hours * 60))
    sys_time = f"{int(days)}天"
    cache.set(key, sys_time, 1800)
    return sys_time


def GetCpuInfo(interval=1):
    """
    取CPU详细信息
    """
    cpuCount = cache.get('pao_cpu_cpuCount')
    if not cpuCount:
        cpuCount = psutil.cpu_count()
        cache.set('pao_cpu_cpuCount', cpuCount, 86400)
    cpuNum = cache.get('pao_cpu_cpuNum')
    if not cpuNum:
        cpuNum = psutil.cpu_count(logical=False)
        cache.set('pao_cpu_cpuNum', cpuNum, 86400)

    # used = cache.get('pao_cpu_used')
    # if not used:
    #     used = psutil.cpu_percent(interval)
    #     cache.set('pao_cpu_used',used,20)

    used_all = cache.get('pao_cpu_used_all')
    if not used_all:
        used_all = psutil.cpu_percent(percpu=True)

    used_total = 0
    for x in used_all: used_total += x

    cpuW = cache.get('pao_cpu_cpuW')
    if not cpuW:
        ret = os.popen('wmic cpu get NumberOfCores').read()
        cpuW = 0
        arrs = ret.strip().split('\n\n')
        for x in arrs:
            val = x.strip()
            if not val: continue
            try:
                val = int(val)
                cpuW += 1
            except:
                pass

        cache.set('pao_cpu_cpuW', cpuW, 86400)

    cpu_name = cache.get('pao_cpu_cpu_name')
    if not cpu_name:
        try:
            cpu_name = '{} * {}'.format(
                ReadReg(r'HARDWARE\DESCRIPTION\System\CentralProcessor\0', 'ProcessorNameString').strip(), cpuW)
        except:
            cpu_name = ''
        cache.set('pao_cpu_cpu_name', cpu_name, 86400)

    tmp = 0
    if cpuW:
        tmp = cpuNum / cpuW

    used = 0
    if used_total:
        used = round(used_total / cpuCount, 2)
    return used, cpuCount, used_all, cpu_name, tmp, cpuW


def GetDiskInfo():
    """
    取磁盘分区信息
    """
    key = 'pao_sys_disk'
    diskInfo = cache.get(key)
    if diskInfo: return diskInfo
    try:
        diskIo = psutil.disk_partitions()
    except:
        import string
        diskIo = []
        for c in string.ascii_uppercase:
            disk = c + ':'
            if os.path.isdir(disk):
                data = {}
                data['mountpoint'] = disk + '/'
                diskIo.append(data)

    diskInfo = []
    for disk in diskIo:
        try:
            tmp = {}
            tmp['path'] = disk.mountpoint.replace("\\", "/")
            usage = psutil.disk_usage(disk.mountpoint)
            tmp['size'] = [to_size(usage.total), to_size(usage.used), to_size(usage.free), usage.percent]
            tmp['inodes'] = False
            diskInfo.append(tmp)
        except:
            pass
    cache.set(key, diskInfo, 10)
    return diskInfo


def RestartServer():
    """
    重启系统
    """
    try:
        os.system("shutdown /r /f /t 0")
    except:
        pass