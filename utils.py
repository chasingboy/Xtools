# -*- coding=utf-8 -*-
# Functions lib

import sublime
from .config import *
import re, os, hashlib, socket
from urllib.parse import urlparse
import ipaddress


# Get system type
platform = sublime.platform()

def convert_ipv4_to_C(view):
    rets = {}
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}'
    regions = view.find_all(pattern)

    for region in regions:  
        ip = view.substr(region)
        if ip in rets.keys():
            rets[ip] = rets[ip] + 1
        else:
            rets[ip] = 1

    rets = sorted(rets.items(), key=lambda v:v[1], reverse = True)

    text = '[+] 所有 C 段: \n'
    for line in rets:
        text += '{0}.0/24 [{1}]'.format(line[0],line[1]) + "\n"
        
    return text


def convert_C_to_ipv4(view):
    pattern = r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)((([\-](1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])|/(1\d|2\d|3[0-2]|[1-9]))(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d))?)?)'
    regions = view.find_all(pattern)
    
    ret = []   
    for region in regions:
        line = view.substr(region)
        try:
            if '/' in line:
                ips = ipaddress.ip_network(line.strip(),strict=False).hosts()
                for ip in ips:
                    ret.append(str(ip))
            elif '-' in line:
                start,end = line.split('-')
                ip_range = parse_ip_range(start,end)
                ret += ip_range
            else:
                ret.append(line)
        except Exception as e:
            print(e)
            sublime.message_dialog('[error] IP C is invaild! Please check...')

    ret = '\n'.join(unique_sort_ipv4(ret))
    return ret


def parse_ip_range(start,end):
    if '.' not in end:
        end = start.rsplit('.',1)[0] + '.' + end
    
    start = ipaddress.ip_address(start)
    end = ipaddress.ip_address(end)
    ip_range = list(range(int(start),int(end)+1))
    ip_range = [str(ipaddress.ip_address(ip)) for ip in ip_range]
    
    return ip_range


def convert_ipv4_to_B(view):
    rets = {}
    pattern = r'\d{1,3}\.\d{1,3}\.'
    regions = view.find_all(pattern)

    for region in regions:  
        ip = view.substr(region).strip('.')
        if ip in rets.keys():
            rets[ip] = rets[ip] + 1
        else:
            rets[ip] = 1

    rets = sorted(rets.items(), key=lambda v:v[1], reverse = True)

    text = '[+] 所有 B 段: \n'
    for line in rets:
        text += '{0}.0.0/16 [{1}]'.format(line[0],line[1]) + "\n"
        
    return text


def select_ipv4(view):
    pattern = r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)((([\-](1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])|/(1\d|2\d|3[0-2]|[1-9]))(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d))?)?)'
    regions = view.find_all(pattern)

    lan_ips = []
    wan_ips = []
    for region in regions:
        text = view.substr(region)
        temp = text.split('-')[0].split('/')[0]
        if is_lan(temp):
            lan_ips.append(text)
        else:
            wan_ips.append(text)
            
    return unique_sort_ipv4(lan_ips),unique_sort_ipv4(wan_ips)


def is_lan(ip):
    try:
        return ipaddress.ip_address(ip.strip()).is_private or ipaddress.ip_address(ip.strip()).is_loopback
    except Exception as e:
        return False


def select_ipv4_range(view):
    pattern = r'(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)((([\-](1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])|/(1\d|2\d|3[0-2]|[1-9]))(\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d))?))'
    regions = view.find_all(pattern)
    ips = []
    for region in regions:
        text = view.substr(region)
        ips.append(text)
    
    return unique_sort_ipv4(ips)


def select_domain(view):
    pattern = r'([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+('+top_sufix+'|'+country_sufix+')'
    regions = view.find_all(pattern, sublime.IGNORECASE)

    rootdomains = []
    domains = []
    for region in regions:
        text = view.substr(region)
        domains.append(text)
        rootdomains.append(select_rootdomain(text))

    domains = list(set(domains))
    rootdomains = list(set(rootdomains))
    return sorted(domains), sorted(rootdomains)


def select_rootdomain(text):
    dms = text.split('.')
    if len(dms) == 2:
        return text
    if dms[-2] in top_sufix and dms[-1] in country_sufix:
        root = "{0}.{1}.{2}".format(dms[-3],dms[-2],dms[-1])
        return root
    if dms[-1] in top_sufix or dms[-1] in country_sufix:
        root = "{0}.{1}".format(dms[-2],dms[-1])
        return root


def select_urls(view, path=False):
    pattern = r'https?://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]'
    regions = view.find_all(pattern, sublime.IGNORECASE)

    array = []
    for region in regions:
        text = view.substr(region)
        if path == False:
            text = delete_url_path(text)
        if text not in array:
            array.append(text)
            
    text = '\n'.join(array)
    return text


def exec_command(cmd):
    if platform == 'windows':
        os.system('start cmd /k ' + cmd)
    elif platform == 'osx':
        try:
            from .applescript import tell
        except:
            sublime.message_dialog('[waring] macOS 请解压 applescript 文件')
            return 0
        tell.app('Terminal','do script"{cmd}"'.format(cmd=cmd),background=True)
    
    elif platform == 'linux':
        os.system("gnome-terminal -e 'bash -c \"{cmd}\"'".format(cmd=cmd))
    else:
        sublime.message_dialog('[waring] <Run Command> module is not supported this system')


def write_file(workdir,text):
    file = os.path.join(workdir,hashlib.md5(text.encode('utf-8')).hexdigest())
    with open(file,'w') as fw:
        fw.write(text)

    return file


def read_file(file):
    with open(file) as fr:
        text = fr.read().strip('\n')
    return text


def delete_url_path(url):
    o = urlparse(url)
    return o.scheme + '://' + o.netloc


def is_url(urls):
    errurls = ''
    for url in urls:
        if re.match(r'^https?:/{2}\w.+$', url):
            pass
        else:
            errurls += url + '\n'
    return errurls


def unique_sort_ipv4(ips):
    try:
        ips = sorted(list(set(ips)),key=socket.inet_aton)
    except:
        ips = sorted(list(set(ips)))
    return ips


'''
Select Routers
: urls,sort,filter
: Regex copy from linkfinder
'''

regex_str = r"""

  (?:"|')                               # Start newline delimiter

  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path

    |

    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be

    |

    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

  )

  (?:"|')                               # End newline delimiter

"""


def select_routers(text):
    regex = re.compile(regex_str, re.VERBOSE)
    routers = [m.group(1).lstrip('/') for m in re.finditer(regex, text)]
    return routers


def filter_routers(results):
    file_exts = ['png','jpg','jpeg','gif','js','vue','ico','svg','css','ts','bmp','ttf','woff','woff2']
    routers = ['\n[+] Routers:\n']
    links = ['\n[+] Links:\n']
    filters = ['\n[+] Filters:\n']
    
    results = sorted(list(set(results)))
    
    for router in results:   
        try:
            if 'http' in router:
                links.append(router)
                continue
            
            temp = router
            if '?' in temp:
                temp = temp.split('?')[0]
                if temp in routers:
                    x = routers.pop()

            ext = temp.split('.')[-1]
            if ext in file_exts:
                filters.append(router)
            else:
                routers.append(router)
        except:
            pass

    routers = [('/' + line) for line in routers]
    text = '\n'.join(routers+links+filters).lstrip('/')
    return text
