import paramiko

host = "167.235.11.154"
user = "terapkco"
password = "(3#JCk2Vyn94hY"
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    print("Connecting...")
    client.connect(host, port, user, password, timeout=10)
    print("Connected.")
    
    # 1. Check path and pull
    commands = [
        "cd repositories/personal_email_marketer/xcomic_backend && git pull origin master",
        "cd repositories/personal_email_marketer/xcomic_backend && mkdir -p tmp && touch tmp/restart.txt",
        "echo 'Done'"
    ]
    
    for cmd in commands:
        print(f"Executing: {cmd}")
        stdin, stdout, stderr = client.exec_command(cmd)
        print("STDOUT:", stdout.read().decode())
        print("STDERR:", stderr.read().decode())

finally:
    client.close()
    print("Closed.")
