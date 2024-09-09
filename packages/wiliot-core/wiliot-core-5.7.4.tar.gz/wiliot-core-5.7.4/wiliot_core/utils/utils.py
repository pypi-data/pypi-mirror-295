#  """
#    Copyright (c) 2016- 2024, Wiliot Ltd. All rights reserved.
#
#    Redistribution and use of the Software in source and binary forms, with or without modification,
#     are permitted provided that the following conditions are met:
#
#       1. Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#
#       2. Redistributions in binary form, except as used in conjunction with
#       Wiliot's Pixel in a product or a Software update for such product, must reproduce
#       the above copyright notice, this list of conditions and the following disclaimer in
#       the documentation and/or other materials provided with the distribution.
#
#       3. Neither the name nor logo of Wiliot, nor the names of the Software's contributors,
#       may be used to endorse or promote products or services derived from this Software,
#       without specific prior written permission.
#
#       4. This Software, with or without modification, must only be used in conjunction
#       with Wiliot's Pixel or with Wiliot's cloud service.
#
#       5. If any Software is provided in binary form under this license, you must not
#       do any of the following:
#       (a) modify, adapt, translate, or create a derivative work of the Software; or
#       (b) reverse engineer, decompile, disassemble, decrypt, or otherwise attempt to
#       discover the source code or non-literal aspects (such as the underlying structure,
#       sequence, organization, ideas, or algorithms) of the Software.
#
#       6. If you create a derivative work and/or improvement of any Software, you hereby
#       irrevocably grant each of Wiliot and its corporate affiliates a worldwide, non-exclusive,
#       royalty-free, fully paid-up, perpetual, irrevocable, assignable, sublicensable
#       right and license to reproduce, use, make, have made, import, distribute, sell,
#       offer for sale, create derivative works of, modify, translate, publicly perform
#       and display, and otherwise commercially exploit such derivative works and improvements
#       (as applicable) in conjunction with Wiliot's products and services.
#
#       7. You represent and warrant that you are not a resident of (and will not use the
#       Software in) a country that the U.S. government has embargoed for use of the Software,
#       nor are you named on the U.S. Treasury Department’s list of Specially Designated
#       Nationals or any other applicable trade sanctioning regulations of any jurisdiction.
#       You must not transfer, export, re-export, import, re-import or divert the Software
#       in violation of any export or re-export control laws and regulations (such as the
#       United States' ITAR, EAR, and OFAC regulations), as well as any applicable import
#       and use restrictions, all as then in effect
#
#     THIS SOFTWARE IS PROVIDED BY WILIOT "AS IS" AND "AS AVAILABLE", AND ANY EXPRESS
#     OR IMPLIED WARRANTIES OR CONDITIONS, INCLUDING, BUT NOT LIMITED TO, ANY IMPLIED
#     WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY, NONINFRINGEMENT,
#     QUIET POSSESSION, FITNESS FOR A PARTICULAR PURPOSE, AND TITLE, ARE DISCLAIMED.
#     IN NO EVENT SHALL WILIOT, ANY OF ITS CORPORATE AFFILIATES OR LICENSORS, AND/OR
#     ANY CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
#     OR CONSEQUENTIAL DAMAGES, FOR THE COST OF PROCURING SUBSTITUTE GOODS OR SERVICES,
#     FOR ANY LOSS OF USE OR DATA OR BUSINESS INTERRUPTION, AND/OR FOR ANY ECONOMIC LOSS
#     (SUCH AS LOST PROFITS, REVENUE, ANTICIPATED SAVINGS). THE FOREGOING SHALL APPLY:
#     (A) HOWEVER CAUSED AND REGARDLESS OF THE THEORY OR BASIS LIABILITY, WHETHER IN
#     CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE);
#     (B) EVEN IF ANYONE IS ADVISED OF THE POSSIBILITY OF ANY DAMAGES, LOSSES, OR COSTS; AND
#     (C) EVEN IF ANY REMEDY FAILS OF ITS ESSENTIAL PURPOSE.
#  """

