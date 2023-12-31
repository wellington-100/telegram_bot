BASE = "https://www.curs.md/ro/office/"

PATHS = {
    "bcr":  "bcr",
    "comert": "comertbank",
    "energ":  "energbank",
    "ecb":  "ecb",
    "exim":  "eximbank",
    "fincom":  "fincombank",
    "maib":  "maib",
    "micb":  "micb",
    "otp":  "mobiasbanca",
    "victoria":  "victoriabank",

    "ebanknotes1":    "everest",
    "ebanknotes2":    "oantaf2",
    "ebanknotes3":    "oantaf3",

    "adalan":         "adalan",

    "armetis":    "armetis",
    "armetis1":  "armetisf1",
    "armetis2":  "armetisf2",
    "armetis3":  "armetisf3",
    "armetis4":  "armetisf4",
    "armetis5":  "armetisf5",
    "arminius": "arminius",

    "avadaciocana":  "avada",
    "avadacentru":  "avadaf9",
    "avadagara":  "avadaf7",
    "ciocana":  "ciocana",

    "clio":    "clio",
    "clio1":      "cliof1",
    "clio2":      "cliof2",
    "clio3":      "clioschimb",
    "clio4":      "cliof4",

    "deghest": "degh",
    "deghest1":   "deghf1",
    "deghest2":   "deghf2",

    "exclusiv": "exclusivschimb",
    "exclusiv1": "exclusivschimbf1",
    "exclusiv2": "exclusivschimbf2",

    "nelcat1": "nelcat",
    "nelcat2": "nelcatf1",
    
    "francunic":  "francunic",

    "arminius":  "arminius",
    "calisto":  "calistong",
    "oanta": "oanta"

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

