#!/bin/bash
#Z1
mkdir -p $1
#Z2
mkdir $1/D1 $1/D2 $1/D3 $1/D4
touch $1/D2/F1.txt $1/D3/F1.txt $1/D4/F1.txt
#Z3
ln -s /etc/passwd $1/D1/passwd_link
#Z4
readlink -f $1/D1/passwd_link  
#Z5
ln $1/D3/F1.txt $1/D2/F2.txt
#Z6
chmod 600 $1/D2/F2.txt
#Z7
chown :users $1/D2/F2.txt
#Z8
chgrp users $1/D3/
#Z9
chmod a-x $1/D3/
#Z10
chmod a-w $1/D2/
#Z11
chmod a-r $1/D4/
#Z12
chmod +t $1/D4/
#Z13
touch $1/D1/scr1.sh
chmod ug+x $1/D1/scr1.sh
#Z14
chmod ug+s $1/D1/scr1.sh
