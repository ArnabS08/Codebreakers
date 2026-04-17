with open("Message.txt", "r", encoding="utf-8") as infile,\
    open("MessageCopy.txt", "w", encoding="utf-8") as outfile:
        for line in infile:
            print(line.strip())
            outfile.write(line)
            outfile.write("This is a new line.\n")