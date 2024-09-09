# cbl_tools: miscelaneous daily tasks helpers

A package with miscelaneous classes meant to help at coding console helpers. Currently there are three classes:

1. **config**: it implements a config file that saves itself. It is a specialization of [configparser](https://docs.python.org/3/library/configparser.html).
2. **process**: it runs external processes, it saves the return code, and it helps (a little bit) to parse the standard output (or the standard error).
3. **git**: a simple interface for git commands.

## config: a self-preserving config file

It implements a config file that saves itself.

The idea is: we want to use a config file for an application, which is a simple text file that contains pairs of values, in a similar fashion to an INI file. If the file exists, it is used; if it doesn't, it is created. We use [configparser](https://docs.python.org/3/library/configparser.html) for this.

An example:

```python
from cbl_tools.config import config

cfg = config(initpath = '~/somewhere/blabla.ini')
cfg.create_section('my_configuration')
cfg.set('my_configuration', 'x', 1)
cfg.set('my_configuration', 'y', '2')
```

When the program above ends, it will save all created configuration to the file ~/somewhere/blabla.ini.

## process: a helper to run external programs

It runs an external program, and it stores the return code and both the standard output and standard error.

You first create an object of this type:
```python
p = process()
```

Then run a command:
```python
p.run("whoami")
```

Immediately after you gain access to the return code, stdout and stderr:
```python
print(p.returncode)
for line in p.stdout:
  print(line)
```

You may check if return code was 0 (i.e., all good) by checking `p.is_ok()` to be true. You may also check whether there is any stdout or any stderr with `p.is_there_stdout()` and with `p.is_there_stderr()`, respectively.

Finally you may extract information out of stdout by using `extract()`. This method receives a regular expression and a boolean that is true by default (meaning that you want to inspect stdout; if false it will inspect stderr instead). The method will look for all matches in each line of stdout and store them in a list. The list stores as many elements as lines stdout has, and each element is a list of all matches within the corresponding line.

## git: a simple git interface

It provides a simple programmatical interface to git.

First, you create a git object by providing a local path to a repo:

```python
from cbl_tools.git import git

x = git("~/Dev/my_repo")
```
The previous will fail if provided path is not a git repo.

Then you may either get the remote urls with `x.get_remote()`, or a get the status of the working tree by invoking `x.get_status()`.

You may also do a commit with a list of files with `x.commit(list-of-files)`, or do a push (`x.git_push('my-commit-message')`) or a pull (`x.git_pull()`).

This package also includes two auxiliary functions:

* `git_clone(url:str, path:str)`: It clones `url` into `path`.
* `is_git_url(url:str)`: It checks whether `url` is a valid git url.
