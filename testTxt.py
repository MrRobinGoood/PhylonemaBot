file = open("resources\quotes.txt",mode="r",encoding="utf8").read()
res = file.split('\n')

quotes = res[::2]
authors = res[1::2]
count = 0
for i in range(len(quotes)):
    count = count + 1
    print(count)
    print(quotes[i])
    print(authors[i])

