# TP 1 - Cryptographie appliquee : TLS/SSL PKI

Les manipulations ont ete realisees sur deux machines virtuelles Alma Linux :

- `tls-ca-timeoC` (192.168.170.54) : autorite de certification intermediaire, qui delivre les certificats.
- `tls-serv-timeoC` (192.168.170.73) : serveur web et reverse proxy HTTPS (Docker, Nginx, deux conteneurs Apache).

La CA racine `Root Lorne` est hebergee sur une troisieme machine geree par l'enseignant (`camanager@192.168.170.231`).

Les fichiers produits pendant le TP (demandes de certificat, certificats, configuration Nginx, client de test) sont dans le dossier `fichiers/` du depot. Les cles privees ne sont volontairement pas versionnees : ce sont les seuls elements qui ne doivent jamais sortir des machines.

---

## Question 1 - Chiffrement et dechiffrement RSA

RSA est un algorithme de cryptographie asymetrique. Il utilise deux cles differentes : une cle publique et une cle privee.

La cle publique contient deux elements :
- n : le module RSA, calcule avec deux nombres premiers p et q.
- e : l'exposant public.

La cle privee contient notamment l'exposant prive d.

### Chiffrement du message

Pour chiffrer un message M, l'expediteur utilise la cle publique du destinataire.

La formule de chiffrement est :

```text
C = M^e mod n
```

Avec :
- M : le message en clair.
- e : l'exposant public.
- n : le module RSA.
- C : le message chiffre.

Le message chiffre C peut ensuite etre envoye au destinataire.

### Dechiffrement du message

Pour retrouver le message original, le destinataire utilise sa cle privee.

La formule de dechiffrement est :

```text
M = C^d mod n
```

Avec d comme exposant prive, le destinataire retrouve le message initial M.

En pratique, RSA utilise un mecanisme de securisation supplementaire comme OAEP pour eviter de chiffrer directement un message brut.

---

## Question 2 - Role de la methode Diffie-Hellman

Diffie-Hellman est une methode qui permet a deux personnes de generer une cle secrete commune sans avoir besoin de l'envoyer directement sur le reseau.

Cette cle peut ensuite etre utilisee pour chiffrer les communications avec un algorithme symetrique comme AES.

### Fonctionnement

On prend l'exemple de deux utilisateurs : Alice et Bob.

1. Alice et Bob choisissent deux parametres publics communs :
   - p : un grand nombre premier.
   - g : un generateur.

2. Alice choisit un nombre secret a et calcule sa valeur publique :

```text
A = g^a mod p
```

3. Bob choisit un nombre secret b et calcule sa valeur publique :

```text
B = g^b mod p
```

4. Ils echangent leurs valeurs publiques A et B.

5. Alice calcule le secret partage avec la valeur de Bob :

```text
K = B^a mod p
```

6. Bob fait le meme calcul avec la valeur d'Alice :

```text
K = A^b mod p
```

Les deux obtiennent le meme resultat :

```text
K = g^(a*b) mod p
```

Diffie-Hellman permet donc de creer une cle commune sans la transmettre directement. Cependant, cette methode seule ne permet pas de verifier l'identite des correspondants. Il faut utiliser un mecanisme d'authentification, comme les certificats numeriques, pour eviter une attaque de type homme du milieu.

---

## Question 3 - Donner 4 informations importantes contenues dans un certificat

Un certificat numerique permet d'associer une identite a une cle publique. Il est delivre et signe par une autorite de certification (CA).

Un certificat contient plusieurs informations. Voici les quatre principales :

### 1. Le sujet (Subject)

Il indique a qui appartient le certificat. Il peut s'agir d'une personne, d'une entreprise ou d'un serveur.

On peut notamment retrouver :
- C : le pays (Country).
- ST : la region (State or Province).
- L : la ville (Locality).
- O : le nom de l'organisation (Organization).
- CN : le nom commun (Common Name).

### 2. La cle publique (Public Key)

