*******************************************************************************
*******************************************************************************
README - Nao Multimédia
Projet 10 : Louise et Nao
2016 Printemps

Auteurs :
ALVAREZ Paulina (paulina.alvarez@telecom-bretagne.eu)
BEN ABBES Bilel (bilel.benabbes@telecom-bretagne.eu)
GOGE Amadou     (amadou.oumarougoge@telecom-bretagne.eu)
PACREAU Boris   (boris.pacreau@telecom-bretagne.eu)
ZHAO Lu         (lu.zhao@telecom-bretagne.eu)
Étudiants ingénieurs à Télécom Bretagne, France
*******************************************************************************
*******************************************************************************
---------------------
I. Liste des fichiers
---------------------
README  -  Ce fichier
data/   -  Management de la base de données (Serveur et Client)
    NaoDatabaseServer.py    -   Lance le serveur pour la base de données
    NaoDatabaseClient.py    -   Gère la connexion à la base de données (CRUD)
    mongod.exe              -   MongoDB daemon
    db/	-	Path pour la base de données
    musicfile/  -   Path pour enregistrer des musiques
    storyfile/  -   Path pour enregistrer des histoires
src/
    filetransfer.py -   Gère une connexion FTP
    NaoBasic.py     -   Classe principal
    NaoGUI.py       -   Obtenir l'information de connection avec Nao
    PATH.py         -   Définitions des paths utilisés
    utils.py        -   Fonctions SpeechRecognition et isConnected
    dialog/         -   WIP
        MenuMultimedia.top
    modules/
        NaoInformationModule.py
        NaoMultimediaModule.py
        NaoMusicModule.py
        NaoNewsModule.py
        NaoRecognitionModule.py
        NaoStoryModule.py
        NaoTvModule.py
    search/
        entry.py
        informationProxy.py
        musicProxy.py
        newsProxy.py
        storyProxy.py
        tvProxy.py
        information/
            wikipediad.py
        music/
            youtubed.py
        news/
            newsd.py
        story/
            storyd.py
        tv/
            tvd.py

---------------
II. Dépendances
---------------
0. Essentielles
    - NAO H25 
    - Accès à Internet

1. Modules et API
    - python 2.7
    - NaoQi 2.1
    - pymongo 3.2.2
    - speech_recognition 3.4.6
    - youtube-dl v2016.06.19.1
    - wikipedia 1.4.0
    - urllib3 1.14
    - feedparser 5.2.1

2. Sites web 
    - Information
        www.wikipedia.fr
    - Journaux
        www.cotebrest.fr
        www.la-croix.com
        www.lequipe.fr/
        www.lemonde.fr
        www.letelegramme.fr
        www.ouest-france.fr
    - Musique
        www.youtube.com
    - Programmes télévision
        www.webnext.fr/epg_cache

3. Ports
    - 20 TCP
    - 80 HTTP
    - 27017 MongoDB

------------------------
III. Lancer le programme
------------------------
- Vérifier tous les dépendances.
- Lancer le script "NaoBasic.py".
- Entrer l'IP et le port pour la connexion TCP avec Nao; et le login et le
mot de passe pour la connexion FTP avec Nao.
- Arrêter avec ctrl+c.

-----------------------
IV. Explication du code
-----------------------
La classe NaoBasic est la classe principale du programme, ici on lance le
serveur et le client de la base de données, la connexion FTP avec NAO,
mais aussi la déclaration des modules NAO ainsi que la connexion avec les 
modules intégrés dans NAO.
Les classes NaoModules gère les interactions entre NAO et l'utilisateur
ainsi que les fonctionnalités de NaoMultimédia. Elles font la connexion
entre NaoBasic et une classe Proxy. 
Les classes Proxy ont un rôle de standardisation des données entrantes et
sortantes vers NaoModules, qui dépendent du type de contenu. 

----------------------
V. Ajouter des sources
----------------------
Pour ajouter des sources de recherche de contenu, vous devez créer une classe
dans src/search/[type] et modifier la classe proxy associée pour avoir la
standardisation de données entrantes et sortantes. 

---------------
VI. Maintenance
---------------
C'est primordial de réaliser la maintenance de la base de données par rapport
aux liens des sites web. Il est possible d'effectuer une modification
manuelle de la base de données à l'aide des classes NaoDatabaseServer et
NaoDatabaseClient.

--------------
VII. Glossaire
--------------
CRUD - Create, read, update and delete
FTP  - File Transfer Protocol
GUI  - Graphical User Interface
HTTP - HyperText Transfer Protocol
IP   - Internet Protocol
TCP  - Transmission Control Protocol
WIP  - Work In Progress