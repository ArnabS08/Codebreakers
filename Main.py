def caesar_cipher(file, shift):
      with open(f"{file}.txt", "r", encoding="utf-8") as infile,\
        open(f"Caesar_Ciphered_{file}.txt", "w", encoding="utf-8") as outfile:
            for line in infile:
                ciphered_line = ""
                for char in line:
                    if char.isalpha():
                        char_code = ord(char)
                        shifted_code = char_code + shift
                        if char.islower():   
                            if shifted_code > ord('z'):
                                shifted_code -= 26
                        elif char.isupper():
                            if shifted_code > ord('Z'):
                                shifted_code -= 26
                        ciphered_line += chr(shifted_code)
                    else:
                        ciphered_line += char
                print(ciphered_line.strip())
                outfile.write(ciphered_line)

caesar_cipher("Message", 3)