from django.core import validators
from django.utils.translation import gettext_lazy as _
import pathlib
import subprocess
import os, sys


SANDBOX_PATH = pathlib.Path('sandbox')
USER_JAILS_PATH = pathlib.Path('sandbox/users')


class FileNameValidator(validators.RegexValidator):
    regex = r"^[\w.-]+\Z"
    message = _(
        "Enter a valid name for your program. This value may contain only "
        "letters, numbers, and ./-/_ characters."
    )
    flags = 0


def get_user_jail(username) -> pathlib.Path:
    user_jail = USER_JAILS_PATH / username

    # Make sure the directory exists
    if not user_jail.is_dir():
        raise FileNotFoundError

    return user_jail


# This will be called when user creates an account
# Upon signup, the jail folder will be the same as the username
def create_user_jail(username):
    user_jail = USER_JAILS_PATH / username

    # Make sure the user directory is created inside the sandbox directory
    # Can be ignored, just throws an internal error on signup
    # if user_jail.parent != USER_JAILS_PATH:
    #     raise Exception

    user_jail.mkdir()


# Called when the user changes profile name
def rename_user_jail(old_username, username):
    old_jail = get_user_jail(old_username)
    old_jail.rename(USER_JAILS_PATH / username)


def save_user_script(username, script_file_name, script_content):
    user_jail = get_user_jail(username)
    user_script_file = user_jail / script_file_name
    with open(user_script_file, 'wb') as f:
        f.write(script_content.encode())


def delete_user_script(username, script_file_name):
    user_jail = get_user_jail(username)
    user_script_file = user_jail / script_file_name
    user_script_file.unlink()


def get_user_script(user, script_file_name) -> bytes:
    user_jail = get_user_jail(user)
    user_script_file = user_jail / script_file_name

    if user_script_file.is_file():
        with open(user_script_file, 'rb') as f:
            return f.read()
        
    return b''


def compile_user_script(user, script) -> tuple[bytes, bytes]:
    user_jail = get_user_jail(user)
    source_code = user_jail /  ('%s.c' % script)  # add the .c extension
    executable = user_jail / ('%s.out' % script)  # add the .out extension

    compile_command = ["gcc", "%s" % source_code, "-o", "%s" % executable]

    p = subprocess.run(
        compile_command,
        stdin=None,
        timeout=5,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return p.stdout, p.stderr


# This script will be ran after creating the chroot
# TODO: Add support for user input from web console
def run_user_script(user, script) -> tuple[bytes, bytes]:
    user_folder = (pathlib.Path('users') / user).resolve()
    executable = user_folder / ('%s.out' % script)

    # the stdout and stderr will be saved to files
    fout = open(user_folder / 'stdout', 'wb')
    ferr = open(user_folder / 'stderr', 'wb')

    command = ["%s" % executable]

    p = subprocess.run(
        command,
        stdin=None,
        timeout=60,
        stdout=fout,
        stderr=ferr,
    )

    fout.close()
    ferr.close()


# Warning: Python must have CAP_SYS_CHROOT capability set in order to call
# the run_in_sandbox() function without root permissions
def run_in_sandbox(user, script) -> tuple[bytes, bytes]:
    # compile
    compile_out, compile_err = compile_user_script(user, script)
    if compile_err != b'' or compile_out != b'':
        # some error occured
        return compile_out, compile_err

    # create sandbox
    gid = 1001
    uid = 1001

    pid = os.fork()
    if pid:
        # this is the parent process (real pid)
        # continue the execution of the webserver
        pass
    else:
        # this is the child process (pid 0)
        full_sandbox_path = SANDBOX_PATH.resolve()
        os.chdir(full_sandbox_path)
        os.chroot(full_sandbox_path)

        # Set gid first, then uid to avoid getting errors
        # os.setgid(gid)
        # os.setuid(uid)

        # run the actual program
        run_user_script(user, script)

        sys.exit(0)

    return compile_out, compile_err
