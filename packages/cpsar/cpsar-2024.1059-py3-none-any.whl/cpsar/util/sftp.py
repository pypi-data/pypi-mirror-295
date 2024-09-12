import paramiko
import cpsar.runtime as R
from cpsar import config

def connect(label:str) -> object:
    cursor = R.db.cursor()
    cursor.execute("""
        select host, port, username, password
        from sftp_account
        where label=%s
        """, (label,))
    if not cursor.rowcount:
        raise config.ConfigError(f"Could not find SFTP account for label {label}")
    host, port, username, password = next(cursor)
    t = paramiko.Transport((host, port))
    t.connect(username=username, password=password)
    return paramiko.SFTPClient.from_transport(t)
