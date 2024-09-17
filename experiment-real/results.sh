cd /usr/src/app
for x in *.time
do
    echo "$x:" && cat $x && echo
done