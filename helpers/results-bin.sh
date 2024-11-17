for i in $(seq 1 10)
do
    sudo docker run --name exp-$i experiment-$i bash -c "tar -cf bins.tar **/bin"
    sudo docker cp exp-$i:/usr/src/app/bins.tar /datadrive/results/bins-$i.tar
    sudo docker rm exp-$i
done