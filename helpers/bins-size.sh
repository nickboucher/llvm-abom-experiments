for i in $(seq 1 10)
do
    sudo tar -tvf /datadrive/results/bins-$i.tar | awk '{print $6,$3}' | sudo tee /datadrive/results/sizes/bins-$i-sizes.txt > /dev/null
done