Elle correspond a la cle publique associee au sujet. Elle peut etre utilisee dans les mecanismes cryptographiques et pour verifier des signatures numeriques.

### 3. L'emetteur (Issuer)

Il indique quelle autorite de certification a delivre et signe le certificat.

### 4. La periode de validite (Validity)

Elle indique pendant quelle periode le certificat est valable :
- Not Before : date de debut de validite.
- Not After : date de fin de validite.

---

## Question 4 - Etapes de l'authentification du site Alice en HTTPS

Bob souhaite se connecter au site suivant :

```text
https://www.alice.com
```

Pour verifier que le site est bien celui d'Alice, le navigateur utilise les certificats numeriques. Dans notre cas, le certificat de Alice est signe par ca1, et le certificat de ca1 est signe par root-ca.

### 1. Reception des certificats

Lorsque Bob se connecte au site, le serveur Alice lui envoie son certificat ainsi que celui de l'autorite intermediaire ca1.

La chaine de certification est la suivante :

```text
www.alice.com
      |
      | signe par
      v
     ca1
      |
      | signe par
      v
   root-ca
```

### 2. Verification du certificat de Alice

Le navigateur verifie que le certificat correspond bien au site www.alice.com. Il controle aussi sa periode de validite et verifie sa signature avec la cle publique de ca1.

### 3. Verification de ca1 et de root-ca

Le navigateur verifie ensuite la signature du certificat de ca1 avec la cle publique de root-ca.

Enfin, il verifie que root-ca est presente dans les autorites de certification reconnues comme fiables par le systeme ou le navigateur de Bob.

### 4. Fin de l'authentification

Si toutes les verifications sont correctes, la chaine de certification est validee.

Le serveur Alice doit egalement prouver qu'il possede la cle privee correspondant a son certificat. Une fois cette verification effectuee, la negociation TLS permet de generer des cles de session.

Ces cles sont ensuite utilisees pour chiffrer les donnees echangees entre Bob et le serveur Alice.

## Question 5 - Longueur de n et fonctionnement de RSA

Apres avoir genere la biclé RSA, on peut afficher son contenu avec la commande :

```text
openssl rsa -in rsa_keys.pem -text -noout
```

La valeur `n` correspond au module RSA. Elle est obtenue en multipliant deux nombres premiers :

```text
n = p * q
```

Dans le sujet, il est demande de generer une cle de 1024 bits. Dans ce cas, la longueur de `n` est normalement de 1024 bits.

Attention : la commande donnee dans le sujet utilise `rsa_keygen_bits:512`. Si cette commande est utilisee telle quelle, la longueur de `n` sera normalement de 512 bits. Il faut donc verifier la commande qui a reellement ete executee.

Pour chiffrer un message M avec RSA, on utilise la cle publique composee de `n` et de `e` :

```text
C = M^e mod n
```

Pour dechiffrer le message, on utilise la cle privee avec l'exposant `d` :

```text
M = C^d mod n
```

Dans l'affichage de la cle, on retrouve egalement le parametre `publicExponent`. Celui-ci est generalement egal a 65537.

Il n'est pas vraiment difficile a deviner pour un pirate, car cette valeur est publique et souvent utilisee par defaut. Ce n'est pas un probleme de securite : l'exposant public est justement fait pour etre connu. La securite de RSA repose principalement sur la difficulte de retrouver la cle privee a partir de la cle publique, et non sur le fait de cacher l'exposant public.

---

## Question 6 - Interet de chiffrer une cle publique ou une cle privee

Il n'y a pas d'interet particulier a chiffrer une cle publique. Elle est faite pour etre partagee avec d'autres personnes afin qu'elles puissent, par exemple, nous envoyer des messages chiffres ou verifier nos signatures.

En revanche, il est important de proteger une cle privee. Si une personne malveillante recupere cette cle, elle peut notamment dechiffrer des messages qui lui sont destines ou usurper l'identite de son proprietaire en realisant des signatures.

