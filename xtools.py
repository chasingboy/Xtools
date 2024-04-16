# -*- coding=utf-8 -*-

import sublime_plugin
from sublime import Region
from .utils import *
import json,time
import base64,hashlib


"""
: Setting working directory
: HOME = '/Users/xxx/'
: workdir = '$HOME/.xtools'
"""  

if platform == 'windows':
    HOME = os.environ['HOMEPATH']
else:
    HOME = os.environ['HOME']

'''
-> 如果系统的用户名是中文且安装不成功，可以尝试在 xtools.py 文件设置系统的 "<用户名>"
-> 删除 # 注释
Eg: 
HOME = "C:\\Users\\" + u"中文"
'''

#HOME = "/Users/" + u"<用户名>"    # osx
#HOME = "/home/" + u"<用户名>"     # linux
#HOME = "C:\\Users\\" + u"<用户名>"  # windows

workdir = os.path.join(HOME,'.xtools')


try:
    if os.path.exists(workdir):
        print('.xtools directory is exists')
    else:
        os.mkdir(workdir)
        print('Create .xtools directory successfully')
except:
    sublime.message_dialog('[waring] .xtools directory is created failed')


'''
-> 版本信息
'''

VERSION = '2.1.1'

ABOUT_XTOOLS = '''
About Xtools

Xtools 是一款 Sublime Text 插件、同时是一款简单的资产处理、命令行调用工具

__   __ _                 _      
\ \ / /| |               | |     
 \ V / | |_  ___    ___  | | ___ 
 /   \ | __|/ _ \  / _ \ | |/ __|
/ /^\ \| |_| (_) || (_) || |\__ \
\/   \/ \__|\___/  \___/ |_||___/


参考文档 Github@https://github.com/chasingboy/Xtools
当前版本 Version@{version}     [{tip}]
'''


# IP And Domain
class SelectIpv4LanCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lan_ips,wan_ips =select_ipv4(self.view)
        text = '\n'.join(lan_ips)  
        new_view(self.view, edit, text)


class SelectIpv4WanCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        lan_ips,wan_ips =select_ipv4(self.view)
        text = '\n'.join(wan_ips)
        new_view(self.view, edit, text)


class SelectIpv4RangeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        ips = select_ipv4_range(self.view)
        text = '\n'.join(ips)
        new_view(self.view, edit, text)


class ConvertRangeIp2cCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = convert_ipv4_to_C(self.view)
        new_view(self.view, edit, text)


class ConvertRangeC2ipCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = convert_C_to_ipv4(self.view)
        new_view(self.view, edit, text)


class ConvertRangeIp2bCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = convert_ipv4_to_B(self.view)
        new_view(self.view, edit, text)


class SelectDomainRootAllCommand(sublime_plugin.TextCommand):
    def remove(self,edit):
        exts = ['.html','.login','.action','.htm']
        text = get_buffer_text(self.view)
        _text = text
        for ext in exts:
            _text = _text.lower().replace(ext,'#####')
        update_file(self.view, edit, _text)

        return text

    def run(self, edit, cmd):
        text = self.remove(edit)
        domains,rootdomains = select_domain(self.view)
        update_file(self.view, edit, text)

        text = '\n'.join(rootdomains) if cmd == 'root' else '\n'.join(domains)
        new_view(self.view, edit, text)

class FilterDnsCdnHostCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        ips = text.replace(' ','').split('\n')
        
        text = ''
        black_text = []
        for ip in ips:
            if ip in filter_hosts:
                black_text.append(ip)
            else:
                text += ip + '\n'

        black_text = '\n'.join(list(set(black_text)))
        text = "{0}\n\n# filter host:\n{1}".format(text,black_text)
        update_file(self.view, edit, text)


class FilterDnsCdnDomainCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        buffers = get_buffer_text(self.view)
        
        text = buffers
        black_text = []
        for line in buffers.split('\n'):
            for fd in filter_domains:
                if fd in line or fd == line:
                    text = text.replace(line + '\n', '')
                    black_text.append(fd)

        black_text = '\n'.join(list(set(black_text)))
        text = "{0}\n\n# filter host:\n{1}".format(text,black_text)
        update_file(self.view, edit, text)


# URL And Router 
class SelectUrlsExcludePathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = select_urls(self.view, False)
        new_view(self.view, edit, text)


class SelectUrlsIncludePathCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = select_urls(self.view, True)
        new_view(self.view, edit, text)


class SelectRoutersFromTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        results = select_routers(text)
        text = filter_routers(results)
        new_view(self.view, edit, text)


class RecoverJsLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        prefix = get_console_text(self.view).strip('\n').strip('/') + '/'

        try:
            text = json.loads(text)
        except:
            sublime.message_dialog('[error] Json data has error! Please check...')
        else:
            rets = ''
            for key in text.keys():
                rets += prefix + key + '.' + text[key] + '.js\n'
            panel_print(self.view, edit, rets)


# Text Edit
class RemoveSpecialCharsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        text = re.sub(r"(\ |,|\.|\?|<|>|:|;|\"|'|{|}|\[|\]|\\|~|!|@|#|$|%|^|&|\*|\(|\)|\+|-|=|)",'',text)        
        update_file(self.view, edit, text)


class RemoveSpecificStringCommand(sublime_plugin.TextCommand):
    def run(self, edit, str):
        text = get_buffer_text(self.view)
        if str == '[*]':
            text = re.sub(r"\[.+\]",'',text)
        if str == '(*)':
            text = re.sub(r"\(.+\)",'',text)
        if str == 'space':
            text = text.replace(' ','')
        update_file(self.view, edit, text)


class DeleteLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        buffers = get_buffer_text(self.view)
        delstr = get_console_text(self.view).strip('\n').split('\n')
        if len(delstr) == 0:
            sublime.message_dialog('[error] Please select input text and input finding strings')
            return

        text = ''
        for line in buffers.split('\n'):
            flag = False
            for ds in delstr:
                if ds in line or ds == line:
                    flag = True
                    break
            if flag == False:
                text += line + '\n'
        
        update_file(self.view, edit, text)


class SelectLinesCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        buffers = get_buffer_text(self.view)
        findstr = get_console_text(self.view).strip('\n').split('\n')
        if len(findstr) == 0:
            sublime.message_dialog('[error] Please select input text and input finding strings')
            return

        text = ''
        for line in buffers.split('\n'):
            for fs in findstr:
                if fs in line or fs == line:
                    text += line + '\n'
        
        new_view(self.view, edit, text)


class ReplaceKeyToValueCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        mapstr = get_console_text(self.view).strip('\n').replace(' => ','=>').split('\n')
        if len(mapstr) == 0:
            sublime.message_dialog('[error] Please select input text and input mapping strings(eg: a=>b)')
            return

        for line in mapstr:
            if '=>' in line:
                key, value = line.split('=>')
                if key == '': continue
                text = text.replace(key,value)
        
        new_view(self.view, edit, text)


class ReplaceValueToKeyCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        mapstr = get_console_text(self.view).strip('\n').replace(' => ','=>').split('\n')
        if len(mapstr) == 0:
            sublime.message_dialog('[error] Please select input text and input mapping strings(eg: a=>b)')
            return

        for line in mapstr:
            if '=>' in line:
                key,values = line.split('=>')
                values = values.split(',')
                
                for value in values:
                    if value == '': continue
                    text = text.replace(value,key)
        
        new_view(self.view, edit, text)


class SortAndUniqueTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        text = list(set(text.split('\n')))
        text = '\n'.join(sorted(text))
        update_file(self.view, edit, text)


# Text encode
class Base64EncodeTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        text = base64.b64encode(text.encode())        
        panel_print(self.view, edit, text.decode())


class Base64DecodeTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view)
        text = base64.b64decode(text.encode())
        panel_print(self.view, edit, text.decode())


class Base64EncodeLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        texts = get_buffer_text(self.view).strip('\n').split('\n')       
        lines = ''
        for line in texts:
            line = base64.b64encode(line.encode())
            lines += line.decode() + '\n'
        panel_print(self.view, edit, lines)


class Base64DecodeLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        texts = get_buffer_text(self.view).strip('\n').split('\n')       
        lines = ''
        for line in texts:
            line = base64.b64decode(line.encode())
            lines += line.decode() + '\n'
        panel_print(self.view, edit, lines)


class UrlEncodeDecodeTextCommand(sublime_plugin.TextCommand):
    def run(self, edit, cmd):
        text = get_buffer_text(self.view).replace('\r\n','\n').replace('\r','\n')
        if cmd == 'encode':
            text = quote(text)
        if cmd == 'decode':
            text = unquote(text)
        panel_print(self.view, edit, text.replace('%0A','\n'))


class Md5EncryptTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view).strip('\n')   
        text = hashlib.md5(text.encode()).hexdigest()
        panel_print(self.view, edit, text)


