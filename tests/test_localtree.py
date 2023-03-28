'''test sftpretty.localtree'''

from common import conn, rmdir, VFS
from pathlib import Path
from sftpretty import Connection, localtree
from tempfile import mkdtemp


def test_localtree(sftpserver):
    '''test the localtree function, with recurse'''
    with sftpserver.serve_content(VFS):
        with Connection(**conn(sftpserver)) as sftp:
            localpath = Path(mkdtemp()).as_posix()
            sftp.get_r('.', localpath)

            cwd = sftp.pwd
            directories = localtree(localpath, localpath, cwd)
            dvalues = [
                (f'{localpath}/pub', f'{cwd}/pub'),
                (f'{localpath}/pub/foo1', f'{cwd}/pub/foo1'),
                (f'{localpath}/pub/foo2', f'{cwd}/pub/foo2'),
                (f'{localpath}/pub/foo2/bar1', f'{cwd}/pub/foo2/bar1')
            ]

            assert len(directories) == len(dvalues)
            assert sorted(directories) == sorted(dvalues)

    # cleanup local
    rmdir(localpath)


def test_localtree_no_recurse(sftpserver):
    '''test the localtree function, without recursing'''
    with sftpserver.serve_content(VFS):
        with Connection(**conn(sftpserver)) as sftp:
            localpath = Path(mkdtemp()).as_posix()
            sftp.chdir('pub/foo2')
            sftp.get_r('.', localpath)

            cwd = sftp.pwd
            directories = localtree(localpath, localpath, cwd, recurse=False)
            dvalues = [
                (f'{localpath}/bar1', f'{cwd}/bar1')
            ]

            assert directories == dvalues

    # cleanup local
    rmdir(localpath)