C'est pour cette raison que le TP propose de chiffrer la biclé avec AES-128 et une passphrase. Cela permet de proteger le fichier contenant la cle privee si quelqu'un arrive a y acceder.

---

## Question 7 - Encodage utilise pour la cle publique

Le fichier `pub.pem` utilise le format PEM (Privacy-Enhanced Mail).

Ce format contient des donnees binaires encodees en Base64, encadrees par des lignes qui indiquent le type de contenu.

Par exemple :

```text
-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----
```

L'encodage Base64 permet de representer des donnees binaires sous forme de caracteres ASCII.

Son avantage est de faciliter le stockage, la lecture et le transfert des cles dans des fichiers texte. Cela permet notamment de copier facilement une cle publique ou de la transmettre par mail ou via un serveur web.

Il faut cependant preciser que Base64 est un encodage et non un chiffrement. Il ne protege donc pas le contenu de la cle.

---

## Question 8 - Verification du contenu de la cle publique

Pour afficher le contenu de la cle publique sous une forme lisible, on utilise la commande OpenSSL :

```text
openssl rsa -pubin -in pub.pem -text -noout
```

On retrouve normalement les elements attendus de la cle publique RSA :

- Le module `Modulus`, qui correspond a n.
- L'exposant public `Exponent`, qui correspond a e.

Ces deux valeurs constituent la cle publique RSA.

Il est interessant de disposer d'un fichier separe contenant uniquement la cle publique, car cela permet de la partager facilement avec d'autres utilisateurs sans transmettre la cle privee.

Chaque personne peut ainsi recuperer notre cle publique pour nous envoyer des messages chiffres, sans avoir acces aux informations privees contenues dans la biclé complete.

---

## Question 9 - Quelle cle utiliser pour chiffrer un message RSA de maniere confidentielle ?

Lorsqu'on souhaite envoyer un message de maniere confidentielle a une personne, il faut utiliser la cle publique du destinataire pour chiffrer le message.

Le destinataire pourra ensuite utiliser sa cle privee pour retrouver le message original.

Par exemple, si Alice souhaite envoyer un message confidentiel a Bob, elle utilise la cle publique de Bob pour chiffrer le message. Bob utilise ensuite sa propre cle privee pour le dechiffrer.

```text
Alice :
Message en clair
       |
       | Chiffrement avec la cle publique de Bob
       v
Message chiffre
       |
       | Envoi a Bob
       v
Bob :
Dechiffrement avec sa cle privee
       |
       v
Message original
```

De cette maniere, seule la personne qui possede la cle privee correspondante peut normalement dechiffrer le message.


---

## Question 10 - Parametres de la commande openssl pkeyutl -encrypt

La commande utilisee pour chiffrer un message avec la cle publique du destinataire est la suivante :

```text
$ openssl pkeyutl -encrypt -pubin -inkey pub.timeoC.pem -in clair.txt -out cipher.bin
```

Detail des parametres :

- `pkeyutl` : sous-commande d'openssl permettant d'effectuer des operations bas niveau avec une cle asymetrique (chiffrement, dechiffrement, signature...).
- `-encrypt` : indique que l'on realise un chiffrement avec la cle publique.
- `-pubin` : indique que la cle fournie avec `-inkey` est une cle publique seule (et non une biclé). Sans cette option, openssl cherche une cle privee.
- `-inkey pub.timeoC.pem` : la cle publique du destinataire.
- `-in clair.txt` : le fichier contenant le message en clair.
- `-out cipher.bin` : le fichier dans lequel est ecrit le message chiffre.

Le fichier `clair.txt` contient :

```text
$ echo "Bonjour de Timeo" > clair.txt
```

L'affichage du contenu du message chiffre se fait avec :

