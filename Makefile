build:
	sudo docker build -t surveil_centos_packaging .

mount:
	sudo docker run -i -t surveil_centos_packaging bash
