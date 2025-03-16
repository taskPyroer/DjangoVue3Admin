"""
Time:     2023/12/1 11:01
Author:   公众号【布鲁的Python之旅】，【github】https://github.com/taskPyroer， 【gitee】https://gitee.com/hu_yupeng123/projects
Version:  V 0.1
File:     linux
Describe: linux系统命令工具类封装
"""
import os, sys, re, time
import psutil
from django.core.cache import cache
from application.settings import EXEC_LOG_PATH
from pathlib import Path
# import pwd
import subprocess
import platform

BASE_DIR = Path(__file__).resolve().parent


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


def WriteLog(logMsg):
    """
    写日志
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
    version = cache.get(key)
    if version: return version
    try:
        # Python 3.8 已移除 此方法 "linux_distribution()"
        platform_dist = platform.linux_distribution()
        version = platform_dist[0] + " " + platform_dist[1]
    except:
        with os.popen("cat /etc/redhat-release", "r") as p:
            release = p.read()
        version = release.replace('release ', '').replace('Linux', '').replace('(Core)', '').strip()

    pyv_info = sys.version_info
    version = "{} {}(Py{}.{}.{})".format(version, os.uname().machine, pyv_info.major, pyv_info.minor, pyv_info.micro)
    cache.set(key, version, 86400)
    return version


def GetLoadAverage():
    """
    取系统负载
    """
    try:
        c = os.getloadavg()
    except:
        c = [0, 0, 0]
    data = {}
    data['one'] = float(c[0])
    data['five'] = float(c[1])
    data['fifteen'] = float(c[2])
    data['max'] = psutil.cpu_count() * 2
    data['limit'] = data['max']
    data['safe'] = data['max'] * 0.75
    temppercent = round(data['one'] / data['max'] * 100)
    data['percent'] = 100 if temppercent > 100 else temppercent
    return data


def GetMemInfo():
    """
    取内存信息
    """
    mem = psutil.virtual_memory()
    memInfo = {}
    memInfo2 = {'memTotal': int(mem.total / 1024 / 1024), 'memFree': int(mem.free / 1024 / 1024),
                'memBuffers': int(mem.buffers / 1024 / 1024), 'memCached': int(mem.cached / 1024 / 1024)}
    memInfo['total'] = round(float(mem.total) / 1024 / 1024 / 1024, 2)
    memInfo['free'] = round((memInfo2['memFree'] + memInfo2['memBuffers'] + memInfo2['memCached']) / 1024, 2)
    memInfo['used'] = round(float(mem.used) / 1024 / 1024 / 1024, 2)
    memInfo['percent'] = round((int(mem.used) / 1024 / 1024) / memInfo2['memTotal'] * 100, 1)
    return memInfo


def get_disk_iostat():
    """
    获取磁盘IO
    """
    iokey = 'iostat'
    diskio = cache.get(iokey)
    mtime = int(time.time())
    if not diskio:
        diskio = {}
        diskio['info'] = None
        diskio['time'] = mtime
    diskio_1 = diskio['info']
    stime = mtime - diskio['time']
    if not stime: stime = 1
    diskInfo = {}
    diskInfo['ALL'] = {}
    diskInfo['ALL']['read_count'] = 0
    diskInfo['ALL']['write_count'] = 0
    diskInfo['ALL']['read_bytes'] = 0
    diskInfo['ALL']['write_bytes'] = 0
    diskInfo['ALL']['read_time'] = 0
    diskInfo['ALL']['write_time'] = 0
    diskInfo['ALL']['read_merged_count'] = 0
    diskInfo['ALL']['write_merged_count'] = 0
    try:
        if os.path.exists('/proc/diskstats'):
            diskio_2 = psutil.disk_io_counters(perdisk=True)
            if not diskio_1:
                diskio_1 = diskio_2
            for disk_name in diskio_2.keys():
                diskInfo[disk_name] = {}
                diskInfo[disk_name]['read_count'] = int(
                    (diskio_2[disk_name].read_count - diskio_1[disk_name].read_count) / stime)
                diskInfo[disk_name]['write_count'] = int(
                    (diskio_2[disk_name].write_count - diskio_1[disk_name].write_count) / stime)
                diskInfo[disk_name]['read_bytes'] = int(
                    (diskio_2[disk_name].read_bytes - diskio_1[disk_name].read_bytes) / stime)
                diskInfo[disk_name]['write_bytes'] = int(
                    (diskio_2[disk_name].write_bytes - diskio_1[disk_name].write_bytes) / stime)
                diskInfo[disk_name]['read_time'] = int(
                    (diskio_2[disk_name].read_time - diskio_1[disk_name].read_time) / stime)
                diskInfo[disk_name]['write_time'] = int(
                    (diskio_2[disk_name].write_time - diskio_1[disk_name].write_time) / stime)
                diskInfo[disk_name]['read_merged_count'] = int(
                    (diskio_2[disk_name].read_merged_count - diskio_1[disk_name].read_merged_count) / stime)
                diskInfo[disk_name]['write_merged_count'] = int(
                    (diskio_2[disk_name].write_merged_count - diskio_1[disk_name].write_merged_count) / stime)

                diskInfo['ALL']['read_count'] += diskInfo[disk_name]['read_count']
                diskInfo['ALL']['write_count'] += diskInfo[disk_name]['write_count']
                diskInfo['ALL']['read_bytes'] += diskInfo[disk_name]['read_bytes']
                diskInfo['ALL']['write_bytes'] += diskInfo[disk_name]['write_bytes']
                if diskInfo['ALL']['read_time'] < diskInfo[disk_name]['read_time']:
                    diskInfo['ALL']['read_time'] = diskInfo[disk_name]['read_time']
                if diskInfo['ALL']['write_time'] < diskInfo[disk_name]['write_time']:
                    diskInfo['ALL']['write_time'] = diskInfo[disk_name]['write_time']
                diskInfo['ALL']['read_merged_count'] += diskInfo[disk_name]['read_merged_count']
                diskInfo['ALL']['write_merged_count'] += diskInfo[disk_name]['write_merged_count']

            cache.set(iokey, {'info': diskio_2, 'time': mtime})
    except:
        return diskInfo
    return diskInfo


def GetNetWork():
    """
    取网卡数据
    """
    cache_timeout = 86400
    otime = cache.get("pao_otime")
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
        networkIo = networkIo_list[net_key][:4]
        up_key = "{}_up".format(net_key)
        down_key = "{}_down".format(net_key)
        otime_key = "pao_otime"

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
        networkInfo['network'][net_key]['up'] = round(float(networkIo[0] - up) / 1024 / (ntime - otime), 2)
        networkInfo['network'][net_key]['down'] = round(float(networkIo[1] - down) / 1024 / (ntime - otime), 2)
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
    networkInfo['iostat'] = get_disk_iostat()

    return networkInfo


def GetBootTime():
    """
    取系统启动时间(天)
    """
    key = 'pao_sys_time'
    sys_time = cache.get(key)
    if sys_time: return sys_time
    uptime_seconds = time.mktime(time.localtime(time.time())) - psutil.boot_time()
    run_days = int(uptime_seconds / 86400)
    # run_hour = int((uptime_seconds % 86400) / 3600)
    # run_minute = int((uptime_seconds % 3600) / 60)
    # run_second = int(uptime_seconds % 60)
    sys_time = "{}天".format(run_days)
    cache.set(key, sys_time, 1800)
    return sys_time


def getCpuInfoDict():
    """
    取/proc/cpuinfo信息字典
    """
    cpuinfo = {}
    procinfo = {}
    nprocs = 0
    with open('/proc/cpuinfo') as f:
        for line in f:
            if not line.strip():
                cpuinfo['proc%s' % nprocs] = procinfo
                nprocs = nprocs + 1
                procinfo = {}
            else:
                if len(line.split(':')) == 2:
                    procinfo[line.split(':')[0].strip()] = line.split(':')[1].strip()
                else:
                    procinfo[line.split(':')[0].strip()] = ''
    return cpuinfo


def GetCpuInfo(interval=1):
    """
    取CPU信息
    """

    cpuCount = cache.get('pao_cpu_cpuCount')
    if not cpuCount:
        cpuCount = psutil.cpu_count()
        cache.set('pao_cpu_cpuCount', cpuCount, 86400)
    cpuNum = cache.get('pao_cpu_cpuNum')
    if not cpuNum:
        cpuNum = psutil.cpu_count(logical=False)
        cache.set('pao_cpu_cpuNum', cpuNum, 86400)

    cpuW = cache.get('pao_cpu_cpuW')
    if not cpuW:
        cpuW = int(subprocess.check_output('cat /proc/cpuinfo | grep "physical id" | sort -u | wc -l', shell=True))
        cache.set('pao_cpu_cpuW', cpuW, 86400)

    used = psutil.cpu_percent(interval)

    used_all = psutil.cpu_percent(percpu=True)

    cpu_name = cache.get('pao_cpu_cpu_name')
    if not cpu_name:
        cpu_name = ""
        try:
            cpuinfo = getCpuInfoDict()
            cpu_name = cpuinfo['proc0']['model name'] + " * {}".format(cpuW)
        except:
            pass
        cache.set('pao_cpu_cpu_name', cpu_name, 86400)

    return used, cpuCount, used_all, cpu_name, cpuNum, cpuW


def GetDiskInfo():
    # 取磁盘分区信息
    key = 'pao_sys_disk'
    diskInfo = cache.get(key)
    if diskInfo: return diskInfo

    with os.popen("df -hT -P|grep '/'|grep -v tmpfs|grep -v 'snap/core'|grep -v udev", "r") as p:
        temp = p.read()

    with os.popen("df -i -P|grep '/'|grep -v tmpfs|grep -v 'snap/core'|grep -v udev", "r") as p:
        tempInodes = p.read()

    tempList = temp.split('\n')
    tempInodesList = tempInodes.split('\n')
    diskInfo = []
    n = 0
    cuts = ['/mnt/cdrom', '/boot', '/boot/efi', '/dev', '/dev/shm', '/run/lock', '/run', '/run/shm', '/run/user']
    for tmp in tempList:
        n += 1
        try:
            inodes = tempInodesList[n - 1].split()
            disk = re.findall(r"^(.+)\s+([\w\.]+)\s+([\w\.]+)\s+([\w\.]+)\s+([\w\.]+)\s+([\d%]{2,4})\s+(/.{0,100})$",
                              tmp.strip())
            if disk: disk = disk[0]
            if len(disk) < 6: continue
            if disk[2].find('M') != -1: continue
            if disk[2].find('K') != -1: continue
            if len(disk[6].split('/')) > 10: continue
            if disk[6] in cuts: continue
            if disk[6].find('docker') != -1: continue
            if disk[1].strip() in ['tmpfs']: continue
            arr = {}
            arr['filesystem'] = disk[0].strip()
            arr['type'] = disk[1].strip()
            arr['path'] = disk[6]
            tmp1 = [disk[2], disk[3], disk[4], disk[5].split('%')[0]]
            arr['size'] = tmp1
            arr['inodes'] = [inodes[1], inodes[2], inodes[3], inodes[4]]
            diskInfo.append(arr)
        except Exception as ex:
            WriteLog('获取磁盘信息失败:%s' % str(ex))
            continue
    cache.set(key, diskInfo, 1000)
    return diskInfo


def RestartServer():
    """
    重启系统
    """
    try:
        os.system("sync && init 6 &")
    except:
        pass
