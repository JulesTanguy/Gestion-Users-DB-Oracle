# Testé avec Python 3.6.8 (dernière version sur le repo CentOS au 08/01/2021)
# Ce programme nécessite une connexion au réseau jolsio.net pour y être executé sans modification

# Import des modules
import ldap
import sys
import cx_Oracle

# Ouverture du fichier pattern
if len(sys.argv) > 1:
    NomFichier = sys.argv[1]
else:
    NomFichier = input("Indiquez l'emplacement du fichier pattern : ")
NomPattern = NomFichier.replace("\\","/")
pattern=open(NomPattern,'r', encoding='utf-8')

# Connection à la base de donnée à l'AD
connect = ldap.initialize('ldap://172.15.11.210')
connect.set_option(ldap.OPT_REFERRALS, 0)
connect.simple_bind_s('btssio', 'P@ssw0rd21')

# Connection à la base de donnée Oracle
connection = cx_Oracle.connect('JTANGUY', 'JTANGUY', cx_Oracle.makedsn('172.15.11.102', 1521, 'orcl'))
curseur = connection.cursor()

# Récuperation et lecture des données de l'AD
Noms = []
result = connect.search_s('OU=Utilisateurs,OU=Toulouse,OU=Finances,DC=stesio,DC=jol', ldap.SCOPE_SUBTREE, "displayName=*")
for ligne in result:
	x=str(ligne).split(',')
	Noms.append(x[0].replace("('CN=",""))

# Lecture du fichier pattern
pattern=pattern.readlines()

# Tant qu'il y a des lignes dans le fichier CSV
for ligne in Noms:
    
    PrenomEtNom = ligne.split()
    prenom=PrenomEtNom[len(PrenomEtNom)-1]
    
    #print(prenom)
    # Si il y a plus de 2 mots dans le prenom et nom
    if len(PrenomEtNom) > 2:
        i=1
        nom=PrenomEtNom[0]
        
        # Tant qu'il y a des mots 'en trop' dans la variable PrenomEtNom,
        # prend ces mots en trop et l'inclut dans la variable nom
        while i < len(PrenomEtNom)-1:
            nom=nom+PrenomEtNom[i]
            i=i+1

        p = prenom[0]
    else:
        nom = PrenomEtNom[0]
        p = prenom[0]

    # Si il y a un tiret dans le prenom
    if '-' in prenom:
            pTemp = prenom
            p = (pTemp[0])[0]+(pTemp[1])[0]
    
    pnom = (p.upper()+nom.upper()).replace("'", "").replace("-", "")
    NomUserOracle = "GR2_"+pnom
    
    # Tant qu'il y a encore des lignes dans le fichier pattern
    i=0
    while i < len(pattern):
        cmdSql = pattern[i].replace("XXXXX", NomUserOracle)
        # Séparation des commandes SQL du fichier pattern 
        tCmdSql=cmdSql.split(';')
        i1 = 0
        while i1 < len(tCmdSql):
            if tCmdSql[i1] == " ":
                break
            print(tCmdSql[i1], end=" ; ")
            curseur.execute(str(tCmdSql[i1]))
            
            i1=i1+1
        print('↑ Commande exécutée avec succès')
        i=i+1

print('Toutes les commandes SQL ont été exécutées avec succès')