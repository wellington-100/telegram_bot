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
    "EGP": "\U0001F1EA\U0001F1EC",  # Флаг Египта
    "THB": "\U0001F1F9\U0001F1ED",  # Флаг Тайланда
    "SGD": "\U0001F1F8\U0001F1EC",  # Флаг Сингапура
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
    "SGD", # Сингапура
    "XDR"# Специальные права заимствования (SDR)
]

currency_commands = [
    f"/usd {currency_flags['USD']} Dolar S.U.A",
    f"/eur  {currency_flags['EUR']} Euro",
    f"/rub  {currency_flags['RUB']} Rublă rusească",
    f"/ron  {currency_flags['RON']} Leu românesc",
    f"/uah {currency_flags['UAH']} Hrivnă ucraineană",
    f"/gbp {currency_flags['GBP']} Liră sterlină",
    f"/chf  {currency_flags['CHF']} Franc elvețian",
    f"/try   {currency_flags['TRY']} Liră turcească",
    f"/cad {currency_flags['CAD']} Dolar canadian",
    f"/pln  {currency_flags['PLN']} Zlot polonez",
    f"/czk {currency_flags['CZK']} Coroană cehă",
    f"/ils   {currency_flags['ILS']} Shekel israelian",
    f"/byn {currency_flags['BYN']} Rublă bielorusă",
    f"/bgn {currency_flags['BGN']} Levă bulgară",
    f"/dkk {currency_flags['DKK']} Coroană daneză",
    f"/nok {currency_flags['NOK']} Coroană norvegiană",
    f"/sek {currency_flags['SEK']} Coroană suedeză",
    f"/isk  {currency_flags['ISK']} Coroană islandeză",
    f"/huf  {currency_flags['HUF']} Forint ungar",
    f"/aed {currency_flags['AED']} Dirham E.A.U.",
    f"/aud {currency_flags['AUD']} Dolar australian",
    f"/hkd {currency_flags['HKD']} Dolar Hong Kong",
    f"/hrk  {currency_flags['HRK']} Kună croată",
    f"/nzd {currency_flags['NZD']} Dolar neozelandez",
    f"/sgd {currency_flags['SGD']} Dolar Singapore",
    f"/all   {currency_flags['ALL']} Lek albanez",
    f"/amd {currency_flags['AMD']} Dram armenesc",
    f"/azn {currency_flags['AZN']} Manat azer",
    f"/jpy  {currency_flags['JPY']} Yen Japonez",
    f"/cny {currency_flags['CNY']} Yuan chinezesc",
    f"/egp {currency_flags['EGP']} Liră egipteană",
    f"/gel  {currency_flags['GEL']} Lari georgian",
    f"/inr   {currency_flags['INR']} Rupie indiană",
    f"/kgs {currency_flags['KGS']} Som kirghiz",
    f"/krw {currency_flags['KRW']} Won sud-coreean",
    f"/kwd {currency_flags['KWD']} Dinar kuweit",
    f"/kzt   {currency_flags['KZT']} Tenghe kazah",
    f"/mkd {currency_flags['MKD']} Dinar macedonian",
    f"/myr  {currency_flags['MYR']} Ringgit malayezian",
    f"/rsd  {currency_flags['RSD']} Dinar sârb",
    f"/thb  {currency_flags['THB']} Bath tailandez",
    f"/tjs   {currency_flags['TJS']} Somoni tadjic",
    f"/tmt {currency_flags['TMT']} Manat turkmen",
    f"/uzs {currency_flags['UZS']} Sum uzbec",
    f"/xdr  {currency_flags['XDR']} Special drawing rights"
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