```text
$ hexdump cipher.bin
0000000 fa01 5098 7b20 3ff2 699a 100c 2f75 d0d4
0000010 b7db 7a47 81c6 50f5 e921 5400 2fc5 59ac
0000020 e7bb d581 3203 4a25 8a18 e10c e8f9 f8d9
0000030 e0bc faec 83d4 f9fd eb63 102e 9a10 44f0
0000040 183d 6f0d e7f9 73c8 5fe4 2be7 d299 87c3
0000050 ac0e 2b80 b4f4 0e07 2eb0 94ce 0c11 1fdf
0000060 33ed a66a da69 4dee 567e 5bc4 7e67 42c7
0000070 8f56 9dcd 34d1 970d 2270 cd97 6dbf 9ecd
0000080
```

Le fichier produit fait 128 octets, ce qui correspond a la taille de la cle RSA utilisee (1024 bits = 128 octets). Un message chiffre avec une cle de 2048 bits ferait 256 octets.

Il faut noter que le chiffrement RSA avec `pkeyutl` utilise par defaut le remplissage PKCS#1 v1.5. La taille du message en clair est donc limitee : elle ne peut pas depasser la taille de la cle moins 11 octets (soit 117 octets pour une cle de 1024 bits).

Le dechiffrement se fait avec la cle privee du destinataire :

```text
$ openssl pkeyutl -decrypt -inkey rsa_keys_cyphered.pem -in cipher.bin -out dechiffre.txt
$ cat dechiffre.txt
Bonjour de Timeo
```

---

## Question 11 - Comparaison de plusieurs chiffrements du meme message

On chiffre trois fois le meme fichier `clair.txt` :

```text
$ openssl pkeyutl -encrypt -pubin -inkey pub.timeoC.pem -in clair.txt -out cipher.bin
$ openssl pkeyutl -encrypt -pubin -inkey pub.timeoC.pem -in clair.txt -out cipher.bin.1
$ openssl pkeyutl -encrypt -pubin -inkey pub.timeoC.pem -in clair.txt -out cipher.bin.2
$ md5sum cipher.bin cipher.bin.1 cipher.bin.2
a94bfffa8f009e407ab5836054427b59  cipher.bin
b9cee505582a27d44b056c70cebb3528  cipher.bin.1
862ae8afe44b519414562a2562ff2f83  cipher.bin.2
```

Les trois messages chiffres sont differents, alors que le message en clair et la cle utilisee sont identiques. C'est normal.

Le chiffrement RSA brut (`C = M^e mod n`) est deterministe : un meme message donnerait toujours le meme resultat. Mais en pratique on ne chiffre jamais directement le message : on utilise un remplissage (padding) comme PKCS#1 v1.5 ou OAEP. Ce remplissage ajoute des octets aleatoires avant le calcul RSA, ce qui rend chaque chiffrement different.

Ce comportement est souhaitable du point de vue de la securite. Si le chiffrement etait deterministe, un attaquant pourrait comparer les messages chiffres et en deduire des informations sur le contenu (par exemple savoir si deux messages sont identiques, ou tester un message probable).

---

## Question 12 - Role de l'option -showcerts de s_client

La commande utilisee est :

```text
$ openssl s_client -showcerts -connect www.univ-grenoble-alpes.fr:443
```

D'apres la page de manuel, l'option `-showcerts` affiche la chaine de certificats complete envoyee par le serveur, et non uniquement le certificat du serveur. Chaque certificat de la chaine est affiche au format PEM.

Au debut de la reponse, on retrouve la chaine de certification avec les niveaux de profondeur :

```text
depth=2 C=GR, O=Hellenic Academic and Research Institutions CA, CN=HARICA TLS RSA Root CA 2021
verify return:1
depth=1 C=GR, O=Hellenic Academic and Research Institutions CA, CN=GEANT TLS RSA 1
verify return:1
depth=0 C=FR, ST=Auvergne-Rhone-Alpes, L=Saint-Martin-d'Heres, O=Universite Grenoble Alpes, CN=*.univ-grenoble-alpes.fr
verify return:1
```

