#########################################
# Словарь соответствия валют и флагов
currency_flags = {
    "MDL": "\U0001F1F2\U0001F1E9",  # Флаг Молдовы
    "USD": "\U0001F1FA\U0001F1F8",  # Флаг США
    "EUR": "\U0001F1EA\U0001F1FA",  # Флаг Евросоюза
    "GBP": "\U0001F1EC\U0001F1E7",  # Флаг Великобритании
    "JPY": "\U0001F1EF\U0001F1F5",  # Флаг Японии
    "RUB": "\U0001F1F7\U0001F1FA",  # Флаг России
    "RON": "\U0001F1F7\U0001F1F4",  # Флаг Румынии
    "UAH": "\U0001F1FA\U0001F1E6",  # Флаг Украины
    "AED": "\U0001F1E6\U0001F1EA",  # Флаг ОАЭ
    "ALL": "\U0001F1E6\U0001F1F1",  # Флаг Албании
    "AMD": "\U0001F1E6\U0001F1F2",  # Флаг Армении
    "AUD": "\U0001F1E6\U0001F1FA",  # Флаг Австралии
    "AZN": "\U0001F1E6\U0001F1FF",  # Флаг Азербайджана
    "BGN": "\U0001F1E7\U0001F1EC",  # Флаг Болгарии
    "BYN": "\U0001F1E7\U0001F1FE",  # Флаг Беларуси
    "CAD": "\U0001F1E8\U0001F1E6",  # Флаг Канады
    "CHF": "\U0001F1E8\U0001F1ED",  # Флаг Швейцарии
    "CNY": "\U0001F1E8\U0001F1F3",  # Флаг Китая
    "CZK": "\U0001F1E8\U0001F1FF",  # Флаг Чехии
    "DKK": "\U0001F1E9\U0001F1F0",  # Флаг Дании
    "GEL": "\U0001F1EC\U0001F1EA",  # Флаг Грузии
    "HKD": "\U0001F1ED\U0001F1F0",  # Флаг Хорватии
    "HRK": "\U0001F1ED\U0001F1F7",  # Флаг Гонконга
    "HUF": "\U0001F1ED\U0001F1FA",  # Флаг Венгрии
    "ILS": "\U0001F1EE\U0001F1F1",  # Флаг Израиля
    "INR": "\U0001F1EE\U0001F1F3",  # Флаг Индии
    "ISK": "\U0001F1EE\U0001F1F8",  # Флаг Исландии
    "KGS": "\U0001F1F0\U0001F1EC",  # Флаг Кыргызстана
    "KRW": "\U0001F1F0\U0001F1F7",  # Флаг Южной Кореи
    "KWD": "\U0001F1F0\U0001F1FC",  # Флаг Кувейта
    "KZT": "\U0001F1F0\U0001F1FF",  # Флаг Казахстана
    "MKD": "\U0001F1F2\U0001F1F0",  # Флаг Северной Македонии
    "MYR": "\U0001F1F2\U0001F1FE",  # Флаг Малайзии
    "NOK": "\U0001F1F3\U0001F1F4",  # Флаг Норвегии
    "NZD": "\U0001F1F3\U0001F1FF",  # Флаг Новой Зеландии
    "PLN": "\U0001F1F5\U0001F1F1",  # Флаг Польши
    "RSD": "\U0001F1F7\U0001F1F8",  # Флаг Сербии
    "SEK": "\U0001F1F8\U0001F1EA",  # Флаг Швеции
    "TJS": "\U0001F1F9\U0001F1EF",  # Флаг Таджикистана
    "TMT": "\U0001F1F9\U0001F1F2",  # Флаг Туркменистана
    "TRY": "\U0001F1F9\U0001F1F7",  # Флаг Турции
    "UZS": "\U0001F1FA\U0001F1FF",  # Флаг Узбекистана
    "EGP": "\U0001F1EA\U0001F1EC",
    "THB": "\U0001F1F9\U0001F1ED", # Флаг Тайланда
    "XDR": "\U0001F310"  # Специальные права заимствования (SDR)
}