import os
import csv
from appdirs import user_data_dir
import logging
import json
import pathlib
import re
import datetime

try:
    from tkinter import Tk, Label, Button, ttk
    import PySimpleGUI as SimGUI
except Exception as e:
    print('could not import PySimpleGUI due to {}'.format(e))

PACKET_PREFIXES_MAPPING = ('process_packet', 'full_packet')


class WiliotDir:
    def __init__(self) -> None:
        self.local_appdata_dir = ''
        self.wiliot_root_path = ''
        self.common_dir_path = ''
        self.config_dir_path = ''
        self.user_config_path = ''
        self.tester_subdirectories = ['results', 'logs', 'configs']
        
        self.set_dir()
        self.create_dir(self.local_appdata_dir)
        self.create_dir(self.wiliot_root_path)
        self.create_dir(self.common_dir_path)
        self.create_dir(self.config_dir_path)
    
    def set_dir(self):
        try:
            if 'WILIOT_APP_ROOT_PATH' in os.environ.keys():
                print(os.environ['WILIOT_APP_ROOT_PATH'])
                self.wiliot_root_path = os.environ['WILIOT_APP_ROOT_PATH']
            else:
                self.local_appdata_dir = user_data_dir()
                self.wiliot_root_path = os.path.abspath(os.path.join(self.local_appdata_dir, 'wiliot'))
            
            self.common_dir_path = os.path.abspath(os.path.join(self.wiliot_root_path, 'common'))
            self.config_dir_path = os.path.abspath(os.path.join(self.common_dir_path, 'configs'))
            self.user_config_path = os.path.abspath(os.path.join(self.config_dir_path, 'user_configs.json'))
        
        except Exception as e:
            logging.warning('Error loading environment or getting in from OS, supporting Windows, Linux and MacOS '
                            '({})'.format(e))
    
    @staticmethod
    def create_dir(path):
        if not os.path.exists(path):
            os.makedirs(path)
    
    def create_tester_dir(self, tester_name):
        tester_path = self.get_tester_dir(tester_name)
        self.create_dir(tester_path)
        
        for subdir in self.tester_subdirectories:
            self.create_dir(tester_path + '/' + subdir)
    
    def get_tester_dir(self, tester_name):
        wiliot_path = self.wiliot_root_path
        tester_path = os.path.abspath(os.path.join(wiliot_path, tester_name))
        return tester_path
    
    def get_dir(self):
        return self.wiliot_root_path, self.common_dir_path, self.config_dir_path, self.user_config_path
    
    def get_wiliot_root_app_dir(self):
        return self.wiliot_root_path
    
    def get_common_dir(self):
        return self.common_dir_path
    
    def get_config_dir(self):
        return self.config_dir_path
    
    def get_user_config_file(self, client_type=None):
        if client_type is None:
            return self.user_config_path
        return self.user_config_path.replace('.json', f'_{client_type}.json')


def open_json(folder_path, file_path, default_values=None):
    """
    opens config json
    :type folder_path: string
    :param folder_path: the folder path which contains the desired file
    :type file_path: string
    :param file_path: the file path which contains the json
            (including the folder [file_path = folder_path+"json_file.json"])
    :type default_values: dictionary
    :param default_values: default values for the case of empty json
    :return: the desired json object
    """
    if not os.path.exists(folder_path):
        pathlib.Path(folder_path).mkdir(parents=True, exist_ok=True)
    
    file_exists = os.path.isfile(file_path)
    if not file_exists or os.stat(file_path).st_size == 0:
        # save the default values to json
        with open(file_path, "w") as out_file:
            json.dump(default_values, out_file)
        
        return json.load(open(file_path, "rb"))
    else:
        with open(file_path) as f:
            json_content = f.read()
        if len(json_content) == 0:
            with open(file_path, "w") as out_file:
                json.dump(default_values, out_file)
            json_content = json.load(open(file_path, "rb"))
        else:
            json_content = json.loads(json_content)
        return json_content


