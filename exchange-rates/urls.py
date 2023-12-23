BASE = "https://www.curs.md/ro/office/"

PATHS = {
    "bcr":        "bcr",
    "comertbank": "comertbank",
    "energbank":  "energbank",
    "eurocreditbank":  "ecb",
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
}

BASE_URLS = {key: BASE + value for key, value in PATHS.items()}

