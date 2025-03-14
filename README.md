# flash_card_app
# Based on tutorial from: https://www.youtube.com/watch?v=Zem1H7Rr9yM

After doing git pull, you need to rerun docker
# docker build -t flash_card_app .
docker build --no-cache -t flash_card_app .

Then start the app
docker run -d -p 5000:5000 flash_card_app

The run the EC2 instance with port 5000

To check for others on the port:
netstat -tulnp | grep 5000

To stop and remove on docker
docker ps 
docker stop <container id>
docker rm <container id>

