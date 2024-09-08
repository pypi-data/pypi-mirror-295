#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import json
import sys
import pymysql
import pandas as pd 
import paramiko
import re
import os
import platform

class Connection:
 
    def __init__(self, username='', password='', match_id='', verbose=False):
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'cross-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"'
        }
        self.resources = None
        self.username = username
        self.password = password
        self.match_id = match_id
        if self.login()['status'] == 0:
            self.login_token = self.login()['data']['token']
        else:
            print("log err:{}".format(self.login()['message']))
        
        if self.get_record()['status'] == 0:
            data = self.get_record()['data']
            self.uuid = data['match_info']['uuid']
            self.module_list = [module['id'] for module in data['match_modules']]
            self.owner_id = data['match_record']['id']
            self.vr_manage_url_token = data['vr_manage_url']['token']

            if self.get_playload()['status'] == 0:
                self.playload = self.get_playload()['data']['all_payload']
                # 清楚hosts之前的内容，windterm2.6.1已修复此bug
                # self.setclear()
                self.setvar()
                # 获取element_id和module_id的对应关系
                self.element_module_dict = self.get_module_elements(verbose)
            else:
                print("get playload err:{}".format(self.get_playload()['message']))
        else:
            print("get record err:{}".format(self.get_record()['message']))
        
    def login(self):
        """
        获取登录token
        """
        url = "https://api-prod.qingjiao.art/uc/api/token/v2"
        params = {
            'username': self.username,
            'password': self.password,
        }
        res = requests.post(url, headers = self.headers, params=params)
        data = json.loads(res.text)

        token = data['data']['token']
        return data
    
    def get_record(self):
        """
        获取owner_id、match_id和管理token
        """
        self.headers['Authorization'] = self.login_token
        url = 'https://api-prod.qingjiao.art/api/match/{}/record'.format(self.match_id)
        res = requests.get(url, headers = self.headers)
        data = json.loads(res.text)
        # data['data']
        return data
        
    def get_playload(self):
        """
        获取status接口的content数据
        """
        self.headers['Authorization'] = self.login_token
        url = 'https://api-prod.qingjiao.art/api/match/record/{}/payload'.format(self.owner_id)
        res = requests.get(url, headers = self.headers)
        data = json.loads(res.text)

        # data['data']
        return data
    
    def get_resource_list(self):
        """
        获取竞赛资源列表
        owner_id: 拥有者的id
        """
        ret = []
        self.headers['Authorization'] = self.login_token
        url = 'https://api-prod.qingjiao.art/api/match/record/{}/resource/list'.format(self.owner_id)
        res = requests.get(url, headers = self.headers)
        data = json.loads(res.text)
        if data['status'] != 0:
            print(data['message'])
            return
        
        resources = data['data']['resources']
        for i, res in enumerate(resources):
            host_name = {}
            host_name['resource_name'] = ' '.join(res['content']['name'].split()).replace("/", "-")
            host_name['resource_id'] = str(res['id'])
            ret.append(host_name)

        return ret
    
    def get_resource_status(self, url='https://api.region-bj02.qingjiao.link//api/v3/virtual-resource/all/status'):
        """
        获取竞赛资源的状态，包括ip、public_ip和password
        """
        ret = []
        # url = 'https://api.region-bj02.qingjiao.link//api/v3/virtual-resource/all/status'
        # url = 'https://api.region-zjk02.qingjiao.link//api/v3/virtual-resource/all/status'
        self.headers['Authorization'] = self.vr_manage_url_token
        data = {
            "content": self.playload
        }
        res = requests.post(url, headers = self.headers, data=data)
        data = json.loads(res.text)

        if data['code'] != 0:
            print(data['message'])
            return
        
        resources = data['data']
        for i, res in enumerate(resources):
            host_info = {}
            host_info['ip'] = res['ip']
            host_info['public_ip'] = res['public_ip']
            host_info['password'] = res['password']
            host_info['resource_id'] = str(res['extra'])
            ret.append(host_info)
        return ret
            
    def get_element_list(self, module_id):
        """
        获取模块的组成id
        """
        self.headers['Authorization'] = self.login_token
        start_url = 'https://api-prod.qingjiao.art/api/match/record/{}/module/{}/element/list'.format(self.owner_id, module_id)

        response = requests.get(url=start_url, headers=self.headers)
        data = json.loads(response.text)
        if data['status'] != 0:
            print(data['message'])
            return
        #ret = ['{}:{}'.format(element['name'], element['id']) for element in data['data']['elements']]
        return data['data']['elements']
    
    def get_module_elements(self, verbose=False):
        """
        获取所有的模块和组合id
        """
        ret = {}
        modules = self.module_list
        for module_id in modules:
            elements = self.get_element_list(module_id)
            for element in elements:
                ret[str(element['id'])] = str(module_id)
            elements_list = ['{}:{}'.format(element['name'], element['id']) for element in elements]
            if verbose:
                print("#"*136)
                print("module: {}, elements: {}".format(module_id, elements_list))
        
        return ret
    
    def get_exam_content(self):
        """
        获取竞赛中所有的模块的内容
        """
        for element_id in self.element_module_dict.keys():
            self.get_element_detail(element_id)
            
    def get_element_detail(self, element_id):
        """
        获取竞赛中题目的内容
        """
        self.headers['Authorization'] = self.login_token
        module_id = self.element_module_dict[element_id]
        start_url = 'https://api-prod.qingjiao.art/api/match/record/{}/module/{}/element/{}/detail'.format(self.owner_id, module_id, element_id)

        response = requests.get(url=start_url, headers=self.headers)
        data = json.loads(response.text)
        if data['status'] != 0:
            print(data['message'])
            return
        if not os.path.exists('./md/{}'.format(self.match_id)):
            # 目录不存在，创建目录
            os.makedirs('./md/{}'.format(self.match_id))

        # 保存单选题
        if 'content' in data['data']['element'].keys():
            contents = data['data']['element']['content']
            f = open('./md/{}/{}-{}-{}.txt'.format(self.match_id, self.match_id, module_id, element_id), 'w', encoding='utf8')
            for i, content in enumerate(contents):
                title = content['name']
                partA = content['options'][0]
                partB = content['options'][1]
                partC = content['options'][2] if len(content['options']) > 2 else ''
                partD = content['options'][3] if len(content['options']) > 3 else ''
                f.write(title + "," + partA + "," + partB + "," + partC + "," + partD + '\n')
            f.close()

        # 保存解答题
        if 'order_tasks' in data['data']['element'].keys():
            order_tasks = data['data']['element']['order_tasks']
            f = open('./md/{}/{}-{}-{}.md'.format(self.match_id, self.match_id, module_id, element_id), 'w', encoding='utf8')
            name_head =  data['data']['element']['name']
            description_head =  data['data']['element']['description']
            f.writelines("# " + name_head + "\n\n")
            f.writelines(description_head)
            f.writelines('\n\n---\n\n')
            for i, task in enumerate(order_tasks):
                name = task['name']
                description = task['description']
                f.writelines("## " + name + "\n\n")
                f.writelines(description)
                f.writelines('\n\n---\n\n')
                order_conditions = task['order_conditions']
                f.writelines("### 考核条件如下 :\n")
                for i, condition in enumerate(order_conditions):
                    name = condition['name']
                    condition_desc = condition['condition_desc']
                    recourseName = "、".join(condition['params'][0]['recourseName'])
                    f.writelines("{}.{}\n\n".format(i+1, name))
                    if name != condition_desc:
                        f.writelines(condition_desc+ "\n\n")
                    f.writelines("操作环境: " + recourseName + "\n\n")
            f.close()  
    
    def setvar(self, verbose=False):
        """
        获取对象的hostname和public_ip，写入本地hosts
        """
        df_name = pd.DataFrame(self.get_resource_list())
        url_master = 'https://api.region-bj02.qingjiao.link//api/v3/virtual-resource/all/status'
        url_slave = 'https://api.region-zjk02.qingjiao.link//api/v3/virtual-resource/all/status'
        if len(self.get_resource_status(url_master)) != 0:
            df_info = pd.DataFrame(self.get_resource_status(url_master))
        else:
            df_info = pd.DataFrame(self.get_resource_status(url_slave))
        
        df = pd.merge(df_name, df_info,on='resource_id')
        self.resources = df[[col for col in df.columns if col != 'resource_id']]
        print(df[[col for col in df.columns if col != 'resource_id']])

        # 清除之前hosts已有的内容
        if platform.system() == 'Windows':
            host_file = "C:/Windows/System32/drivers/etc/HOSTS"
        else:
            host_file = "/etc/hosts"

        with open(host_file, 'r', encoding='utf8') as f:
            lines = f.readlines()
        if '# Qingjiao Host Start\n' in lines:
            lines = lines[:lines.index('# Qingjiao Host Start\n')]
            with open(host_file, 'w', encoding='utf8') as f:
                f.writelines(lines)
        
        # 写入新的hosts
        with open(host_file, 'a+', encoding='utf8') as f:
            f.write("# Qingjiao Host Start\n")
            for index, row in df.iterrows():
                #if row['resource_name'] in ['Hadoop-Hive-Spark', 'Hadoop-Spark', 'Hadoop-hive']:
                #    f.write(row['public_ip']+" "+"hadoop000\n")
                f.write(row['public_ip']+" "+row['resource_name']+"\n")
        
    def setclear(self):
        """
        清除本地WindTerm的密钥记录,windter2.6.1已修复此bug
        """
        if platform.system() == 'Windows':
            sessions_file = 'D:/Portable/WindTerm_2.5.0/.wind/profiles/default.v10/terminal/user.sessions'
        with open(sessions_file, 'r', encoding='utf8') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            if not 'session.autoLogin' in line:
                new_lines.append(line)
        with open(sessions_file, 'w', encoding='utf8') as f:
            f.writelines(new_lines)
            
    def setbasic(self, verbose=False):
        """
        登录主机后的基本操作
        """
        # 远程执行setvar
        command = "cat > /usr/etx.txt <<EOF\n"
        for index, row in self.resources.iterrows():
            command = command + row['resource_name'] + "," + row['ip'] + "," + row['public_ip'] + "," + row['password'] + "\n"
        command = command + "EOF"
        
        for index, row in self.resources.iterrows():
            resource_name = row['resource_name']
            # 执行远程命令
            out,err = self.ssh_exec(resource_name=resource_name, command=command)
            
            if resource_name == 'master' or resource_name == 'slave1' or resource_name == 'slave2':
                print("{}-cluster".format(resource_name))
                download_command = "curl -o /etc/profile.d/my.sh -O -L https://gitee.com/yiluohan1234/vagrant_bigdata_cluster/raw/master/resources/bdcompetition/cluster.sh"
                source_command = "source /etc/profile"
                setvar_command = "setvar"
                out,err = self.ssh_exec(resource_name=resource_name, command=download_command)
                out,err = self.ssh_exec(resource_name=resource_name, command=source_command)
                out,err = self.ssh_exec(resource_name=resource_name, command=setvar_command)
                # 设置ip
                out,err = self.ssh_exec(resource_name=resource_name, command='source /etc/profile && setip')
            else:
                print("{}-single".format(resource_name))
                download_command = "curl -o /etc/profile.d/my.sh -O -L https://gitee.com/yiluohan1234/vagrant_bigdata_cluster/raw/master/resources/bdcompetition/single.sh && source /etc/profile"
                out,err = self.ssh_exec(resource_name=resource_name, command=download_command)
        
        print("setbasic success!")
        
    def clear(self):
        """
        删除my.sh
        """
        for index, row in self.resources.iterrows():
            resource_name = row['resource_name']
            # 执行远程命令
            out, err = self.ssh_exec(resource_name=resource_name, command='rm -rf /etc/profile.d/my.sh')
            
    def ssh_exec(self, resource_name, command):
        """
        远程执行命令
        """
        hostname_df = self.resources[self.resources['resource_name']==resource_name]
        hostname = hostname_df['public_ip'].values[0]
        port = '22'
        username = 'root'
        password = hostname_df['password'].values[0]
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=hostname, port=port, username=username, password=password)

            stdin, stdout, stderr = ssh.exec_command(command)
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            ssh.close()
        return out, err
    
    def get_check(self, resource_name):
        """
        获取远程的日志文件内容
        """
        hostname_df = self.resources[self.resources['resource_name']==resource_name]
        hostname = hostname_df['public_ip'].values[0]
        port = '22'
        username = 'root'
        password = hostname_df['password'].values[0]
        out, err = self.ssh_exec(resource_name=resource_name, command="echo $(ps -ef | grep aliyun-assist | grep aliyun-service | grep -v grep | awk '{print $8}'|xargs dirname)/log/aliyun_assist_main.log")
        # out, err = self.ssh_exec(resource_name=resource_name, command='source /etc/profile && getlog')
        file = out.replace('\n', '')
            
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            client.connect(hostname, port, username, password)
            sftp_client = client.open_sftp()
            remote_file = sftp_client.open(file, "r")
            file_content = remote_file.readlines()
            # lines = [line for line in file_content if "https://cn-beijing.axt.aliyun.com/luban/api/v1/task/finish" in line]
            lines = [line for line in file_content if "/luban/api/v1/task/finish" in line]
            ret_list = []
            for line in lines:
                line_str = line.replace("\\", "")
                json_match = re.search(r'{\s*"status":\s*(-?\d+),\s*"message":\s*".*?"\s*}', line_str)
                if json_match:
                    status_json = json_match.group(0)
                    status_data = json.loads(status_json)
                    ret_list.append(status_data)
            
            # 打印倒数3个JSON数据
            for data in ret_list[-3:]:
                print(data)

        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            remote_file.close()
            client.close()
    
    def upload(self, resource_name, local_file_path, remote_file_path):
        """
        获取远程的日志文件内容
        """
        hostname_df = self.resources[self.resources['resource_name']==resource_name]
        hostname = hostname_df['public_ip'].values[0]
        port = '22'
        username = 'root'
        password = hostname_df['password'].values[0]
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port, username, password)
            sftp = client.open_sftp()
            # 上传本地文件到远程服务器
            # 报错Failure：sftp.put("/tmp/xx.py", "/tmp/xx.py")
            sftp.put(local_file_path, remote_file_path)
        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            sftp.close()
            client.close()

    def download(self, resource_name, remote_file):
        """
        获取远程的日志文件内容
        """
        local_dir = './download/{}/'.format(self.match_id)
        if not os.path.exists(local_dir):
            # 目录不存在，创建目录
            os.makedirs(local_dir)

        file_name = remote_file.split('/')[-1]
        local_file = local_dir + file_name
        hostname_df = self.resources[self.resources['resource_name']==resource_name]
        hostname = hostname_df['public_ip'].values[0]
        port = '22'
        username = 'root'
        password = hostname_df['password'].values[0]
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname, port, username, password)
            sftp = client.open_sftp()
            # 上传本地文件到远程服务器
            # 报错Failure：sftp.put("/tmp/xx.py", "/tmp/xx.py")
            sftp.get(remote_file, local_file)
        except paramiko.AuthenticationException as auth_exception:
            print("Authentication failed: {}".format(auth_exception))
        except paramiko.SSHException as ssh_exception:
            print("SSH connection failed: {}".format(ssh_exception))
        except Exception as general_exception:
            print("An unexpected error occurred: {}".format(general_exception))
        finally:
            sftp.close()
            client.close()
    
    def getsql(self, resource_name, sql_name):
        """
        获取sql文件
        """
        download_sql = "curl -o /root/{}.sql -O -L https://gitee.com/yiluohan1234/vagrant_bigdata_cluster/raw/master/resources/bdcompetition/sql/{}.sql && source /etc/profile".format(sql_name, sql_name)
        out, err = self.ssh_exec(resource_name=resource_name, command=download_sql)
        print("upload sql")

    def setssh(self):
        """
        windows和linux免密登录
        """
        if platform.system() == 'Windows':
            username = os.environ.get('USERNAME')
            id_rsa_path = 'C:/Users/{}/.ssh/id_rsa.pub'.format(username)
            ssh_known_file = 'C:/Users/{}/.ssh/known_hosts'.format(username)
            ssh_config_file = 'C:/Users/{}/.ssh/config'.format(username)
        else:
            id_rsa_path = '/root/.ssh/id_rsa.pub'
            ssh_known_file = '/root/.ssh/known_hosts'

        for index, row in self.resources.iterrows():
            resource_name = row['resource_name']
            self.upload(resource_name, id_rsa_path, '/root/id_rsa.pub')
            out, err = self.ssh_exec(resource_name, 'source /etc/profile && cat /root/id_rsa.pub >> ~/.ssh/authorized_keys && rm -rf /root/id_rsa.pub')

        # 清除之前已有的内容
        if platform.system() == 'Windows':
            with open(ssh_config_file, 'r', encoding='utf8') as f:
                lines = f.readlines()
            if '# Qingjiao Host Start\n' in lines:
                lines = lines[:lines.index('# Qingjiao Host Start\n')]
                with open(ssh_config_file, 'w', encoding='utf8') as f:
                    f.writelines(lines)

            # 写入新的ssh_config
            with open(ssh_config_file, 'a+', encoding='utf8') as f:
                f.write("# Qingjiao Host Start\n")
                for index, row in self.resources.iterrows():
                    f.write("Host " + row['resource_name'] + "\n")
                    f.write("    HostName " + row['public_ip'] + "\n")
                    f.write("    Port 22\n")
                    f.write("    User root\n")
                    f.write("    IdentityFile ~/.ssh/id_rsa\n\n")

        # 清除known中已存的信息
        with open(ssh_known_file, 'r', encoding='utf8') as f:
            lines = f.readlines()
        new_lines = []
        for line in lines:
            is_exist = False
            for index, row in self.resources.iterrows():
                resource_name = row['resource_name'].lower()
                if resource_name in line :
                    is_exist = True
                    break
            if not is_exist:
                new_lines.append(line)
        with open(ssh_known_file, 'w', encoding='utf8') as f:
            f.writelines(new_lines)

    def get_command(self, title):
        ret = []
        try:
            db=pymysql.connect(host='localhost',user='root',passwd='199037wW', port=3306, db='hongya',charset='utf8')
            cursor = db.cursor()
            sql = "select * from bd_command where title like '%{}%'".format(title)
            cursor.execute(sql)
            data_list = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()
        for data in data_list:
            #print(data)
            ret.append({'type':data[1], 'title':data[2], 'command': data[3]})
        if len(ret) == 0:
            print("no data")
            return
        return ret

    def get_abcd(self, title):
        ret = []
        try:
            db=pymysql.connect(host='localhost',user='root',passwd='199037wW', port=3306, db='hongya',charset='utf8')
            cursor = db.cursor() 
            sql = "select * from bd_practice where title like '%{}%'".format(title)
            cursor.execute(sql)
            data_list = cursor.fetchall()
        except Exception as e:
            print(e)
        finally:
            db.commit()
            db.close()
        for data in data_list:
            #print(data)
            ret.append({'type':data[2], 'answer':data[7], 'title':data[1], 'A':data[3], 'B':data[4], 'C':data[5], 'D':data[6]})
        if len(ret) == 0:
            print("no data")
            return
        return ret