Ensuite, la section `Certificate chain` detaille chaque certificat :

- `0` : le certificat du serveur, `CN=*.univ-grenoble-alpes.fr`.
- `1` : le certificat de l'autorite intermediaire, `CN=GEANT TLS RSA 1`.
- `2` : le certificat de l'autorite racine, `CN=HARICA TLS RSA Root CA 2021`.

Le serveur a donc envoye 3 certificats. On remarque que le serveur envoie effectivement son certificat mais aussi le certificat des autorites de certification intermediaires.

---

## Question 13 - Le format x509 et le sujet du certificat

L'option `x509` de la commande openssl indique que l'on travaille sur un certificat au format X.509. X.509 est le standard qui definit la structure d'un certificat a cle publique. La commande utilisee est :

```text
$ openssl x509 -in cert0.pem -noout -text
```

Le sujet (subject) du certificat est :

```text
subject=C=FR, ST=Auvergne-Rhone-Alpes, L=Saint-Martin-d'Heres, O=Universite Grenoble Alpes, CN=*.univ-grenoble-alpes.fr
```

Cette notation est une suite de paires attribut/valeur :

- `C=FR` : Country, le pays du proprietaire du certificat.
- `ST=Auvergne-Rhone-Alpes` : State or Province, la region.
- `L=Saint-Martin-d'Heres` : Locality, la ville.
- `O=Universite Grenoble Alpes` : Organization, le nom de l'organisme proprietaire du certificat.
- `CN=*.univ-grenoble-alpes.fr` : Common Name, le nom commun.

Le CN correspond au nom de la machine pour laquelle le certificat a ete delivre. Ici, la valeur `*.univ-grenoble-alpes.fr` contient un joker (`*`) : le certificat est valable pour tous les noms de machines du domaine `univ-grenoble-alpes.fr` (par exemple `www`, `ent`, `moodle`...).

L'organisme qui a delivre le certificat est indique dans l'attribut `issuer` :

```text
issuer=C=GR, O=Hellenic Academic and Research Institutions CA, CN=GEANT TLS RSA 1
```

Le certificat a donc ete delivre par l'autorite intermediaire `GEANT TLS RSA 1`.

---

## Question 14 - Signification du "s" et du "i"

Dans la section `Certificate chain` de la reponse de s_client, on trouve pour chaque certificat deux lignes :

```text
0 s:C=FR, ST=Auvergne-Rhone-Alpes, L=Saint-Martin-d'Heres, O=Universite Grenoble Alpes, CN=*.univ-grenoble-alpes.fr
  i:C=GR, O=Hellenic Academic and Research Institutions CA, CN=GEANT TLS RSA 1
```

- `s` signifie **subject** : c'est le proprietaire du certificat, celui a qui le certificat a ete delivre.
- `i` signifie **issuer** : c'est l'autorite de certification qui a signe et delivre ce certificat.

Le numerotage `0`, `1`, `2` indique la position dans la chaine de certification.

---

## Question 15 - Analyse du certificat de www.univ-grenoble-alpes.fr

Le certificat du serveur ne contient que la partie publique de la cle RSA, c'est-a-dire le module `n` et l'exposant public `e`. La cle privee n'est jamais transmise dans un certificat. On le voit dans la sortie de la commande :

```text
Public Key Algorithm: rsaEncryption
    Public-Key: (2048 bit)
    Modulus:
        ...
    Exponent: 65537 (0x10001)
```

Les algorithmes utilises sont :

- `rsaEncryption` pour la cle publique contenue dans le certificat.
- `sha256WithRSAEncryption` pour la signature du certificat (SHA-256 pour le hachage, RSA pour la signature). C'est aussi l'algorithme de la signature de l'emetteur, puisque le certificat est signe par une CA qui utilise une cle RSA.

L'attribut CN du sujet contient `*.univ-grenoble-alpes.fr`. C'est un nom generique : le certificat est valable pour toute machine du domaine `univ-grenoble-alpes.fr`.

