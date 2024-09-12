import os,sys

class vrunn(object):
    def __init__(self, host:str=None,runner=None,do_destroy:bool=True):
        self.host = host
        self.do_destroy = do_destroy
        if not runner:
            def run(string):
                print(string)
                try:os.system(string)
                except Exception as e:
                    print(e)
                return None
            runner = run
        self.runner = runner

    def cmd(self, string, prefix="", suffix=""):
        command = " ".join([
            prefix,
            string,
            host,
            suffix
        ])
        command = str(command).strip()
        if not isinstance(self.host, list):
            self.host = [self.host]

        output = {}
        for host in self.host:
            output[host] = self.runner(command)
        return output

    def up(self, prefix="", suffix=""):
        return self.cmd(string="up", prefix=prefix, suffix=suffix)

    def down(self):
        return self.cmd(string="down", prefix=prefix, suffix=suffix)

    def suspend(self):
        return self.cmd(string="suspend", prefix=prefix, suffix=suffix)

    def resume(self):
        return self.cmd(string="resume", prefix=prefix, suffix=suffix)

    def destroy(self, force:bool=True, prefix="", suffix=""):
        if self.do_destroy:
            command = "destroy"
            if force:
                command = command + " -f"
            return self.cmd(command, prefix=prefix, suffix=suffix)
        return None

    def __enter__(self):
        self.up()
        return self

    def __exit__(self, a=None,b=None,c=None):
        self.destroy()
        return

    def run(self, string:str=None, dyr:str="/vagrant", prefix="", suffix=""):
        if dyr:
            string = "cd {0}/;{1}".format(string, dyr)
        return self.cmd(string=string, prefix=prefix, suffix=suffix)

    def trun(self, string:str=None, dyr:str="/vagrant", prefix="", suffix=""):
        return self.cmd(
            string='tmux new-session -d  "{0}"'.format(string),
            dyr=dyr,
            prefix=prefix,
            suffix=suffix
        )