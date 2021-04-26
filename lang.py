import googletrans

for abbr, lang in googletrans.LANGUAGES.items():
    print(abbr, lang)