L'attribut qui contient les autres noms de machine pour lesquels le certificat peut etre utilise est l'extension `subjectAltName` (Subject Alternative Name) :

```text
X509v3 Subject Alternative Name:
    DNS:*.univ-grenoble-alpes.fr, DNS:univ-grenoble-alpes.fr
```

Ce sont ces valeurs que les navigateurs verifient reellement : le CN n'est plus pris en compte par les navigateurs modernes lorsque l'extension subjectAltName est presente.

La duree de validite est donnee par les champs `Not Before` et `Not After` :

```text
Not Before: Oct 20 09:03:04 2026 GMT
Not After : May  7 09:03:03 2027 GMT
```

Le certificat est donc valable du 20 octobre 2026 au 7 mai 2027, soit environ 6 mois et demi. Cette duree courte est imposee par la reglementation (CA/Browser Forum) pour limiter la duree d'exposition en cas de compromission d'une cle.

Le lien vers un fichier `.crl` est indique dans l'extension CRL Distribution Points :

```text
X509v3 CRL Distribution Points:
    Full Name:
        URI:http://crl.harica.gr/HARICA-GEANT-TLS-R1.crl
```

Une CRL (Certificate Revocation List) est la liste des certificats revoques par une autorite de certification. Elle permet au client de verifier que le certificat du serveur n'a pas ete revoque avant sa date de fin de validite (par exemple si la cle privee a ete volee).

---

## Question 16 - Signature du certificat du serveur

Le certificat de www.univ-grenoble-alpes.fr a ete signe par l'autorite de certification intermediaire dont le sujet est :

```text
C=GR, O=Hellenic Academic and Research Institutions CA, CN=GEANT TLS RSA 1
```

