"""It runs an external program, and it stores the return code and both the standard
output and standard error.

You first create an object of this type:
> p = process()

Then run a command:
> p.run("whoami")

Immediately after you gain access to the return code, stdout and stderr:
> print(p.returncode)
> for line in p.stdout:
>   print(line)

You may check if return code was 0 (i.e., all good) by checking p.is_ok() to be true.
You may also check whether there is any stdout or any stderr with p.is_there_stdout()
and with p.is_there_stderr(), respectively.

Finally you may extract information out of stdout by using extract(). This method receives
a regular expression and boolean that is true by default (meaning that you want to inspect
stdout; if false it will inspect stderr instead). The method will look for all matches in
each line of stdout and store them in a list. The list stores as many elements as lines
stdout has, and each element is a list of all matches within the corresponding line.
"""

import re
import subprocess

class process:
    command = None
    returncode = None
    stdout = None
    stderr = None

    def __str__(self) -> str:
        if not self.command:
            return "<Empty cbl_tools.process object>"
        else:
            out = f"({self.command})->{self.returncode}\n"
            if self.stdout:
                out += ''.join(map(lambda x: 'O: '+x+'\n', self.stdout))
            if self.stderr:
                out += ''.join(map(lambda x: 'E: '+x+'\n', self.stderr))
            return out

    def reset(self) -> None:
        self.command = None
        self.returncode = None
        self.stdout = None
        self.stderr = None

    def run(self, comm:str, fail_if_not_ok:bool = False) -> None:
        cp = subprocess.run(comm.split(" "), capture_output=True, text=True)
        self.command = comm
        self.returncode = cp.returncode
        if cp.stdout != '':
            self.stdout = cp.stdout.rstrip(" \n").split("\n")
        if cp.stderr != '':
            self.stderr = cp.stderr.rstrip(" \n").split("\n")
        if fail_if_not_ok and not self.is_ok():
            print(self)
            exit(1)

    def is_ok(self) -> bool:
        return self.returncode == 0

    def is_there_stdout(self) -> bool:
        if self.stdout == None:
            return None
        else:
            return len(self.stdout)>0

    def is_there_stderr(self) -> bool:
        if self.stderr == None:
            return None
        else:
            return len(self.stderr)>0

    def extract(self, pat:str, stdout:bool = True, join:str = True) -> list:
        wheretolook = self.stdout if stdout else self.stderr
        if not wheretolook:
            return None

        pattern = re.compile(pat)

        if join:
            return pattern.findall("".join(wheretolook))

        else:
            lst = []
            for line in wheretolook:
                lst.append(pattern.findall(line))
            return lst