def valid_packet_start(msg):
    '''
    Function to check if the packet starts with 'process_packet' or 'full_packet', if it is, it will return True
    If
    '''
    pattern = r'(' + '|'.join(PACKET_PREFIXES_MAPPING) + r')\("(.*?)"\)'
    match = re.search(pattern, msg)

    return match.group(2) if match else ''


def credentials_gui(client_type=None, owner_id=None, env=None):
    """
    open GUI for getting api_key from user
    :param client_type: the cloud client type. relevant if you have different api key for several client,
                       which will be save in different yser_config files
    :type client_type: str
    :return: the user input, dict with api_key, owner_id and env
    :rtype: dict
    """
    if client_type is None:
        client_type = 'DEFAULT'
    layout = [
        [SimGUI.Text('Please enter your Wiliot API key')],
        [SimGUI.Text(f'Client Type: {client_type}')],
        [SimGUI.Text('API key:'),
         SimGUI.InputText('', key='api_key')],
        [SimGUI.Text('owner id (optional):'),
         SimGUI.InputText('' if owner_id is None else owner_id, key='owner_id')],
        [SimGUI.Text('environment (optional):'),
         SimGUI.InputCombo(('prod', 'test', 'dev'), default_value='prod' if env is None else env, key='env')],
        [SimGUI.Submit()]]
    
    window = SimGUI.Window('User Credentials', layout)
    while True:
        event, values = window.read()
        if event == 'Submit':
            break
        elif event is None:
            print('User exited the program')
            window.close()
            break
    
    window.close()
    return values


def check_user_config_is_ok(owner_id=None, env=None, client_type=None):
    """
    check user credentials
    :param owner_id: use the key of the specified owner id
    :type owner_id: str or None
    :param env: use the key of the specified environment
    :type env: str or None
    :param client_type: if specified the credential will be read/write from the same use config file,
                        but with the specified suffix
    :type client_type: str or None
    :return: user_config_file_path - the file path,
             api_key -the key,
             is_success - True if the credentials we entered correctly
    :rtype: tuple
    """
    # Create wiliot appdata directory if not exists:
    is_success = True
    auth_gui_is_needed = False
    api_key = None
    cfg_data = []
    env_dirs = WiliotDir()
    config_dir_path = env_dirs.get_config_dir()
    user_config_file_path = env_dirs.get_user_config_file(client_type)
    if env is not None:
        env = env.lower()
    if env == '':
        env = 'prod'
    if env == 'non-prod':
        env = 'test'
    
    if not os.path.isdir(config_dir_path):
        pathlib.Path(config_dir_path).mkdir(parents=True, exist_ok=True)

    if os.path.exists(user_config_file_path):
        cfg_data = open_json(folder_path=config_dir_path, file_path=user_config_file_path)
        try:
            api_key_list = cfg_data['api_key']
            env_list = cfg_data['env']
            owner_list = cfg_data['owner_id']
            env_list = [env_element if env_element != 'non-prod' else 'test' for env_element in env_list]
            if not isinstance(api_key_list, list) or api_key_list == []:
                print('api key is missing. Please enter it manually')
                is_success = False
                auth_gui_is_needed = True
            elif (owner_id is not None and owner_id not in owner_list) or \
                    (env is not None and env not in env_list):
                print('api key does not match the request owner id or env. Please enter it manually')
                auth_gui_is_needed = True
            else:
                api_key = [k for i, k in enumerate(api_key_list)
                           if (owner_id is None or owner_id == owner_list[i]) and
                           (env is None or env == env_list[i])]
                if api_key == []:
                    print('could not find the api key for the specified environment and owner id')
                    auth_gui_is_needed = True
                api_key = api_key[0]
        except Exception as e:
            auth_gui_is_needed = True
            print("Config file is not readable at path {}. Exception {}\n Please enter new credentials".format(
                user_config_file_path, e))
    else:
        print("Config file user_configs.json doesn't exist at {}\n".format(config_dir_path))
        auth_gui_is_needed = True
    
    while auth_gui_is_needed:
        auth_gui_is_needed = False
        values = credentials_gui(client_type, owner_id, env)
        api_key = values['api_key']
        if api_key == '':
            print('api key is missing. Please try again\n')
            auth_gui_is_needed = True
        elif api_key is None:
            is_success = False
        else:
            with open(user_config_file_path, 'w') as cfg:
                if isinstance(cfg_data, dict):
                    for k in values.keys():
                        if k in cfg_data.keys() and isinstance(cfg_data[k], list):
                            cfg_data[k].append(values[k])
                        else:
                            cfg_data[k] = [values[k]]
                    json.dump(cfg_data, cfg)
                else:
                    json.dump({'api_key': [api_key], 'owner_id': [values['owner_id']], 'env': [values['env']]}, cfg)
            is_success = True

    return user_config_file_path, api_key, is_success