Soit E l'algorithme de chiffrement RSA. La signature presente dans le certificat est calculee avec la cle privee de la CA emettrice, que l'on note `(n_CA, d_CA)`. On note M le contenu du certificat a signer (le `tbsCertificate`, c'est-a-dire tous les champs du certificat sauf la signature elle-meme) et H la fonction de hachage SHA-256.

La signature s'obtient par :

```text
S = H(M)^d_CA mod n_CA
```

La verification se fait avec la cle publique de la CA, que l'on possede grace a son certificat `(n_CA, e_CA)`. On recalcule :

```text
H(M) = S^e_CA mod n_CA
```

et on compare le resultat avec le hachage du certificat recu. Si les deux valeurs sont identiques, la signature est valide : le certificat a bien ete signe par la CA et n'a pas ete modifie.

---

## Question 17 - Certificat de l'autorite de certification intermediaire

Le certificat de la CA qui a delivre le certificat du serveur est le certificat de niveau 1 de la chaine (`cert1.pem`) :

```text
$ openssl x509 -in cert1.pem -noout -subject -issuer -text
subject=C=GR, O=Hellenic Academic and Research Institutions CA, CN=GEANT TLS RSA 1
issuer=C=GR, O=Hellenic Academic and Research Institutions CA, CN=HARICA TLS RSA Root CA 2021
```

Le sujet de ce certificat est donc :

```text
C=GR, O=Hellenic Academic and Research Institutions CA, CN=GEANT TLS RSA 1
```

La taille de la cle publique presente dans ce certificat est de 3072 bits :

```text
Public Key Algorithm: rsaEncryption
    Public-Key: (3072 bit)
```

C'est logique : une cle de CA est plus longue qu'une cle de serveur (2048 bits), car elle sert a signer un grand nombre de certificats et doit resister plus longtemps aux attaques.

Ce certificat a ete signe par la CA racine `HARICA TLS RSA Root CA 2021`.

---

## Question 18 - Verification de la chaine de certification

Pour verifier la chaine, on compare pour chaque certificat de niveau n son emetteur (issuer) avec le sujet (subject) du certificat de niveau n-1, et on verifie la signature.

**Le certificat de niveau 0 (serveur) est valide par le certificat de niveau 1.**

- Le sujet de `cert1.pem` est `CN=GEANT TLS RSA 1`.
- L'emetteur de `cert0.pem` est `CN=GEANT TLS RSA 1`.
- L'identifiant de cle `Authority Key Identifier` de `cert0.pem` vaut `86:01:72:3F:8C:A9:70:E2:31:06:53:16:CE:01:5F:5B:79:C8:3C:3B`, ce qui correspond exactement au `Subject Key Identifier` de `cert1.pem`.

**Le certificat de niveau 1 est valide par le certificat de niveau 2.**

- Le sujet de `cert2.pem` est `CN=HARICA TLS RSA Root CA 2021`.
- L'emetteur de `cert1.pem` est `CN=HARICA TLS RSA Root CA 2021`.
- L'`Authority Key Identifier` de `cert1.pem` vaut `0A:48:23:A6:60:A4:92:0A:33:EA:93:5B:C5:57:EA:25:4D:BD:12:EE`, ce qui correspond au `Subject Key Identifier` de `cert2.pem`.

**Le certificat de dernier niveau (niveau 2) est valide par la CA racine.**

Le certificat `cert2.pem` n'est pas auto-signe ici : son emetteur est

```text
C=GR, L=Athens, O=Hellenic Academic and Research Institutions Cert. Authority, CN=Hellenic Academic and Research Institutions RootCA 2015
```

Il est donc valide par le certificat de la CA racine `Hellenic Academic and Research Institutions RootCA 2015`. Ce certificat ne se trouve pas dans la reponse du serveur : il est present dans le magasin de certificats de confiance du systeme d'exploitation (et dans les navigateurs), car c'est une autorite racine reconnue.

Sous Alma Linux (RedHat), ce magasin est constitue a partir du fichier indique dans la documentation de `update-ca-trust` :

```text
/etc/pki/ca-trust/extracted/openssl/ca-bundle.trust.crt
```

C'est dans ce fichier que l'on retrouve le certificat de la CA racine, que l'on extrait dans le fichier `root-ca1.pem`.

Il faut noter que le certificat `HARICA TLS RSA Root CA 2021` existe en deux versions : une version auto-signee (celle du magasin de confiance) et une version signee par la racine `HARICA RootCA 2015` (celle envoyee par le serveur). Les deux contiennent la meme cle publique, ce qui permet la verification.

---

## Question 19 - Le certificat racine et son auto-signature

Dans le certificat racine extrait dans `root-ca1.pem`, les champs subject et issuer sont identiques :

```text
subject=C=GR, O=Hellenic Academic and Research Institutions CA, CN=HARICA TLS RSA Root CA 2021
issuer =C=GR, O=Hellenic Academic and Research Institutions CA, CN=HARICA TLS RSA Root CA 2021
```

On en deduit que ce certificat est signe par lui-meme : c'est un certificat **auto-signe**. Il ne peut pas etre signe par une autre autorite, sinon il ne serait pas la racine de la chaine. C'est pour cette raison qu'il doit etre distribue et installe manuellement dans le magasin de confiance des clients : c'est le seul certificat de la chaine que l'on doit croire sur parole.

La signature de ce certificat a ete generee avec la cle privee de la CA racine elle-meme, notee `(n_root, d_root)` :

```text
S = H(M)^d_root mod n_root
```

avec M le contenu du certificat (tbsCertificate) et H la fonction de hachage SHA-256.

Ce type de certificat s'appelle un certificat racine, ou certificat auto-signe (self-signed).

---

## Question 20 - Etude de la CA racine Root Lorne

La CA racine est decrite dans le fichier `/home/camanager/ca/openssl.cnf`. La section `[ CA_default ]` indique l'emplacement de ses elements :

```text
$ grep -E "^(dir|private_key|certificate|policy)" ~/ca/openssl.cnf
dir = /home/camanager/ca
private_key = $dir/private/ca.key.pem
certificate = $dir/certs/ca.cert.pem
policy = policy_strict
```

Le certificat de la CA s'affiche avec :

```text
$ openssl x509 -in ~/ca/certs/ca.cert.pem -noout -text
```

### Type et taille de cle, courbe

La cle de la CA racine est une cle a courbe elliptique (`id-ecPublicKey`) de 256 bits, sur la courbe `prime256v1`, appelee aussi NIST P-256 :

```text
Public Key Algorithm: id-ecPublicKey
    Public-Key: (256 bit)
    ASN1 OID: prime256v1
    NIST CURVE: P-256
```

Une cle EC de 256 bits offre un niveau de securite comparable a une cle RSA de 3072 bits, pour une taille beaucoup plus petite. C'est ce qui justifie ce choix pour une autorite de certification.

### Duree de validite

```text
$ openssl x509 -in ~/ca/certs/ca.cert.pem -noout -dates
notBefore=Nov 12 12:43:56 2025 GMT
notAfter=Nov  7 12:43:56 2045 GMT
```

Le certificat est valable du 12 novembre 2025 au 7 novembre 2045, soit environ 20 ans. Une CA racine est delivree pour une tres longue duree, car changer de racine impose de reinstaller le certificat sur tous les clients.

### Certificat racine et auto-signe

Les champs `subject` et `issuer` du certificat sont identiques :

```text
$ openssl x509 -in ~/ca/certs/ca.cert.pem -noout -subject -issuer
subject=C=FR, ST=Savoie, L=Chambery, O=TP Securite, CN=Root Lorne
issuer =C=FR, ST=Savoie, L=Chambery, O=TP Securite, CN=Root Lorne
```

De plus, l'extension `Authority Key Identifier` contient la meme valeur que le `Subject Key Identifier` :

```text
X509v3 Subject Key Identifier:
    85:44:BC:D9:48:94:58:B7:90:E3:B0:65:31:CC:2C:23:2C:8F:5F:80
X509v3 Authority Key Identifier:
    85:44:BC:D9:48:94:58:B7:90:E3:B0:65:31:CC:2C:23:2C:8F:5F:80
```

C'est ce qui permet d'affirmer que le certificat est auto-signe : il est signe par sa propre cle privee. Comme il n'existe aucune autorite au-dessus de lui, c'est forcement le cas, c'est la definition d'une racine. Son authenticite repose uniquement sur le fait qu'il a ete installe manuellement dans le magasin de confiance des clients.

### Usages autorises

```text
$ openssl x509 -in ~/ca/certs/ca.cert.pem -noout -ext keyUsage,basicConstraints
X509v3 Basic Constraints: critical
    CA:TRUE
X509v3 Key Usage: critical
    Digital Signature, Certificate Sign, CRL Sign
```

L'extension `X509v3 Key Usage` autorise trois usages :

- `Digital Signature` : la cle peut signer (notamment les CRL et les reponses OCSP).
- `Certificate Sign` : la cle peut signer des certificats. Sans cet usage, l'autorite ne pourrait delivrer aucun certificat, et ne pourrait donc pas signer les certificats de CA intermediaires.
- `CRL Sign` : la cle peut signer les listes de revocation de certificats.

Ces usages sont marques `critical`, ce qui signifie qu'un client qui ne comprend pas cette extension doit refuser le certificat. Le `CA:TRUE` de `Basic Constraints` confirme qu'il s'agit d'une autorite de certification et non d'un certificat de serveur.

La cle privee de la CA est chiffree : la commande `openssl ec` demande une phrase de passe (la "cle de chiffrement florent" indiquee dans le sujet) avant d'afficher la cle :

```text
$ openssl ec -in ~/ca/private/ca.key.pem -text -noout
read EC key
Enter PEM pass phrase:
```

Cette protection est indispensable : la cle privee de la racine permet de signer n'importe quel certificat, donc d'usurper l'identite de n'importe quel serveur de la PKI.

---
