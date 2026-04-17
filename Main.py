def caesar_cipher(file, shift, mode="encrypt"):
    if mode not in ("encrypt", "decrypt"):
        raise ValueError("mode must be 'encrypt' or 'decrypt'")

    direction = 1 if mode == "encrypt" else -1
    output_suffix = "Ciphered" if mode == "encrypt" else "Deciphered"

    with open(f"{file}.txt", "r", encoding="utf-8") as infile,\
        open(f"Caesar_{output_suffix}_{file}.txt", "w", encoding="utf-8") as outfile:
            for line in infile:
                ciphered_line = ""
                for char in line:
                    if char.isalpha():
                        if char.islower():
                            base = ord('a')
                        else:
                            base = ord('A')

                        shifted_code = (ord(char) - base + direction * shift) % 26 + base
                        ciphered_line += chr(shifted_code)
                    else:
                        ciphered_line += char
                outfile.write(ciphered_line)


def vigenere_cipher(file, password, mode="encrypt"):
    if mode not in ("encrypt", "decrypt"):
        raise ValueError("mode must be 'encrypt' or 'decrypt'")

    direction = 1 if mode == "encrypt" else -1
    output_suffix = "Ciphered" if mode == "encrypt" else "Deciphered"
    password = password.lower()
    password_len = len(password)
    password_index = 0

    with open(f"{file}.txt", "r", encoding="utf-8") as infile,\
        open(f"Vigenere_{output_suffix}_{file}.txt", "w", encoding="utf-8") as outfile:
            for line in infile:
                ciphered_line = ""
                for char in line:
                    if char.isalpha():
                        shift = ord(password[password_index % password_len]) - ord('a')
                        if char.islower():
                            base = ord('a')
                        else:
                            base = ord('A')

                        shifted_code = (ord(char) - base + direction * shift) % 26 + base
                        ciphered_line += chr(shifted_code)
                        password_index += 1
                    else:
                        ciphered_line += char
                outfile.write(ciphered_line)

caesar_cipher("Message", 3, "encrypt")
caesar_cipher("Caesar_Ciphered_Message", 3, "decrypt")

vigenere_cipher("Message", "key", "encrypt")
vigenere_cipher("Vigenere_Ciphered_Message", "key", "decrypt")