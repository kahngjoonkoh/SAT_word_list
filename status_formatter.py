import csv
file = "word_lists/words3(alleviate-anomalous).csv"

word_list = {}
with open(file, 'r', encoding="utf8") as f:
    csv_reader = csv.reader(f)
    header = next(csv_reader)
    for row in csv_reader:
        word = row[0]
        form = row[1]
        definition = row[2]
        korean = row[3]
        example = row[4]
        related = row[5]
        status = row[6]
        word_list[word] = {"word": word, "form": form, "definition": definition, "korean": korean,
                                "example": example,
                                "related": related, "status": None}

fieldnames = ['word', 'form', 'definition', 'korean', 'example', 'related', 'status']
with open(file, 'w', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(word_list.values())