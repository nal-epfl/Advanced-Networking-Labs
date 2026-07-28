chown -R frr:frr /var/run/frr/
setfacl -m u:frr:rx /home/advnet
setfacl -m u:frr:rx /home/advnet/Desktop
setfacl -m u:frr:rx /home/advnet/Desktop/lab6
chown -R frr:frr /home/advnet/Desktop/lab6/run
chmod 750 /home/advnet/Desktop/lab6/run

