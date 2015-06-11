build:
	sudo docker build -t centos_packaging .

mount:
	sudo docker run -i -t --name centos_packaging centos_packaging

remove:
	sudo docker rm -f centos_packaging
