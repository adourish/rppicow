def getASCII(url):
response = urequests.get("https://static.wikia.nocookie.net/wombles/images/c/c5/Great_uncle_bulgaria_1990s.jpg")
im = Image.open(response.raw)
im = im.resize((80, 40), resample=Image.BICUBIC)
im = im.convert("L")
chars = "$@B%8WM#*oahkbdpwmZO0QlJYXzcvnxrjft/\|()1{}[]-_+~<>i!lI;:,"
for y in range(im.size[1]):
    row = []
    for x in range(im.size[0]):
        pixel = im.getpixel((x, y))
        char = chars[int(pixel / 256 * len(chars))]
        row.append(char)
    print("".join(row))