def csv_to_dict(path=None):
    """
    convert csv to dictionary (arranged by columns)
    :param path: the csv path
    :type path: str
    :return: the data as dictionary
    :rtype: dict
    """
    if path:
        with open(path, 'r') as f:
            reader = csv.DictReader(f, delimiter=',')
            col_names = reader.fieldnames
            data_out = {col: [] for col in col_names}
            try:
                for row in reader:
                    for col in col_names:
                        data_out[col].append(row[col])
            except Exception as e:
                print("couldn't load csv due to {}".format(e))
        return data_out
    else:
        print('please provide a path')
        return None


def set_logger(app_name, dir_name='', file_name='', common_run_name=None):
    if not isinstance(app_name, str) or app_name == '':
        raise Exception(f'app_name must be a string, better to use the actuall application name: {app_name}')
    logger = logging.getLogger(app_name)

    formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    wiliot_dir = WiliotDir()
    if dir_name == '':
        dir_name = re.sub(r'(?<!^)(?=[A-Z])', '_', app_name).lower()

    logger_path = os.path.join(wiliot_dir.get_wiliot_root_app_dir(), dir_name)
    if not os.path.isdir(logger_path):
        os.mkdir(logger_path)

    if common_run_name is None:
        if file_name == '':
            file_name = dir_name + '_log'
        common_run_name = f'{file_name}_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}'
    else:
        logger_path = os.path.join(logger_path, common_run_name)
        if not os.path.isdir(logger_path):
            os.mkdir(logger_path)

    logger_path = os.path.join(logger_path, f'{common_run_name}.log')
    file_handler = logging.FileHandler(logger_path, mode='a')
    file_formatter = logging.Formatter('%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', '%H:%M:%S')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.INFO)
    return logger_path, logger