currency_codes = [
    "MDL", #  Молдовы
    "USD", #  США
    "EUR", #  Евросоюза
    "GBP", #  Великобритании
    "JPY", #  Японии
    "RUB", #  России
    "RON", #  Румынии
    "UAH", #  Украины
    "AED", #  ОАЭ
    "ALL", #  Албании
    "AMD", #  Армении
    "AUD", #  Австралии
    "AZN", #  Азербайджана
    "BGN", #  Болгарии
    "BYN", #  Беларуси
    "CAD", #  Канады
    "CHF", #  Швейцарии
    "CNY", #  Китая
    "CZK", #  Чехии
    "DKK", #  Дании
    "GEL", #  Грузии
    "HKD", #  Хорватии
    "HRK", #  Гонконга
    "HUF", #  Венгрии
    "ILS", #  Израиля
    "INR", #  Индии
    "ISK", #  Исландии
    "KGS", #  Кыргызстана
    "KRW", #  Южной Кореи
    "KWD", #  Кувейта
    "KZT", #  Казахстана
    "MKD", #  Северной Македонии
    "MYR", #  Малайзии
    "NOK", #  Норвегии
    "NZD", #  Новой Зеландии
    "PLN", #  Польши
    "RSD", #  Сербии
    "SEK", #  Швеции
    "TJS", #  Таджикистана
    "TMT", #  Туркменистана
    "TRY", #  Турции
    "UZS", #  Узбекистана
    "EGP", # Египта
    "THB", # Тайлайнда 
    "XDR"# Специальные права заимствования (SDR)
]

currency_commands = [
    "/usd Dolar S.U.A",
    "/eur Euro",
    "/rub Rublă rusească",
    "/ron Leu românesc",
    "/uah Hrivnă ucraineană",
    "/gbp Liră sterlină",
    "/chf Franc elvețian",
    "/try Liră turcească",
    "/cad Dolar canadian",
    "/pln Zlot polenez",
    "/czk Coroană cehă",
    "/ils Shekel israelian",
    "/byn Rublă bielorusă",
    "/bgn Levă bulgară",
    "/dkk Coroană daneză",
    "/nok Coroană norvegiană",
    "/sek Coroană suedeză",
    "/isk Coroană islandeză",
    "/huf Forint ungar",
    "/aed Dirham E.A.U.",
    "/aud Dolar australian",
    "/hkd Dolar Hong Kong",
    "/hrk Kună croată",
    "/nzd Dolar neozelandez",
    "/all Lek albanez",
    "/amd Dram armenesc",
    "/azn Manat azer",
    "/jpy Yen Japonez",
    "/cny Yuan chinezesc",
    "/egp Liră egipteană",
    "/gel Lari georgian",
    "/inr Rupie indiană",
    "/kgs Som kirghiz",
    "/krw Won sud-coreean",
    "/kwd Dolar kuweitean",
    "/kzt Tenghe kazah",
    "/mkd Dinar macedioan",
    "/myr Ringgit malayezian",
    "/rsd Dinar sârb",
    "/thb Bath tailandez",
    "/tjs Somoni tadjic",
    "/tmt Manat turkmen",
    "/uzs Sum uzbec",
]

banks = [
    "/bnm Banca Națională a Moldovei",
    "/bcr Banca Comercială Română",
    "/comert Comerțbank",
    "/energ Energbank",
    "/ecb EuroCreditBank",
    "/exim EximBank",
    "/fincom FinComBank",
    "/maib Moldova Agroinbank",
    "/micb Moldincombank",
    "/otp OPT Bank",
    "/victoria Victoriabank",
]

exchanges = [
    "/abanknotes aBANKnotes",
    "/adalan Adalan-Com",
    "/armetis Armetis-Grup",
    "/arminius Arminius",
    "/avada Avada Invest",
    "/bancassurance Bancassurance",
    "/bonifar Bonifar-Com",
    "/prometeu Bălți Prometeu",
    "/nelus Nelus-Grup",
    "/clio Clio",
    "/casso Casso",
    "/dalion Dalion",
    "/deghest Deghest",
    "/euroschimb Euro Schimb",
    "/exclusiv Exclusiv-Schimb",
    "/ghestrat Ghestrat",
    "/grafitis Grafitis",
    "/lozcoz Lozcoz",
    "/matco Mațco Trade",
    "/milinex Milinex-com",
    "/mixolidia Mixolidia",
    "/nichi Nichi-schimb",
    "/oanta Oanță-Schimb",
    "/profx PRO-FX Schimb",
    "/ramforinh Ramforinh",
    "/rizavic Rizavic",
    "/schimbimpact Schimb Impact",
    "/trendline Trendline",
    "/vadisan Vadisan",
    "/valutaelit Valuta Elit",
    "/vandis Vandis-Schimb",
    "/francunic Francunic",
    "/franklin Franklin",
    "/eurus Eurus Trade SRL",
    
]