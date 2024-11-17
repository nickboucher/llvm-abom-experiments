for attempts in 100000
do
    for deps in 1 10 100 1000 10000 100000
    do
        for i in {1..10}
        do
            docker run --rm llvm-abom-experiment-artificial $deps $attempts | tee $deps-$attempts-$i.txt
        done
    done
done