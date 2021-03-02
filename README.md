## Consignes

Il s’agit ici d’utiliser l’annuaire d’un serveur Windows (AD) pour créer automatiquement les comptes utilisateurs du système de gestion de bases de données (SGBD) Oracle de l’entreprise STESIO. Il est possible de récupérer la liste des utilisateurs via le protocole LDAP (library python-ldap) et d'exécuter les commandes de création d'utilisateurs sur le serveur de base de données Oracle (library Cx_Oracle). Les commandes à exécuter seront enregistrées dans un fichier pattern.txt où le nom des utilisateurs sera remplacé par XXXXX.

## Installation des libraries Python sous CentOS

### Installer cx_Oracle

```
pip3 install cx_Oracle

wget https://download.oracle.com/otn_software/linux/instantclient/211000/oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm

sudo rpm -i oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm
```

### Installer python-ldap

```
yum groupinstall "Development tools"

yum install openldap-devel python3-devel clang-analyzer valgrind

pip3 install python-ldap
```

## Utilisation du script sous Linux

python3 gererUsersOracle.py [Fichier Pattern]

exemple : `python3 gererUsersOracle.py pattern.txt`

Par défaut le script trouve dans l'AD le nom complet des utilisateurs et les transforme en nom abrégé par exemple :

Jean-Baptiste LE FLOC’H --> JBLEFLOCH

Comme dans indiqué dans l'exemple ci-dessus le script supporte les noms composés, avec des espaces, des apostrophes.

## Modifiation du script

### Modifier les identifiants de connexion Oracle dans le script

* Se rendre ligne n°22
* Remplacer tous les paramètres entre cotes (' ') par les votres :

```
connection = cx_Oracle.connect('Identifiant', 'Mot de passe', cx_Oracle.makedsn('adresse du serveur', 'port', 'SID'))
```

### Modifier les identifiants de connexion LDAP dans le script

* Se rendre ligne n°17
* Remplacer tous les paramètres entre cotes (' ') par les votres :

```
connect = ldap.initialize('ldap://adresse du serveur')
connect.set_option(ldap.OPT_REFERRALS, 0)
connect.simple_bind_s('Identifiant', 'Mot de passe')
```

### Modifier l'emplacement des utilisateurs dans l'AD

* Se rendre ligne n°28
* Remplacer tous les paramètres entre cotes (' ') par les votres :

```
result = connect.search_s('OU=Utilisateurs,OU=Toulouse,OU=Finances,DC=stesio,DC=jol', ldap.SCOPE_SUBTREE, "displayName=*")
```
