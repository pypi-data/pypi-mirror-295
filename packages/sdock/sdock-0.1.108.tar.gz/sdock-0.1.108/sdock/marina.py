import os,sys,mystring as mys,docker,subprocess
from sdock.util import open_port, checkPort
from hugg import dock as container_storage

def flatten_list(obj: object) -> list:
    running = []
    for item in obj:
        if isinstance(item, list):
            running.extend(flatten_list(item))
        else:
            running += [item]
    return running

class titan(object):
    def __init__(self, image:str, working_dir:str, ports=[], network=None,detach=False,sudo=True,remove_container=True,name=None,mount_from_to={}, to_be_local_files=[], python_package_imports=[], environment_variables={}, raw_cmds=[], auto_pull=True,download_working_dir_file=False):
        self.container = mooring(image, working_dir, ports, network,detach,sudo,remove_container,name,mount_from_to,auto_pull, download_working_dir_file)

        #Prep Stuff
        self.python_package_imports = ["pip"] + python_package_imports
        self.to_be_local_files = to_be_local_files
        self.environment_variables = environment_variables
        self.raw_cmds = raw_cmds

    def __enter__(self):
        wake = self.container.__enter__()

        for raw_cmd in flatten_list(self.raw_cmds):
            wake(raw_cmd)

        for to_be_local_file in flatten_list(self.to_be_local_files):
            localized_to_be_local_file = os.path.join(self.container.working_dir, to_be_local_file)
            wake("mkdir -p {0}".format(os.path.dirname(to_be_local_file)))
            wake.storage.upload(to_be_local_file, localized_to_be_local_file)

        wake("python3 -m pip install --upgrade {0}".format(" ".join(flatten_list(self.python_package_imports))))

        for env_var_key, env_var_value in self.environment_variables.items():
            wake("""echo export {0}={1}" >> ~/.bashrc""".format(env_var_key, env_var_value))

        return wake

    def __exit__(self,a=None,b=None,c=None):
        container_name = self.container.name

        try:self.container.__exit__()
        except:pass

        try:kill_container(container_name)
        except Exception as e:pass
    
    def execute(self, *commands):
        boat = self.__enter__()
        for cmd in commands:
            if cmd is not None and cmd.strip() != '':
                boat(cmd)
        self.__exit__()

