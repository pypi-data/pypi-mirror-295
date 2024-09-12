import os.path
import pathlib

from funnylog2 import logger
from nocmd import Cmd

from youqu3 import setting


def cli_cmd_creator(cmd_name, cmd_txt):
    cmd_path = os.path.expanduser(f"~/.local/bin/{cmd_name}")
    if not os.path.exists(cmd_path):
        Cmd.run(f"echo '{cmd_txt}' >> {cmd_path}")
        Cmd.run(f"chmod +x {cmd_path}")


def envx(python_version=None):
    if python_version is None:
        python_version = "3"
    rootdir = pathlib.Path(".").absolute()
    logger.info(rootdir)
    # pip
    stdout, return_code = Cmd.run("pip3 --version", return_code=True)
    if return_code != 0:
        Cmd.sudo_run('apt update', timeout=600)
        Cmd.sudo_run('apt install python3-pip -y')
        Cmd.run(f'pip3 install -U pip -i {setting.PYPI_MIRROR} --break-system-packages')
    # youqu3
    Cmd.run(f'pip3 install youqu3 -i {setting.PYPI_MIRROR} --break-system-packages')
    cli_cmd_creator("youqu3-cargo", 'pipenv run youqu3 "$@"')
    cli_cmd_creator("youqu3-shell", 'pipenv shell')
    cli_cmd_creator("youqu3-rm", 'pipenv --rm')
    cli_cmd_creator("youqu3-venv", 'pipenv --venv')
    # PATH
    with open(os.path.expanduser("~/.bashrc"), 'r') as f:
        bashrc = f.read()
    path_cmd = "export PATH=$PATH:$HOME/.local/bin"
    if path_cmd not in bashrc:
        Cmd.run(f"echo '{path_cmd}' >> ~/.bashrc")
        Cmd.run("source ~/.bashrc")
    # pipenv
    Cmd.run(f'pip3 install pipenv -i {setting.PYPI_MIRROR} --break-system-packages')
    Cmd.run(f"pipenv --python {python_version}", workdir=rootdir)
    Cmd.run(
        f"pipenv run pip install -r requirements.txt -i {setting.PYPI_MIRROR} --break-system-packages",
        workdir=rootdir,
        timeout=1800,
    )


if __name__ == '__main__':
    envx()
