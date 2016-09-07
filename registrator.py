# -*- coding: utf-8 -*-
import os
from stat import S_ISDIR
import hashlib


class PluginsRegistrator:
    def __init__(self):
        self.modules = []
        self.plugins_path = 'plugins'
        self.plugins_directory = os.getcwd() + '/' + self.plugins_path
        self.signature_check = PluginSignatureCheck()

    def get_modules(self):
        return self.modules

    def get_directory_content(self, directory):
        return os.listdir(directory)

    def get_plugins(self):
        plug = []
        plugins = self.get_directory_content(self.plugins_directory)
        for plugin in plugins:
            plugin_path = self.plugins_directory + '/' + plugin
            stat_info = os.stat(plugin_path)
            mode = stat_info.st_mode
            if S_ISDIR(mode):
                modules = self.get_modules_names(plugin_path)
                for module in modules:
                    plug.append(module)
        return plug

    def get_modules_names(self, directory):
        modules = []
        directory_content = self.get_directory_content(directory)
        for file in directory_content:
            if file.endswith('.py'):
                module_name = file[: -3]
                if module_name != "base" and module_name != "__init__":
                    modules.append(module_name)
        return modules

    def register_plugins(self):
        plugins_name = self.get_plugins()
        for plugin in plugins_name:
            if self.check_authenticity(self.plugins_directory + '/' + plugin):
                self.package_obj = __import__(self.plugins_path + '.' + plugin + '.' + plugin)
                self.modules.append(plugin)

    def check_authenticity(self, plugin_name):
        return self.signature_check.start(plugin_name)


class PluginSignatureCheck:
    def start(self, plugin_name):
        self.plugin_name = plugin_name
        plugin_files = os.listdir(self.plugin_name)
        self.md5_sum = ''
        for file in plugin_files:
            if file.endswith('.py'):
                self.add_md5_sum(self.plugin_name + '/' + file)
        self.time = str(self.get_time())
        return self.check_signature()

    def add_md5_sum(self, filename):
        md5_sum = ''
        file = open(filename, 'rb')
        try:
            file_content = file.read()
            md5_sum += hashlib.md5(file_content).hexdigest()
            #print(md5_sum)
            self.md5_sum += md5_sum
        finally:
            file.close()

    def get_time(self):
        directory_info = os.lstat(self.plugin_name)
        return directory_info.st_mtime

    def check_signature(self):
        file = open(self.plugin_name + '/signature.txt', mode='r')
        signature = file.readlines()
        file.close()
        if (signature[0] == self.md5_sum + '\n') & (signature[1] == self.time):
            return True
        else:
            return False

if __name__ == '__main__':
    register = PluginsRegistrator()
    register.register_plugins()
    #sign = PluginSignatureCheck()
    #res = sign.start('/home/oksana/PycharmProjects/oop3/plugins/json_serialization')
    #print(res)
