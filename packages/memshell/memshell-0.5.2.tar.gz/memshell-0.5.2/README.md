# MemShell

Ever have trouble with Makefiles or Jenkinsfiles or other scripting tools that simply
invoke a new shell for every command or block of commands, forgetting what was sourced
or what your current path is? (I'm looking at you NPM...) Wouldn't it be nicer if these
tools just used a single shell instance so that you can just treat it like you are using
your terminal?

That is what this library aims to fix. Using a bit of trickery it is able to create a
long-running shell that your Python script can interact with, and it will remember the
environment variables, including the PATH and PWD, for as long as the shell object is in
scope!

## Usage

### Basics

```python
from memshell import Shell

shell = Shell()
result = shell.exec(
    "pwd",
    "cd ~",
    "ls",
    "cd code",
    "ls"
)
print(result.std_out)
print(result.std_err)
print(result.return_code)
shell.close()
```

`Shell.exec` takes variatic arguments as strings of commands to run and returns one
combined output

To set `-e` mode pass it in to the `exec` method with the `modes` argument.

```python
result = shell.exec("spam", "ls", modes=["-e"])  # this will fail at the first command 
# (unless you have an executable called 'spam' in your PATH, that is)
print(result.std_out)  # ''
print(result.return_code)  # 127
print(result.std_err)  # 'zsh: command not found: spam'
```

To get the output from each command individually, use the `exec_all` method which takes
a list of strings as commands.

```python
results = shell.exec_all(["pwd", "cd ~", "ls"])
print(len(results))  # 3
print(results[0].std_out)  # '/home/yourname/code/project'
print(results[1].return_code)  # 0
```

`Shell` can be invoked with a context manager to automatically close out the shell

```python
with Shell() as shell:
    ...  # use shell
```
