import paramiko

host = "167.235.11.154"
port = 22
username = "terapkco"
password = "(3#JCk2Vyn94hY"

try:
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)
    
    stdin, stdout, stderr = ssh.exec_command("source /home/terapkco/virtualenv/xcomic_backend/3.11/bin/activate && cd xcomic_backend && python test_db2.py")
    out = stdout.read().decode()
    err = stderr.read().decode()
    print("STDOUT:", out)
    print("STDERR:", err)
    
    ssh.close()
except Exception as e:
    print(f"Error: {e}")
