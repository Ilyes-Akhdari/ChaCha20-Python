from Crypto.Cipher import ChaCha20 as ChaCha20_Lib
# On importe notre propre classe du fichier précédent pour comparer
from chacha20_fromscratch import ChaCha20 as ChaCha20_Perso

def main():
    print("=== COMPARISON : LIBRAIRIE vs MANUEL ===")
    # Données communes
    key = b'0123456789abcdef0123456789abcdef' 
    nonce = b'000000000001' 
    plaintext = "Exemple de mot de passe à chiffrer pour la SAE"

    print(f"Clé utilisée   : {key.hex()}")
    print(f"Nonce utilisé  : {nonce.hex()}")
    print(f"Message        : {plaintext}")
    print("-" * 50)

    # 1. Utilisation de la librairie officielle (PyCryptodome)
    cipher_lib = ChaCha20_Lib.new(key=key, nonce=nonce)
    # Note: PyCryptodome gère le compteur automatiquement
    msg_lib = cipher_lib.encrypt(plaintext.encode('utf-8'))
    print(f"[LIBRAIRIE] Résultat : {msg_lib.hex()}")

    # 2. Utilisation de NOTRE code manuel
    cipher_perso = ChaCha20_Perso(key, nonce)
    msg_perso = cipher_perso.encrypt(plaintext)
    print(f"[MANUEL]    Résultat : {msg_perso.hex()}")

    # 3. Verdict
    print("-" * 50)
    if msg_lib == msg_perso:
        print("✅ SUCCÈS TOTAL : Votre implémentation est correcte !")
        print("   Ce résultat (hex) est prêt à être inséré en Base de Données.")
    else:
        print("❌ ERREUR : Les résultats diffèrent.")

    # Sauvegarde dans un fichier (Consigne Section 3)
    try:
        with open("resultat_sae.txt", "a") as f:
            f.write(f"admin:{msg_lib.hex()}\n")
        print("✅ Sauvegarde fichier OK")
    except:
        print("Pas de sauvegarde fichier")

if __name__ == "__main__":
    main()