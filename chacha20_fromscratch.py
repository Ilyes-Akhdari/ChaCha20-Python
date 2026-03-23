import struct

class ChaCha20:
    """
    Implémentation de l'algorithme ChaCha20 selon la RFC 8439.
    SAE Cryptographie - IUT Vélizy
    """
    def __init__(self, key, nonce, counter=0):
        if len(key) != 32:
            raise ValueError("La clé doit faire 32 octets (256 bits)")
        if len(nonce) != 12:
            raise ValueError("Le nonce doit faire 12 octets (96 bits)")
        
        self.key = key
        self.nonce = nonce
        self.counter = counter
        # Constantes "expand 32-byte k"
        self.constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]

    def _rotl(self, x, n):
        """Rotation binaire vers la gauche (Bitwise Rotation)."""
        return ((x << n) & 0xffffffff) | (x >> (32 - n))

    def _quarter_round(self, x, a, b, c, d):
        """Le 'Quarter Round' : mélange de base de ChaCha20."""
        x[a] = (x[a] + x[b]) & 0xffffffff; x[d] ^= x[a]; x[d] = self._rotl(x[d], 16)
        x[c] = (x[c] + x[d]) & 0xffffffff; x[b] ^= x[c]; x[b] = self._rotl(x[b], 12)
        x[a] = (x[a] + x[b]) & 0xffffffff; x[d] ^= x[a]; x[d] = self._rotl(x[d], 8)
        x[c] = (x[c] + x[d]) & 0xffffffff; x[b] ^= x[c]; x[b] = self._rotl(x[b], 7)

    def _make_block(self, counter_val):
        """Génère un bloc de 64 octets de keystream."""
        # Construction de l'état initial (State)
        ctx = self.constants + list(struct.unpack('<8I', self.key)) + [counter_val] + list(struct.unpack('<3I', self.nonce))
        working_state = ctx[:]

        # 20 tours de mélange
        for _ in range(10):
            # Colonnes
            self._quarter_round(working_state, 0, 4, 8, 12)
            self._quarter_round(working_state, 1, 5, 9, 13)
            self._quarter_round(working_state, 2, 6, 10, 14)
            self._quarter_round(working_state, 3, 7, 11, 15)
            # Diagonales
            self._quarter_round(working_state, 0, 5, 10, 15)
            self._quarter_round(working_state, 1, 6, 11, 12)
            self._quarter_round(working_state, 2, 7, 8, 13)
            self._quarter_round(working_state, 3, 4, 9, 14)

        # Addition finale (État final + État initial)
        for i in range(16):
            working_state[i] = (working_state[i] + ctx[i]) & 0xffffffff
            
        return struct.pack('<16I', *working_state)

    def encrypt(self, plaintext):
        """Chiffre (ou déchiffre) des données."""
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
            
        encrypted = bytearray(len(plaintext))
        curr_counter = self.counter
        
        for i in range(0, len(plaintext), 64):
            keystream = self._make_block(curr_counter)
            curr_counter += 1
            chunk = plaintext[i : i + 64]
            for j in range(len(chunk)):
                encrypted[i + j] = chunk[j] ^ keystream[j]
                
        return bytes(encrypted)

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)

# --- Zone d'exécution si on lance ce fichier seul ---
if __name__ == "__main__":
    print("=== TEST MANUEL (FROM SCRATCH) ===")
    cle = b'0123456789abcdef0123456789abcdef'
    nonce = b'000000000001'
    msg = "Test de notre implémentation ChaCha20 !"
    
    cipher = ChaCha20(cle, nonce)
    res = cipher.encrypt(msg)
    print(f"Message clair : {msg}")
    print(f"Chiffré (hex) : {res.hex()}")
    
    decipher = ChaCha20(cle, nonce)
    print(f"Déchiffré     : {decipher.decrypt(res).decode()}")