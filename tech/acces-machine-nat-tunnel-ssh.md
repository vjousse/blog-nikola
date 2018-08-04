<!-- 
.. title: Accès machine derriere NAT/Firewall avec tunnel SSH
.. slug: acces-machine-nat-tunnel-ssh.md 
.. date: 2017-05-13 20:39:20 UTC+02:00
.. tags: ssh, linux
.. category: 
.. link: 
.. description: 
.. type: text
-->

Ceci est plus un post it perso qu'autre chose.

J'ai une machine qui est bien cachée sur mon réseau d'entreprise / fac (appelons la, `machine_cachee`). Forcément, cette machine je ne peux pas y accéder facilement quand je suis à la maison car elle n'a pas d'ip publique, elle est derrière un firewall, ou une box internet, ou je ne sais quoi. Je peux encore moins accéder au serveur http qui tourne dessus depuis chez moi (je ne peux y accéder que quand je suis sur le réseau de la FAC/entreprise).

Donc, quand j'ai accès à cette machine, je lance un tunnel SSH vers un serveur dédié que je détiens sur le nainternet mondial avec un compte dessus sous le nom de `mon_compte`, appelons-le `serveur_dedie`.

De `machine_cachee`:

    ssh -R 0.0.0.0:8888:127.0.0.1:80 mon_compte@serveur_dedie.com

Ça va ouvrir, sur `serveur_dedie.com` le port `8888` qui va me rediriger vers le port `80` de ma `machine_cachee`.

Il faut avoir rajouté dans `/etc/ssh/sshd_config` du serveur distant

    AllowTcpForwarding yes
    GatewayPorts yes

Puis:

    sudo service ssh reload
