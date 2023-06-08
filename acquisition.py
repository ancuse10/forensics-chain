import time
from datetime import datetime
import re
import paramiko
import interactive
import subprocess

def adquisicion():
	k = paramiko.RSAKey.from_private_key_file("PATH_TO_RSA_KEY")
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	hostname = "IP_ADDRESS"
	acquisition_date = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

	# Define el nombre del archivo de log
	log_file = f"LOG_FILE_NAME"

	try:
	    print("\nConnecting to: " + hostname)
	    ssh.connect(hostname=hostname, username="USERNAME", pkey=k)
	    print("\nConnected to: " + hostname)

	    print("\nThe following filesystems are available: \n")
	    stdin,stdout,stderr = ssh.exec_command("df")
	    for line in stdout.readlines():
	        print(line)
	    stdin.flush()
	    stdout.flush()
	    stderr.flush()

	    file_to_acquire = input("\nEnter the filesystem you would like to acquire (e.g. /dev/mmcblk0p1): ")

	    # Comprobar si el archivo existe
	    stdin, stdout, stderr = ssh.exec_command(f"test -e {file_to_acquire}")
	    retorno = stdout.channel.recv_exit_status()


    	    # Pedir al usuario que ingrese un nombre de archivo válido
	    while retorno == 1:
	        print(f"\n{file_to_acquire} does not exist")
	        file_to_acquire = input("\nEnter a valid filesystem to acquire (e.g. /dev/mmcblk0p1): ")
	        stdin, stdout, stderr = ssh.exec_command(f"test -e {file_to_acquire}")
	        retorno = stdout.channel.recv_exit_status()

	    print("\nAcquiring Filesystem\n")

	    with open(log_file, 'a') as f:
	        f.write(f"Information for {file_to_acquire}:\n")

	        # Obtener información del disco
	        stdin, stdout, stderr = ssh.exec_command(f"lsblk -b {file_to_acquire} -o SIZE,MODEL,SERIAL")
	        output = stdout.readlines()
	        if len(output) > 0:
	            disk_info = output[1].strip().split()
	            disk_size = disk_info[0]
	            """disk_model = disk_info[1] #.decode('utf-8')
	            disk_serial = disk_info[2] #.decode('utf-8')"""
	            f.write("[Physical Evidentiary Item (Source) Information]:\n")
	            f.write(f"[Drive Geometry]\n Storage Size: {int(disk_size)/512}\n")

	            # Realizar adquisición
	            f.write(f"\n[Image Information]:\n Acquisition started: {acquisition_date}\n")
	            filename = f"{acquisition_date}.dd"
	            stdin, stdout, stderr = ssh.exec_command(f"sudo dd if={file_to_acquire} bs=1M count=100 of={filename}")
	            for line in stderr.readlines():
	                f.write(line)
	            f.write("\n Acquisition finished: {}\n".format(datetime.now()))

	            sftp = ssh.open_sftp()
	            sftp.get(f"{filename}", f"{filename}")
	            sftp.close()
	            print("\nFile downloaded successfully\n")

	            stdin, stdout, stderr = ssh.exec_command(f"rm -f {filename}")
	            for line in stderr.readlines():
	                print(line)

	            # Calcular hashes
	            f.write("[Computed Hashes]:\n")
	            output = subprocess.run(["md5sum", filename], capture_output = True)
	            md5sum = output.stdout.decode().split()[0]
	            f.write(f" MD5 checksum: {md5sum}\n")
	            output = subprocess.run(["sha1sum", filename], capture_output = True)
	            sha1sum = output.stdout.decode().split()[0]
        	    f.write(f" SHA1 checksum: {sha1sum}\n")

	            # Agregar información de archivo generado
	            f.write(f"\n Segment list:\n  {datetime.now().strftime('%F-%T')}.dd\n\n")

	    print("\nFilesystem acquired")
	    stdin.flush()
	    stdout.flush()
	    stderr.flush()

	    return log_file

	except KeyboardInterrupt:
	    print("\nProgram interrupted by user.")
	finally:
	    print("Closing SSH connection.")
	    ssh.close()