def kill_container(name):
    sys = lambda x:subprocess.check_call(x.split(),stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:sys("docker rm -f -v {0}".format(name))
    except Exception as e:pass #print("1:Killing")
    
    try:sys("docker rm -v {0}".format(name))
    except Exception as e:pass #print("2:Killing")
    
    try:sys("docker rm -f {0}".format(name))
    except Exception as e:pass #print("3:Killing")
    
    try:sys("docker rm {0}".format(name))
    except Exception as e:pass #print("4:Killing")

class mooring(object):
    def __init__(self, image:str, working_dir:str, ports=[], network=None,detach=False,sudo=True,remove_container=True,name=None,mount_from_to={},auto_pull=True,download_working_dir_file=False):
        self.client = docker.from_env()

        self.image = image
        self.working_dir = working_dir
        self.ports = ports
        self.network = network
        self.detach = detach
        self.sudo = sudo
        self.remove_container = remove_container
        self.name = name
        self.mount_from_to = mount_from_to

        self._container = None
        self._on = False
        self._off = True
        self._remove = True

        self.storage = None

        self.auto_pull = auto_pull
        self.download_working_dir_file = download_working_dir_file

    @property
    def on(self):
        if not self.is_on():
            try:
                self.container
                self.container.start()
            except Exception as e:
                print("Starting")
                print(e)

            self._on = self.status != "NotCreated"
            self._off = self.status == "NotCreated"
            self._remove = self.status == "NotCreated"

        return self._on

    def is_on(self):
        return self._on

    @property
    def off(self):
        if not self.is_off():
            try:
                self.container.stop()
            except Exception as e:
                print("Stopping")
                print(e)

            self._on = False
            self._off = True

        return self._off

    def is_off(self):
        return self._off

    @property
    def remove(self):
        if not self.is_removed():
            self.off
            try:self.container.kill()
            except Exception as e:pass #print("1:Killing")
            
            try:self.container.remove()
            except Exception as e:pass #print("2:Killing")
            
            try:os.system("docker rm {0}".format(self._name))
            except Exception as e:pass #print("2:Killing")

            self._remove = True

        return self._remove

    def is_removed(self):
        return self._remove

    @property
    def status(self):
        return "NotCreated" if self._container is None else self._container.status

    @property
    def container(self):
        if self._container is None:
            if self.auto_pull:
                self.client.images.pull(self.image)

            temp_containers = {}
            for mount_from, mount_to_in_container in self.mount_from_to.items():
                temp_containers[mount_from]={
                    "bind":mount_to_in_container,
                    "mode":"rw"
                }

            self._container = self.client.containers.create(
                image = self.image,
                command = "sleep 100000", #Seems to be necessary to keep the container alive while working with it?
                ports = {"{0}/tcp".format(port):port if checkPort(port) else open_port() for port in self.ports}, #Need to fix this
                network=self.network,
                detach=self.detach,
                privileged=self.sudo,
                #user=user_id,
                working_dir=self.working_dir,
                name=self.name,
                volumes=temp_containers
            )

            self.name = self._container.name
        return self._container

    def __enter__(self):
        self.on
        self.storage = container_storage(
            container=self.container,
            working_dir=self.working_dir
        ).__enter__()
        return self

    def run(self, string):
        return self(string)

    def __call__(self, string):
        exit_code=None;output_logs = []
        try:
            logs = self.container.exec_run(
                cmd = string,
                privileged=self.sudo,
                workdir=self.working_dir,
                stderr=True, stdout=True
            )
            for log_itr,log in enumerate(logs):
                if log_itr == 0:
                    try:
                        exit_code = int(str(log))
                    except Exception as e:
                        print("Error decoding {1} @ line {0}".format(str(log_itr), str(log)))
                else:
                    try:
                        log_line = str(log.decode("utf-8")).strip()
                        for subline in log_line.split("\n"):
                            output_logs += [str(subline).strip()]
                    except Exception as k:
                        print("Error decoding {1} @ line {0}".format(str(log_itr), str(log)))

        except Exception as e:
            print(e)
        return exit_code, output_logs

    def __exit__(self,a=None,b=None,c=None):
        if self.download_working_dir_file:
            self.download_working_dir(self.name+"_env.tar")

        self.storage.__exit__(None, None, None)
        self.off
        if self.remove_container:
            self.remove

        return

    def files(self):
        if self.storage is not None:
            return self.storage.files()
        return []

    def upload(self,file_path=None,path_in_repo=None):
        if self.storage is not None:
            return self.storage.upload(file_path=file_path,path_in_repo=path_in_repo)
        return None

    def download(self, file_path=None, download_to=None):
        if self.storage is not None:
            return self.storage.download(file_path=file_path,download_to=download_to)
        return None

    def download_working_dir(self, download_to=None):
        download_dir_to = download_to;ext = ".tar"
        if download_dir_to is None or not download_dir_to.endswith(ext):
            import uuid
            download_dir_to = download_to.replace(".tar","")+"_"+str(uuid.uuid4())+ext

            while os.path.exists(download_dir_to):
                download_dir_to = download_to.replace(".tar","")+"_"+str(uuid.uuid4())+ext

        base_download = os.path.basename(download_dir_to)
        current_files = str(self("ls /home/")[-1])

        temp_folder=base_temp_folder = "/home/__downloading__";ktr = 0
        while self.working_dir == temp_folder or temp_folder in current_files:
            temp_folder = base_temp_folder + str(ktr)
            ktr += 1

        self("mkdir -p {0}".format(temp_folder))

        tar_exitcode, tar_logs = self("tar cvf {0}/{1} {2}".format(temp_folder, base_download,self.working_dir))

        with container_storage(
            container=self.container,
            working_dir=temp_folder
        ) as downloading_storage:
            downloading_storage.download(base_download, download_to)

        return download_to