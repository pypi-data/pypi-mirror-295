from pathlib import Path
import subprocess
import yaml

class Ras_connection:
    def __init__(self, version, arch, ras_hostname='localhost', ras_port='1545', cluster_hostname='localhost', cluster_port='1540') -> None:
        
        self._ras_instance  = None
        self.arch           = arch
        self.version        = version
        self.cluster_name   = ''
        self.ras_hostname   = ras_hostname
        self.ras_port       = ras_port
        self.cluster_hostname   = cluster_hostname
        self.cluster_port       = cluster_port
        self.ras_run_locally    = True

        if not arch == '64':
            self.execpath = Path('C:/Program Files (x86)/', "1cv8", version, "bin")
        else:
            self.execpath = Path('C:/Program Files/', "1cv8", version, "bin")
        self._check_path_exist(self.execpath, 'Платформа 1С')
        
        if self.ras_hostname == 'localhost':
            self.ras_path    = Path(self.execpath, 'ras.exe')
            self._check_path_exist(self.ras_path, 'Сервер RAS')
        else:
            self.ras_run_locally = False
        
        self.rac_path    = Path(self.execpath, 'rac.exe')
        self._check_path_exist(self.rac_path, 'Консоль RAC')

        pass

    def __del__(self):
        if not self._ras_instance is None:
            self._ras_instance.terminate()
        print('  Подключение к серверу администрирования RAS уничтожено!')

    def _check_path_exist(self, path_to_check, info = ""):
        if not path_to_check.exists():
            raise AttributeError(f"Не найдено: {info}! Путь {path_to_check}")

    def _execute_cli(self, params):
        ret = subprocess.run(params, text=True, capture_output=True, encoding='cp866')
        str_out  = ret.stdout.encode("utf_8").decode("utf_8")
        #if ret.stdout != '':
        #    print(f'    Ответ RAS сервера: {str_out}')
        str_err  = ret.stderr.encode("utf_8").decode("utf_8")
        assert ret.returncode == 0, 'Обращение к RAS закончилось ошибкой. Описание ошибки: ' + str_err
        return str_out

    def _RAS_start_process(self):
        ret = False
        if self._ras_instance is None:
            command = [self.ras_path]
            command.append('cluster')
            command.append(f'--port={self.ras_port}')
            command.append(f'{self.cluster_hostname}:{self.cluster_port}')
            print(command)
            self._ras_instance = subprocess.Popen(command)
            if self._ras_instance.returncode == None:
                print(' Запустили локальный сервер RAS')
                ret = True
            else:
                self._ras_instance   = None
                print(' Не удалось запустить сервер RAS!')
        return ret

    def get_cluster_by_hostname(self, cluster_hostname):
        self.cluster_hostname = cluster_hostname
        if self.ras_run_locally and self._ras_instance is None:
            assert self._RAS_start_process(), 'Не удалось запустить RAS сервер!'
        
        return Ras_cluster(self, cluster_hostname)

class Ras_cluster:
    def __init__(self, ras_connection, cluster_hostname = None, id = None) -> None:
        self.ras_connection = ras_connection
        self.cluster = ''
        self.host    = ''
        self.port    = ''
        self.name    = ''
        self.expiration_timeout    = ''
        self.bases   = []
        if not cluster_hostname == None:
            self.host = cluster_hostname
            self.get_by_hostname(cluster_hostname)
    
    def set_properties(self, data):
        for key in data:
            try:
                self.__setattr__(key, data[key])
            except:
                pass
            # print(key, data[key])

    def get_by_hostname(self, cluster_hostname):

        assert not cluster_hostname == None, 'Hostname of cluster is None'
        self.host = cluster_hostname

        print(f'    Начинаем получение объекта кластера по имени {self.host}')
        ras = self.ras_connection
        ret_stdout = ras._execute_cli([ras.rac_path, 'cluster', 'list', f'{ras.ras_hostname}:{ras.ras_port}'])
       
        data = yaml.safe_load(ret_stdout)
        self.set_properties(data)

        print(f'    Начинаем получение списка баз кластера по имени {self.host}')

        ret_stdout = ras._execute_cli([ras.rac_path, 'infobase', 'summary', 'list', f'--cluster={self.get_id()}'])
       
        list_bases  = ret_stdout.split('\n\n')
        for yaml_base in list_bases:
            if yaml_base == '':
                continue
            data = yaml.safe_load(yaml_base)
            # data = yaml_base.split('\n')
            self.bases.append(Ras_base(self, data['name'], data['infobase']))

    def get_base_by_name(self, base_name):
        print(f'    Начинаем получение базы по имени {base_name}')
        ret_value   = None
        for base_obj in self.bases:
            if base_obj.name == base_name:
                ret_value = base_obj
                break
        return ret_value
        

    def get_id(self):
        return self.cluster
            

