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