class Md5EncryptLineCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        texts = get_buffer_text(self.view).strip('\n').split('\n')       
        lines = ''
        for line in texts:
            lines += hashlib.md5(line.encode()).hexdigest() + '\n'
        panel_print(self.view, edit, lines)


# Command
class RunCmdCommand(sublime_plugin.TextCommand):
    def run(self, edit, cmd):
        text = get_buffer_text(self.view)
        global workdir
        file = write_file(workdir,text)
        cmd = cmd.replace('target.txt',file)
        exec_command(cmd)


class CurlDownloadFileCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        text = get_buffer_text(self.view).strip('\n')
        global workdir
        file = write_file(workdir,text)
        ticks = str(int(time.time()))

        workdir = os.path.join(HOME,'Desktop','work')
        dwdir = os.path.join(workdir,ticks)
        
        if os.path.exists(workdir) == False:
            os.mkdir(workdir)
            os.mkdir(dwdir)
        else:
            os.mkdir(dwdir)

        errurls = is_url(text.split('\n'))
        if len(errurls) > 0:
            sublime.message_dialog('[error] Urls are invaild! Please check...')
            panel_print(self.view, edit, '[-] The invaild urls:\n' + errurls)
            return

        if os.path.exists(workdir):
            if platform == 'windows':
                cmd = '"cd {dir} && FOR /f %f IN ({file}) DO curl -k -O %f"'.format(dir=dwdir,file=file)
            else:
                cmd = 'cd {dir};for line in $(cat {file});do curl -k -O ${line};done;'.format(dir=dwdir,file=file,line='{line}')
            exec_command(cmd)
        else:
            panel_print(self.view, edit, '[!] $HOME/Desktop/work folder not exists!')


# Format tools result
class FormatToolsResultCommand(sublime_plugin.TextCommand):
    def run(self, edit, tool):
        text = get_buffer_text(self.view)   
        global workdir
        if tool == 'nmap':
            file = write_file(workdir,text)
            text = format_nmap_open_port(file)

        if len(text) > 0:
            new_view(self.view, edit, text)


# Pentest help module
class PentestHelpModuleCommand(sublime_plugin.TextCommand):
    def run(self, edit, tool):
        if tool == 'upload':
            global file_upload_package
            text = file_upload_package

        new_view(self.view, edit, text, 'Markdown.sublime-syntax')


# Reserve shell tool
class ReverseShellToolsCommand(sublime_plugin.TextCommand):
    def run(self, edit, shell):
        ip_port = get_buffer_text(self.view)
        if shell == 'bash':
            text = reverse_shell_tools('bash',ip_port)
        if shell == 'sh':
            text = reverse_shell_tools('sh',ip_port)
        if shell == 'other':
            text =   reverse_shell_tools('other',ip_port)

        if len(text) > 0:
            new_view(self.view, edit, text, 'Bash.sublime-syntax')


# Input text
class InputTextCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        panel_print(self.view, edit, 'Input Text:\n')


# Setting config
class SettingXtoolsConfigCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        config_file = os.path.join(sublime.packages_path(),"Xtools","Context.sublime-menu")
        self.view.window().open_file(config_file)
        

# Notebook
class XtoolsNoteBookCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        notebook = os.path.join(sublime.packages_path(),"Xtools","Notebook.md")
        self.view.window().open_file(notebook)


# About Xtools
class AboutXtoolsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        tip = check_version(VERSION)
        sublime.message_dialog(ABOUT_XTOOLS.format(version=VERSION,tip=tip))


# Function lib

def get_buffer_text(view):
    site = Region(0, view.size())
    text = view.substr(site)
    return text


def region_to_text(view,regions):
    text = []
    for region in regions:
        text.append(view.substr(region))

    text = sorted(list(set(text)))
    return '\n'.join(text)


def get_console_text(view):
    panel = view.window().find_output_panel('exec')
    text = get_buffer_text(panel).replace('Input Text:\n','')
    return text


def panel_print(view, edit, text):
    view.window().destroy_output_panel('exec')
    panel = view.window().create_output_panel('exec')
    view.window().run_command('show_panel', {'panel': 'output.exec'})
    panel.run_command('insert', {'characters': text})


def new_view(view, edit, text, syntax=''):
    new_view = view.window().new_file(syntax=syntax)
    new_view.set_scratch(True)
    # 旧版本 Sublime Text
    # new_view.insert(edit, 0, text.strip())
    # 新版本 Sublime Text
    new_view.run_command('insert', {'characters': text.strip()})
    view.window().focus_view(new_view)


def update_file(view, edit, text):
    view.replace(edit, sublime.Region(0, view.size()), text)