class Ras_base:
    def __init__(self, cluster, name=None, id=None) -> None:
        self._cluster      = cluster
        self.id            = id
        self.name          = name
        self.descr      = ''
        self.username   = ''
        self.passwood   = ''

    def set_properties(self, data):
        for key in data:
            try:
                self.__setattr__(key, data[key])
            except:
                pass
            # print(key, data[key])

    def set_credentials(self, username, passwood):
        self.username   = username
        self.passwood   = passwood
    
    def get_info(self, username='', passwood=''):

        print(f'Получаем свойства информационной базы {self.name}')
        if not (username == '' or passwood == ''):
            self.set_credentials(username, passwood)
        cluster = self._cluster
        ras = cluster.ras_connection
        ret_stdout = ras._execute_cli([ras.rac_path, 'infobase', 'info', f'--infobase={self.id}', 
                                       f'--infobase-user={self.username}', 
                                       f'--infobase-pwd={self.passwood}', 
                                       f'--cluster={cluster.get_id()}'])
       
        data = yaml.safe_load(ret_stdout.replace('"', "'"))
        self.set_properties(data)

    def create(self):
        """Not implemented yet"""
        raise 'Not implemented yet'

    def drop(self):
        """Not implemented yet"""
        raise 'Not implemented yet'
    
    def update_properties(self):

        print(f'Обновляем свойства информационной базы {self.name}')
        cluster = self._cluster
        ras = cluster.ras_connection
        param_list  = [ras.rac_path,
                       'infobase',
                       'info',
                        f'--infobase={self.id}', 
                        f'--infobase-user={self.username}', 
                        f'--infobase-pwd={self.passwood}', 
                        f'--cluster={cluster.get_id()}']
        
        ret_stdout = ras._execute_cli(param_list)
        data = yaml.safe_load(ret_stdout)
        param_list  = [ras.rac_path,
                       'infobase',
                       'update',
                        f'--infobase={self.id}', 
                        f'--infobase-user={self.username}', 
                        f'--infobase-pwd={self.passwood}', 
                        f'--cluster={cluster.get_id()}']
        need_update = False
        for key in data:
            try:
                new_value   = self.__getattribute__(key)
                if not new_value == data[key]:
                    print(f'key:{key}. old value is {data[key]}, new value is {new_value}')
                    need_update = True
                    param_list.append(f'--{key}={new_value}')
            except:
                pass
        if need_update:
            ret_stdout = ras._execute_cli(param_list)
            print('properties of infobase has been updated')
    
    def deny_sessions(self, date_from=None, date_to=None, permission_code=None, message = ''):
        """Метод устанвливает блокировку информационной базы """
        self.__setattr__('denied-from', date_from.strftime('%Y-%m-%dT%H:%M:%S'))
        self.__setattr__('denied-to', date_to.strftime('%Y-%m-%dT%H:%M:%S'))
        self.__setattr__('denied-message', message)
        self.__setattr__('permission-code', permission_code)
        self.__setattr__('sessions-deny', 'on')
        self.update_properties()

    def allow_sessions(self):
        """Метод снимает блокировку информационной базы """
        self.__setattr__('denied-from', '')
        self.__setattr__('denied-to', '')
        self.__setattr__('denied-message', '')
        self.__setattr__('permission-code', '')
        self.__setattr__('sessions-deny', 'off')
        self.update_properties()

    def deny_scheduled_jobs(self):
        """Метод устанавливает блокировку регламентных заданий """
        self.__setattr__('scheduled-jobs-deny', 'on')
        self.update_properties()
 
    def allow_scheduled_jobs(self):
        """Метод снимает блокировку регламентных заданий """
        self.__setattr__('scheduled-jobs-deny', 'off')
        self.update_properties()

    def get_sessions_list(self):
        """Method return list of active sessions for base"""
        cluster = self._cluster
        ras = cluster.ras_connection
        param_list  = [ras.rac_path,
                       'session',
                       'list',
                        f'--infobase={self.id}', 
                        f'--cluster={cluster.get_id()}']
        
        ret_stdout = ras._execute_cli(param_list)
        # print(ret_stdout)

        ret_value = []
        list_sessions  = ret_stdout.split('\n\n')
        for yaml_base in list_sessions:
            if yaml_base == '':
                continue
            data = yaml.safe_load(yaml_base)
            ret_value.append(data)
        return ret_value

    def terminate_session(self, session_number):
        """Terminate infobase session with uid.
        Args:
            session_number (str, int): session uid
        """
        cluster = self._cluster
        ras = cluster.ras_connection
        param_list  = [ras.rac_path,
                    'session',
                    'terminate',
                        f'--session={session_number}', 
                        # f'--infobase-user={self.username}', 
                        # f'--infobase-pwd={self.passwood}', 
                        f'--cluster={cluster.get_id()}']
        
        try:
            ret_stdout = ras._execute_cli(param_list)
        except Exception as e:
            print(f'    failed to end session: {e}')
        print(f'    session {session_number} is terminate.')

    def terminate_all_sessions(self):
        sessions = self.get_sessions_list()
        for session in sessions:
            self.terminate_session(session['session'])