class GetApiKey(object):
    def __init__(self, owner_id=None, env=None, client_type=None, gui_type='ttk'):
        self.owner_id = owner_id
        self.env = env
        self.fix_env_string()
        self.api_key_values = {}
        self.user_config_file_path = self.get_config_path(client_type)
        auth_gui_is_needed, api_key, cfg_data = self.check_file()
        if auth_gui_is_needed:
            gui_type = gui_type if gui_type is not None else 'PySimpleGui'
            if gui_type == 'PySimpleGui':
                self.api_key_values = credentials_gui(client_type, self.owner_id, self.env)
                self.save_api_key(cfg_data)
            elif gui_type == 'ttk':
                self.popup_key(client_type, cfg_data)
            else:
                raise Exception(f'gui type: {gui_type} is not supported please select: PySimpleGui, ttk')
        else:
            self.api_key_values = {'api_key': api_key, 'owner_id': self.owner_id, 'env': self.env}

    def get_api_key(self):
        return self.api_key_values['api_key'] if 'api_key' in self.api_key_values else ''

    def get_config_path(self, client_type):
        env_dirs = WiliotDir()
        config_dir_path = env_dirs.get_config_dir()
        if not os.path.isdir(config_dir_path):
            pathlib.Path(config_dir_path).mkdir(parents=True, exist_ok=True)

        return env_dirs.get_user_config_file(client_type)

    def fix_env_string(self):
        if self.env is not None:
            self.env = self.env.lower()
        if self.env == '':
            self.env = 'prod'
        if self.env == 'non-prod':
            self.env = 'test'

    def check_file(self):
        auth_gui_is_needed = False
        api_key = None
        cfg_data = []

        if os.path.exists(self.user_config_file_path):
            cfg_data = open_json(folder_path=os.path.dirname(self.user_config_file_path),
                                 file_path=self.user_config_file_path)
            try:
                api_key_list = cfg_data['api_key']
                env_list = cfg_data['env']
                owner_list = cfg_data['owner_id']
                env_list = [env_element if env_element != 'non-prod' else 'test' for env_element in env_list]
                if not isinstance(api_key_list, list) or api_key_list == []:
                    print('api key is missing. Please enter it manually')
                    auth_gui_is_needed = True
                elif (self.owner_id is not None and self.owner_id not in owner_list) or \
                        (self.env is not None and self.env not in env_list):
                    print('api key does not match the request owner id or env. Please enter it manually')
                    auth_gui_is_needed = True
                else:
                    api_key = [k for i, k in enumerate(api_key_list)
                               if (self.owner_id is None or self.owner_id == owner_list[i]) and
                               (self.env is None or self.env == env_list[i])]
                    if api_key == []:
                        print('could not find the api key for the specified environment and owner id')
                        auth_gui_is_needed = True
                    api_key = api_key[0]
            except Exception as e:
                auth_gui_is_needed = True
                print("Config file is not readable at path {}. Exception {}\n Please enter new credentials".format(
                    self.user_config_file_path, e))
        else:
            print("Config file user_configs.json doesn't exist {}\n".format(self.user_config_file_path))
            auth_gui_is_needed = True

        return auth_gui_is_needed, api_key, cfg_data

    def popup_key(self, client_type, cfg_data):
        default_font = ("Helvetica", 10)
        popup = Tk()
        popup.eval('tk::PlaceWindow . center')
        popup.wm_title('Missing API key')
        client_type = client_type if client_type is not None else 'DEFAULT'

        def quit_tester():
            try:
                popup.destroy()
            except Exception as e:
                print(e)
                exit(1)

        popup.protocol("WM_DELETE_WINDOW", quit_tester)

        def ok():
            api_key = c1.get()
            self.api_key_values = {'api_key': api_key, 'owner_id': self.owner_id, 'env': self.env}
            self.save_api_key(cfg_data)
            popup.destroy()

        l1 = Label(popup, text=f'Get API KEY for:\n\n'
                               f'ClientType: {client_type}\nOwner: {self.owner_id}\nEnv: {self.env}', font=default_font)
        l1.grid(row=2, column=0, padx=10, pady=10, columnspan=5)

        l4 = Label(popup, text='API Key:', font=default_font)
        l4.grid(row=6, column=0, padx=10, pady=10)
        c1 = ttk.Combobox(popup, state='normal', width=30)
        c1.grid(row=7, column=0, padx=10, pady=15)
        b3 = Button(popup, text="OK", command=ok, height=1, width=10)
        b3.grid(row=8, column=0, padx=10, pady=10)
        popup.mainloop()

    def save_api_key(self, cfg_data):
        api_key = self.get_api_key()
        if api_key:
            with open(self.user_config_file_path, 'w') as cfg:
                if isinstance(cfg_data, dict):
                    for k in self.api_key_values.keys():
                        if k in cfg_data.keys() and isinstance(cfg_data[k], list):
                            cfg_data[k].append(self.api_key_values[k])
                        else:
                            cfg_data[k] = [self.api_key_values[k]]
                    json.dump(cfg_data, cfg)
                else:
                    value_to_save = {k: [v] for k, v in self.api_key_values.items()}
                    json.dump(value_to_save, cfg)
        else:
            print('api key is missing. Please try again\n')


if __name__ == '__main__':
    k = GetApiKey(owner_id='hi', env='test')
    print(k.get_api_key())
