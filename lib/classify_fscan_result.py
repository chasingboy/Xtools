# -*- coding=utf-8 -*-

import re

header = '''
+--------+--------+---------+-----------+--------------+------------+
|  Code  |   Url  |   Len   |   Title   |   Redirect   |   Finger   |
+--------+--------+---------+-----------+--------------+------------+\n
'''.lstrip()


def select_ip_port(text:str) -> str:
    ip_port_list = re.findall(
        r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d+)\ open', text
    )
    if ip_port_list == []:
        return 'ip:port 结果为空'
    
    ip_port_list = [('{ip}:{port} open'.format(ip=line[0],port=line[1])) for line in ip_port_list]
    return '\n'.join(ip_port_list)


def select_web_poc(text:str) ->str:
    web_poc_list = re.findall(r'(http.*?) (poc-.*)', text)
    if web_poc_list == []:
        return 'POC 检测漏洞结果为空'
    
    web_poc_list = [('{url} {poc}').format(url=line[0],poc=line[1]) for line in web_poc_list]
    return '[+] ' + '\n[+] '.join(web_poc_list)
    


def select_web_info(text:str) ->str:
    web_list = re.findall(
        r'WebTitle:\s*(http.*?)\s+code:(\d+)\s+len:(.*?)\s+title:(.*?)\n', text
    )

    if web_list == []:
        return 'Web Code｜Title 等信息为空'

    finger_list = re.findall(r'InfoScan:\s*(http.*?)\s+\[(.*?)]', text)
    
    webinfo = []
    for line in web_list:
        finger = 'Null'
        for x in finger_list:
            if line[0] == x[0]:
                finger = x[1]
                break
        
        webinfo.append(
            '[{code}] {url} [{length}] [{title}] [Finger: {finger}]'.format(
                url=line[0],code=line[1],length=line[2],title=line[3],finger=finger)
        )

    webinfo = '\n'.join(sorted(webinfo)).replace(' 跳转url: ','] [Redirect-> ')
    return header + webinfo


def select_ip_exp(text:str) -> str:
    ip_exp_list = re.findall(
            r'\[\+]\s*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(.*)', text
    )
    if ip_exp_list == []:
        return 'Exp 检测漏洞结果为空'
    
    ip_exp_list = [(
        'IP: {ip} Exp: {exp}'.format(ip=line[0],exp=line[1])
        ) for line in ip_exp_list
    ]

    return '[+] ' + '\n[+] '.join(ip_exp_list)


def select_weak_password(text:str) -> str:
    weak_password_list = re.findall(
        r'\[\+\]\s*((ftp|Mysql|Mssql|SMB|RDP|Postgres|SSH|Oracle|SMB2-shares|redis|Mongodb|Memcached)(:|\s).+)\n', text, re.I
    )
    if weak_password_list == []:
        return '弱口令检查结果为空'
    
    weak_password_list = sorted([line[0] for line in weak_password_list])

    weak_password, server = '',''
    for line in weak_password_list:
        if server == line.split(':',1)[0]:
            weak_password += '[+] {}\n'.format(line)
        else:
            weak_password += '\n[+] {}\n'.format(line)
            server = line.split(':',1)[0]

    return weak_password


def select_os_info(text:str) -> str:
    # OS | NetBios | NetInfo
    osinfo = ''
    
    os_list = re.findall(r"\[\*]\s*(\d+\.\d+\.\d+\.\d+..+)", text)
    for line in os_list:
        osinfo += '[*] {}\n'.format(line)

    # NetBios:\s*(.*?)\s+(.*?\S)\s+(.*)
    netbios_list = re.findall(r'(NetBios:\s*\d+\.\d+\.\d+\.\d+..+)', text)
    for line in netbios_list:
        osinfo += '[*] {}\n'.format(line)

    netinfo_list = re.findall(r'(NetInfo:\n\[\*]\s*\d+\.\d+\.\d+\.\d+\s*\n(\s*\[\->].+\n)*)', text)
    netinfo_list = [line[0] for line in netinfo_list]

    for line in netinfo_list:
        osinfo += '[*] {}\n'.format(line.replace(' ',''))

    if osinfo == '':
        return '主机信息探测结果为空'
   
    return osinfo.rstrip('\n[*] ')


def classify_fscan_result(text:str) -> dict:
    ip_ports, web_poc, web_info, ip_exp, weak_password, os_info = (
        select_ip_port(text),
        select_web_poc(text),
        select_web_info(text),
        select_ip_exp(text),
        select_weak_password(text),
        select_os_info(text)
    )

    results = {
        'ip-port.txt': ip_ports,
        'web-poc.txt': web_poc,
        'web-info.txt': web_info,
        'ip-exp.txt': ip_exp,
        'weak-password.txt': weak_password,
        'os-info.txt': os_info
    }
    return results


# Reference
# https://blog.csdn.net/aaaaa_ascii/article/details/131956793