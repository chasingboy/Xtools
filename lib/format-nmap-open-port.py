# -*- coding=utf-8 -*-
# python3

import sys

waf_hosts = ['\n\n# WAF host:']

def format_nmap_ports_from_xml(xml):
    results = ''
    for host in xml.find_all('host'):
        address, ports = host.address['addr'], host.ports

        open_ports = ports.find_all('port')
        if len(open_ports) > 100:
            waf_hosts.append(address)
            continue
        
        for info in open_ports:
            if info.state['state'] != 'open': continue
            
            port = info['portid']
            try:
                service = info.service['name']
            except:
                service = 'unknow'
            
            #print(address + ':' + port)
            results += address + ':' + port + '\n'
    return results
            

if __name__ == '__main__':
    filename = sys.argv[1]

    try:
        from bs4 import BeautifulSoup
    except:
        with open(filename,'w') as fw: fw.write(f'[ERR] could not import bs4, please install bs4 [python3 -m pip install bs4]')
        exit()

    try:
        with open(filename) as fr: xml = fr.read()
        xml = BeautifulSoup(xml,'xml')
    except:
        #print(f'[ERR] could not open file {filename}')
        with open(filename,'w') as fw: fw.write(f'[ERR] could not open xml file')
        exit()
    
    results = format_nmap_ports_from_xml(xml)
    if len(waf_hosts) > 1:
        results += '\n'.join(waf_hosts)
    try:
        with open(filename,'w') as fw: fw.write(results)
    except:
        with open(filename,'w') as fw: fw.write('[ERR] script running failed!')
