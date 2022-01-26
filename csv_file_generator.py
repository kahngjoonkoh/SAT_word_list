import csv
import requests
file = "word_lists/words7(blase-cacophonous).txt"

word_list = {}
with open(file, 'r', encoding="utf8") as f:
    for word in f.readlines():
        word.lower()
        word.strip()
        try:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            doc = requests.get(url).json()[0]
            print("doc success")
            word = doc['word']
            form = doc['meanings'][0]['partOfSpeech']
            print("fetched form")
            definition = doc['meanings'][0]['definitions'][0]['definition']
            print("fetched definition")
            korean = None
            example = doc['meanings'][0]['definitions'][0]['example']
            print("fetched example")
            related = None
            word_list[word] = {"word": word, "form": form, "definition": definition, "korean": korean,
                                    "example": example,
                                    "related": related, "status": None}
        except KeyError:
            print(f"{word}: failed")

fieldnames = ['word', 'form', 'definition', 'korean', 'example', 'related', 'status']
with open('word_lists/words7(blase-cacophonous).csv', 'w+', encoding='UTF8', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(word_list.values())