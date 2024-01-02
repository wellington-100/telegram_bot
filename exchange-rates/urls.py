BASE = "https://www.curs.md/ro/office/"

PATHS = {
    "bcr":        "bcr",
    "comertbank": "comertbank",
    "energbank":  "energbank",
    "ecb":  "eurocreditbank",
    "eximbank":  "eximbank",
    "fincombank":  "fincombank",
    "maib":  "maib",
    "micb":  "micb",
    "otp":  "mobiasbanca",
    "victoriabank":  "victoriabank",

    "cliocsv":    "clio",
    "clio1":      "cliof1",
    "clio2":      "cliof2",
    "clio3":      "clioschimb",
    "clio4":      "cliof4",
    "deghestcsv": "degh",
    "deghest1":   "deghf1",
    "deghest2":   "deghf2",
    "francunic":  "francunic",
    "everest":    "everest",
    "armetisgrup":    "armetis",
    "armetis1":  "armetisf1",
    "armetis2":  "armetisf2",
    "armetis3":  "armetisf3",
    "armetis4":  "armetisf4",
    "armetis5":  "armetisf5",


    "arminius":  "arminius",
    "avada":  "avada",
    "calisto":  "calistong",

}

BASE_URLS = {key: BASE + value for key, value in PATHS.items()}

base_url = "https://www.curs.md/ro/office/"
suffixes = [
        "everest",
        "oantaf2",
        "oantaf3",
        "adalan",
        "armetis",
        "armetisf1",
        "armetisf2",
        "armetisf3",
        "armetisf4",
        "armetisf5",
        "avadaf9",
        "avadaf7",
        "beatel",
        "calistong",
        "ciocana",
        "clio",
        "cliof1",
        "cliof4",
        "clioschimb",
        "exclusivschimb",
        "exclusivschimbf1",
        "exclusivschimbf2",
        "francunic/csv",
        "franklin",
        "lozcoz",
        "milinex",
        "milinexschimb",
        "nelcat",
        "nelcatf1",
        "nelus",
        "nichi",
        "oanta",
        "orion",
        "ramforinh",
        "vadisan",
        "valutaelit",

]
urls = [base_url + suffix for suffix in suffixes]

