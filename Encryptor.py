class Encryptor:
    @staticmethod
    def xor_encrypt(text: str, key: str, encoding: str = "utf-8") -> str:
        """
        מצפין טקסט ב-XOR עם מפתח שהוא מחרוזת.
        מחזיר טקסט מוצפן בפורמט הקס.
        """
        if not key:
            raise ValueError("המפתח לא יכול להיות ריק")

        data = text.encode(encoding)
        key_bytes = key.encode(encoding)

        cipher_bytes = bytes([
            b ^ key_bytes[i % len(key_bytes)]
            for i, b in enumerate(data)
        ])

        cipher_hex = cipher_bytes.hex()
        print(cipher_hex)  # הדפסה לפי הבקשה
        return cipher_hex