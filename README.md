# 🔐 ChaCha20 Stream Cipher (RFC 8439) - Implémentation "From Scratch" en Python

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Security](https://img.shields.io/badge/Security-Cryptography-red.svg)
![RFC](https://img.shields.io/badge/IETF-RFC%208439-success.svg)

## 📌 Contexte du Projet
Ce projet a été réalisé dans le cadre de la sécurisation d'une plateforme web de gestion de parc informatique (SAÉ BUT Informatique). L'objectif principal est l'implémentation algorithmique de bas niveau, sans aucune dépendance à des librairies externes ("from scratch"), du chiffrement par flot **ChaCha20**.

ChaCha20, conçu par Daniel J. Bernstein, est aujourd'hui un standard de l'industrie (intégré notamment dans TLS 1.3) réputé pour sa vitesse d'exécution logicielle et sa résistance à la cryptanalyse. Notre implémentation respecte strictement les spécifications de la **RFC 8439** de l'IETF.

## ⚙️ Architecture et Fonctionnalités Implémentées

Le code est structuré de manière modulaire autour de deux fichiers principaux:

### 1. Le Moteur Cryptographique (`chacha20_fromscratch.py`)
Ce module encapsule la classe orientée objet `ChaCha20` et implémente la logique interne du chiffrement :

* **Matrice d'État (State Matrix) :** Initialisation de la matrice 4x4 (512 bits) comprenant les constantes magiques ("expand 32-byte k"), la clé secrète (256 bits), le compteur de bloc (32 bits, initialisé à 0 selon la norme) et le Nonce (96 bits). L'utilisation de la bibliothèque `struct` assure la conversion correcte des octets.
* **Mécanisme ARX (Addition, Rotation, XOR) :** Implémentation de la fonction `Quarter Round` pour apporter confusion (Addition modulaire 32 bits), diffusion (Rotation circulaire gauche) et non-linéarité (XOR).
* **Contrôle Strict de l'Architecture (32 bits) :** Python gérant nativement des entiers de taille arbitraire, des masques hexadécimaux (`& 0xffffffff`) ont été appliqués (notamment dans la méthode `_rotl`) pour forcer le comportement d'un registre matériel de 32 bits et éviter les dépassements de mémoire (overflow).
* **Génération du Keystream :** Exécution des 20 itérations de mélange (10 Column Rounds + 10 Diagonal Rounds) pour garantir un **Effet Avalanche** total. L'addition finale de l'état initial à l'état final transforme la permutation en une fonction à sens unique.
* **Sérialisation Little-Endian :** Utilisation de `struct.pack('<16I', *working_state)` pour garantir la conformité binaire de l'endianness exigée par la norme.
* **Chiffrement/Déchiffrement Involutif :** Application de l'opération XOR entre les fragments du message et le keystream généré. En raison de la propriété involutive du XOR, la méthode `decrypt` fait appel à la méthode `encrypt`.

### 2. Le Banc de Test et Validation (`chacha20_library.py`)
Ce script agit comme un système d'intégration automatisé pour prouver mathématiquement l'exactitude de l'implémentation :

* **Validation Croisée :** Le script chiffre un message avec notre classe `ChaCha20`, puis chiffre le même message, avec les mêmes paramètres (clé, nonce), en utilisant le module industriel de référence `Crypto.Cipher.ChaCha20` (PyCryptodome). Une vérification d'égalité stricte entre les deux flux de sortie valide notre implémentation de la RFC.
* **Simulation de Persistance :** Conversion du flux d'octets chiffré en chaîne hexadécimale via `.hex()` pour simuler une insertion sécurisée dans une base de données (ex: MariaDB), évitant la corruption par des caractères non-imprimables. Le résultat final est exporté dans un fichier de log (`resultat_sae.txt`).

## ⚠️ Notes sur la Mise en Production (Recommandations)
Ce projet est une implémentation **pédagogique**.
* **Performance :** Pour traiter des volumes massifs sur un serveur de production, une version pré-compilée en C ou exploitant les instructions vectorielles SIMD du processeur serait requise.
* **Cas d'usage (Gestion des mots de passe) :** Bien que ce projet illustre le fonctionnement de ChaCha20, les standards de sécurité pour le stockage de mots de passe en base de données recommandent l'utilisation de fonctions de hachage lentes (Argon2, Bcrypt). ChaCha20 est cependant idéal pour le chiffrement de flux réseau ou la protection de clés d'API réversibles.

## 📚 Références
* IETF RFC 8439 : *ChaCha20 and Poly1305 for IETF Protocols*.
* Daniel J. Bernstein : *ChaCha, a variant of Salsa20*.
