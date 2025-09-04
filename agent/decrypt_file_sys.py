#!/usr/bin/env python3
import sys
import codecs
def xor_decrypt_hex_string(data: str, key: str) -> bytes:
    """פענוח XOR על רצף בייטים"""
    encrypted_bytes = codecs.decode(data.strip().encode("utf-8"), 'hex')
    key_bytes = key.encode("utf-8")
    decrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(encrypted_bytes)])
    return decrypted

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} <input_file> <key>")
        sys.exit(1)

    input_file = sys.argv[1]
    key = sys.argv[2]

    try:
        with open(input_file, "r",encoding="utf-8") as f:
            encrypted_data = f.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)

    decrypted_data = xor_decrypt_hex_string(encrypted_data, key)

    # פלט למסך
    print(decrypted_data.decode("utf-8", errors="ignore"))

if __name__ == "__main__":
    main()
