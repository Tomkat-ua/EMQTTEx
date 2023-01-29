
container=TMQTTEx
img=tomkat/tmqttex

docker build -t $img .


docker container stop $container
docker container rm $container

#ports - host:container
docker run -d  -p 8084:80 \
    --net net_18  --ip 172.18.0.3 \
    --restart always \
    --name $container \
    -e TZ=Europe/Kiev \
    -e TEST_ENV_VAR='topic1/test/test2' \
    -e SERVER_PORT=80 \
    -e GET_DELAY=10 \
    -e BROKER_IP='172.18.0.2' \
    -e BROKER_PORT=1883 \
    -e TOPIC='tele/7C9EBDFA21A0/SENSOR' \
    -e USERNAME='mqtt' \
    -e PASSWORD='mqtt001' \
       $img