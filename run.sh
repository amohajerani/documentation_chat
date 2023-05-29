sudo git pull
#sudo docker system prune -a
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
#sudo docker rmi -f $(sudo docker images -aq)

sudo docker build --memory 4g -t app ./app


sudo docker run --name app -d -p 8000:8000  app

sudo docker ps