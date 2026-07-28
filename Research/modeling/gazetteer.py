"""The altepetl gazetteer — the model's spine. Stdlib only.

First tranche, kickoff round 1: 75 altepetl / polities covering (a) the Basin of
Mexico lakeshore network, (b) the campaign corridor Veracruz -> Tenochtitlan and
the 1520-21 southern circuit, (c) the Codex Mendoza tribute-province capitals
that carry the extent of the tributary system, (d) the independent polities whose
independence IS the map's argument (Tlaxcallan, Metztitlan, Tototepec, Yopitzinco,
the Purépecha state).

NOT YET COVERED (recorded, so the register can hold it honestly): the full
Mendoza roster is ~38 provinces / ~400 tribute towns; this tranche carries every
province whose capital is confidently locatable plus the complete lakeshore
network, and omits ~9 poorly-located frontier provinces (Atlan, Oxitipan,
Tzicóac*, Quiauhteopan, Tlalcozauhtitlan, Malinaltepec, Cuahuacan, Petlacalco*,
Itzcuincuitlapilco) — *Tzicóac included with contested coordinates; Petlacalco is
an administrative unit around the capital, not a town. Register item B1-b.

Fields per entry (schema in Research/DATA-SCHEMA.md):
  slug            stable id, never recycled
  nahuatl         endonym, standard orthography with macrons where established
  exonym          the Spanish/colonial name a reader will recognise
  modern          modern successor settlement (the coordinate anchor)
  lat, lon        WGS84, the modern successor's centre unless noted
  group           'triple-alliance-core' | 'tributary' | 'independent' | 'rival-state'
                  | 'spanish-foundation'   (state at 1 Jan 1519, before the war)
  province        Codex Mendoza tribute province (tributaries only)
  entered         (year, ruler, manner) the polity entered the tributary system;
                  None for non-tributaries. Years are scholarly approximations ->
                  confidence field.
  role            six-word role note for the card fact row
  coord_conf      confidence in the location: good | moderate | contested
  entry_conf      confidence in the entered-tributary data
  note            what is contested, if anything

Sources (named per SOURCING-AND-LICENSING §1; page-level pins are register B1-c):
  [CM]  Codex Mendoza, tribute + conquest folios — Berdan & Anawalt (1992),
        The Codex Mendoza, UC Press; INAH digital edition codicemendoza.inah.gob.mx
  [GER] Gerhard (1972), A Guide to the Historical Geography of New Spain, CUP
        — identifications of Mendoza towns with modern settlements
  [SB]  Smith & Berdan (1996), Aztec Imperial Strategies, Dumbarton Oaks
        — province structure, strategic vs tributary provinces
  [HAS] Hassig (2006), Mexico and the Spanish Conquest, 2e — campaign geography
  [INE] coordinates read from the modern successor settlement (INEGI localities)

Run me:  python3 gazetteer.py
"""

from __future__ import annotations

CONFIDENCE = ("good", "moderate", "contested", "none")
GROUPS = ("triple-alliance-core", "tributary", "independent", "rival-state",
          "spanish-foundation")

# (slug, nahuatl, exonym, modern, lat, lon, group, province,
#  entered:(year, ruler, manner)|None, role, coord_conf, entry_conf, note)
_ROWS = [
    # ---- the Triple Alliance core -------------------------------------------
    ("tenochtitlan", "Mēxihco-Tenōchtitlan", "Tenochtitlán", "Mexico City (Centro)",
     19.4348, -99.1313, "triple-alliance-core", None, None,
     "island capital of the Mexica", "good", "good",
     "coordinate anchored on the Templo Mayor excavation"),
    ("tlatelolco", "Mēxihco-Tlatelōlco", "Tlatelolco", "Mexico City (Tlatelolco)",
     19.4506, -99.1372, "triple-alliance-core", "Tlatelolco",
     (1473, "Axayácatl", "conquest of the sister city"),
     "market twin-city of Tenochtitlan", "good", "good",
     "self-governing until 1473; its people supplied Book XII's informants"),
    ("texcoco", "Tetzcohco", "Texcoco", "Texcoco de Mora",
     19.5080, -98.8830, "triple-alliance-core", "Acolhuacan", None,
     "Acolhua capital, second alliance seat", "good", "good",
     "alliance co-founder 1428; split allegiance in 1520-21 is the war's hinge"),
    ("tlacopan", "Tlacopan", "Tacuba", "Tacuba (Mexico City)",
     19.4590, -99.1880, "triple-alliance-core", None, None,
     "Tepanec third seat of alliance", "good", "good", ""),

    # ---- Basin lakeshore network -------------------------------------------
    ("azcapotzalco", "Azcapotzalco", "Azcapotzalco", "Azcapotzalco (Mexico City)",
     19.4820, -99.1860, "tributary", "Petlacalco",
     (1428, "Itzcóatl", "conquest — fall of the Tepanec hegemony"),
     "former Tepanec imperial capital", "good", "good", ""),
    ("coyoacan", "Coyohuacan", "Coyoacán", "Coyoacán (Mexico City)",
     19.3467, -99.1617, "tributary", "Petlacalco",
     (1430, "Itzcóatl", "conquest"),
     "Tepanec town, causeway south shore", "good", "moderate", ""),
    ("culhuacan", "Cōlhuahcan", "Culhuacán", "Culhuacán (Mexico City)",
     19.3372, -99.1078, "tributary", "Petlacalco",
     (1430, "Itzcóatl", "conquest"),
     "old Toltec-heir prestige polity", "good", "moderate", ""),
    ("iztapalapa", "Iztapalapan", "Iztapalapa", "Iztapalapa (Mexico City)",
     19.3570, -99.0920, "tributary", "Petlacalco",
     (1430, "Itzcóatl", "absorbed into core"),
     "causeway town of Cuitláhuac's line", "good", "moderate", ""),
    ("mexicaltzingo", "Mexicaltzinco", "Mexicaltzingo", "Mexicaltzingo (Mexico City)",
     19.3620, -99.1150, "tributary", "Petlacalco",
     (1430, "Itzcóatl", "absorbed into core"),
     "small lakeshore town, south causeway", "moderate", "moderate", ""),
    ("huitzilopochco", "Huitzilopochco", "Churubusco", "Churubusco (Mexico City)",
     19.3550, -99.1500, "tributary", "Petlacalco",
     (1430, "Itzcóatl", "absorbed into core"),
     "springs town on south causeway", "good", "moderate", ""),
    ("xochimilco", "Xōchimīlco", "Xochimilco", "Xochimilco (Mexico City)",
     19.2571, -99.1030, "tributary", "Xochimilco",
     (1430, "Itzcóatl", "conquest"),
     "chinampa heartland of the south", "good", "good", ""),
    ("cuitlahuac", "Cuitláhuac", "Tláhuac", "Tláhuac (Mexico City)",
     19.2869, -99.0055, "tributary", "Xochimilco",
     (1433, "Itzcóatl", "conquest"),
     "island town between fresh lakes", "good", "moderate", ""),
    ("mizquic", "Mīzquic", "Mixquic", "San Andrés Míxquic",
     19.2258, -98.9600, "tributary", "Xochimilco",
     (1432, "Itzcóatl", "conquest"),
     "chinampa town, south lake edge", "good", "moderate", ""),
    ("chalco", "Chālco", "Chalco", "Chalco de Díaz Covarrubias",
     19.2647, -98.8975, "tributary", "Chalco",
     (1465, "Moctezuma I", "conquest after the long Chalco wars"),
     "confederation head, grain-rich southeast", "good", "good",
     "the 25-year Chalco wars; defected early to the coalition, Jan-Mar 1521"),
    ("tlalmanalco", "Tlālmanalco", "Tlalmanalco", "Tlalmanalco",
     19.2036, -98.8025, "tributary", "Chalco",
     (1465, "Moctezuma I", "conquest with Chalco"),
     "Chalca confederation seat", "good", "moderate", ""),
    ("amaquemecan", "Amaquēmehcan", "Amecameca", "Amecameca de Juárez",
     19.1238, -98.7664, "tributary", "Chalco",
     (1465, "Moctezuma I", "conquest with Chalco"),
     "Chalca seat under the volcanoes", "good", "moderate",
     "Cortés's November 1519 route passed through it"),
    ("chimalhuacan", "Chīmalhuahcan", "Chimalhuacán", "Chimalhuacán",
     19.4214, -98.9536, "tributary", "Acolhuacan",
     (1431, "alliance settlement", "folded into Acolhua domain"),
     "Acolhua lakeshore town", "good", "moderate", ""),
    ("huexotla", "Huexōtla", "Huexotla", "San Luis Huexotla",
     19.4780, -98.8670, "tributary", "Acolhuacan",
     (1431, "alliance settlement", "folded into Acolhua domain"),
     "walled Acolhua town by Texcoco", "good", "moderate", ""),
    ("coatlinchan", "Cōātl īchān", "Coatlinchán", "San Miguel Coatlinchán",
     19.4480, -98.8680, "tributary", "Acolhuacan",
     (1431, "alliance settlement", "folded into Acolhua domain"),
     "old Acolhua dynastic seat", "good", "moderate", ""),
    ("tepetlaoxtoc", "Tepetlaōztōc", "Tepetlaoxtoc", "Tepetlaoxtoc de Hidalgo",
     19.5730, -98.8200, "tributary", "Acolhuacan",
     (1431, "alliance settlement", "folded into Acolhua domain"),
     "Acolhua hill town", "good", "moderate", ""),
    ("otompan", "Otompan", "Otumba", "Otumba de Gómez Farías",
     19.6989, -98.7578, "tributary", "Acolhuacan",
     (1430, "Nezahualcóyotl", "reconquest of Acolhua domain"),
     "Otomí town, plain of Otumba", "good", "moderate",
     "the 7 July 1520 battle on its plain turned the retreat"),
    ("teotihuacan", "Teōtīhuahcan", "Teotihuacán", "San Juan Teotihuacán",
     19.6850, -98.8610, "tributary", "Acolhuacan",
     (1431, "alliance settlement", "folded into Acolhua domain"),
     "town by the ancient ruins", "good", "moderate", ""),
    ("acolman", "Ācōlman", "Acolman", "Acolman de Nezahualcóyotl",
     19.6370, -98.9120, "tributary", "Acolhuacan",
     (1431, "alliance settlement", "folded into Acolhua domain"),
     "Acolhua town, northeast shore", "good", "moderate", ""),
    ("ecatepec", "Ehcatepēc", "Ecatepec", "Ecatepec de Morelos",
     19.6010, -99.0600, "tributary", "Acolhuacan",
     (1428, "Itzcóatl", "absorbed with Tepanec fall"),
     "north lake narrows town", "good", "moderate", ""),
    ("xaltocan", "Xāltocān", "Xaltocan", "Santa Ana Xaltocan",
     19.7120, -99.0890, "tributary", "Hueypoxtla",
     (1395, "Tepanec conquest; alliance after 1428", "conquest"),
     "Otomí island polity, north lakes", "good", "moderate",
     "a major independent state until its 1395 fall"),
    ("zumpango", "Tzompanco", "Zumpango", "Zumpango de Ocampo",
     19.7970, -99.0990, "tributary", "Hueypoxtla",
     (1428, "Itzcóatl", "absorbed with Tepanec fall"),
     "north basin lakeshore town", "good", "moderate", ""),
    ("citlaltepec", "Citlaltepēc", "Citlaltepec", "San Juan Zitlaltepec",
     19.8230, -99.1280, "tributary", "Hueypoxtla",
     (1428, "Itzcóatl", "absorbed with Tepanec fall"),
     "northernmost lake town", "moderate", "moderate", ""),
    ("cuauhtitlan", "Cuauhtitlan", "Cuautitlán", "Cuautitlán",
     19.6720, -99.1810, "tributary", "Cuauhtitlan",
     (1430, "Itzcóatl", "absorbed with Tepanec fall"),
     "province head, northwest basin", "good", "moderate",
     "its annals are a major native source"),
    ("tenayuca", "Tenayohcan", "Tenayuca", "Tenayuca (Tlalnepantla)",
     19.5270, -99.1690, "tributary", "Cuauhtitlan",
     (1428, "Itzcóatl", "absorbed with Tepanec fall"),
     "old Chichimec seat, west shore", "good", "moderate", ""),
    ("tultitlan", "Tōltitlan", "Tultitlán", "Tultitlán de Mariano Escobedo",
     19.6450, -99.1690, "tributary", "Cuauhtitlan",
     (1428, "Itzcóatl", "absorbed with Tepanec fall"),
     "Tepanec-sphere town", "good", "moderate", ""),
    ("tepotzotlan", "Tepotzohtlan", "Tepotzotlán", "Tepotzotlán",
     19.7160, -99.2240, "tributary", "Cuauhtitlan",
     (1428, "Itzcóatl", "absorbed with Tepanec fall"),
     "northwest valley town", "good", "moderate", ""),

    # ---- the campaign corridor and the southern circuit ---------------------
    ("cempoala", "Cēmpoallān", "Cempoala", "Zempoala (Úrsulo Galván)",
     19.4460, -96.4040, "tributary", "Cuetlaxtlan",
     (1458, "Moctezuma I", "conquest of the Totonac coast"),
     "Totonac city, first Cortés ally", "good", "moderate",
     "its 'fat cacique' aired the tribute grievance the coalition was built on"),
    ("quiahuiztlan", "Quiyahuiztlān", "Quiahuiztlan", "Quiahuiztlán ruins (Actopan)",
     19.6720, -96.3960, "tributary", "Cuetlaxtlan",
     (1458, "Moctezuma I", "conquest of the Totonac coast"),
     "clifftop Totonac town, first landfall ally", "good", "moderate", ""),
    ("xicochimalco", "Xicochimalco", "Xico", "Xico Viejo (Veracruz)",
     19.4220, -97.0100, "tributary", "Cuetlaxtlan",
     (1458, "Moctezuma I", "conquest"),
     "highland-road town above the coast", "moderate", "moderate", ""),
    ("tlaxcala", "Tlaxcallān", "Tlaxcala", "Tlaxcala de Xicohténcatl",
     19.3180, -98.2380, "independent", None, None,
     "independent Nahua confederation of four", "good", "good",
     "never tributary; blockaded; the coalition's core from Sept 1519"),
    ("huexotzinco", "Huexōtzinco", "Huejotzingo", "Huejotzingo",
     19.1590, -98.4070, "independent", None, None,
     "independent altepetl between volcanoes", "good", "moderate",
     "flower-war rival of the Mexica; sought Mexica help against Tlaxcala 1512-15; joined the coalition 1519"),
    ("cholula", "Chōlōllān", "Cholula", "San Pedro Cholula",
     19.0633, -98.3064, "independent", None, None,
     "holy city of Quetzalcóatl", "good", "moderate",
     "independent but Mexica-aligned by 1519; the October 1519 massacre is the war's most contested episode"),
    ("calpan", "Calpan", "Calpan", "San Andrés Calpan",
     19.1040, -98.4630, "independent", None, None,
     "small altepetl allied to Huexotzinco", "moderate", "moderate", ""),
    ("tepeaca", "Tepeyacac", "Tepeaca", "Tepeaca (Puebla)",
     18.9670, -97.9000, "tributary", "Tepeacac",
     (1466, "Moctezuma I", "conquest"),
     "province head on the eastern road", "good", "good",
     "retaken by Cortés Aug-Sep 1520; Segura de la Frontera founded there"),
    ("itzocan", "Itzōcan", "Izúcar", "Izúcar de Matamoros",
     18.5990, -98.4670, "tributary", "Tepeacac",
     (1450, "Moctezuma I", "conquest"),
     "garrison town on the southern road", "good", "moderate", ""),
    ("cuauhquechollan", "Cuauhquechōllan", "Huaquechula", "Huaquechula",
     18.7700, -98.5450, "tributary", "Tepeacac",
     (1450, "Moctezuma I", "conquest"),
     "altepetl that turned on its garrison", "good", "moderate",
     "its 1520 defection ambushed the Mexica garrison; its lienzo records the war from an ally's view"),
    ("quauhnahuac", "Cuauhnāhuac", "Cuernavaca", "Cuernavaca",
     18.9186, -99.2343, "tributary", "Cuauhnahuac",
     (1439, "Itzcóatl / Moctezuma I", "conquest, then reconsolidation"),
     "cotton-rich province head, warm lands", "good", "moderate", ""),
    ("huaxtepec", "Huaxtepēc", "Oaxtepec", "Oaxtepec",
     18.9050, -98.9720, "tributary", "Huaxtepec",
     (1450, "Moctezuma I", "conquest"),
     "garden province head of Morelos", "good", "moderate", ""),
    ("yauhtepec", "Yauhtepēc", "Yautepec", "Yautepec de Zaragoza",
     18.8830, -99.0670, "tributary", "Huaxtepec",
     (1450, "Moctezuma I", "conquest"),
     "warm-lands tribute town", "good", "moderate", ""),
    ("yacapichtla", "Yacapichtlān", "Yecapixtla", "Yecapixtla",
     18.8840, -98.8650, "tributary", "Huaxtepec",
     (1450, "Moctezuma I", "conquest"),
     "hill town above the warm lands", "good", "moderate", ""),
    ("ayotzinco", "Ayōtzinco", "Ayotzingo", "San Juan / Santa Catarina Ayotzingo",
     19.2080, -98.9250, "tributary", "Chalco",
     (1465, "Moctezuma I", "conquest with Chalco"),
     "lake port where the causeway road began", "moderate", "moderate",
     "Cortés's column embarked the lake edge here, November 1519"),
    ("malinalco", "Malinalco", "Malinalco", "Malinalco",
     18.9480, -99.4940, "tributary", "Malinalco",
     (1476, "Axayácatl", "conquest of the Matlatzinca lands"),
     "rock-shrine town southwest of basin", "good", "moderate", ""),
    ("tolocan", "Tōllohcan", "Toluca", "Toluca de Lerdo",
     19.2880, -99.6570, "tributary", "Tulucan",
     (1478, "Axayácatl", "conquest of the Matlatzinca"),
     "Matlatzinca valley province head", "good", "moderate", ""),
    ("ocuilan", "Ocuillan", "Ocuilan", "Ocuilan de Arteaga",
     18.9780, -99.4000, "tributary", "Ocuilan",
     (1476, "Axayácatl", "conquest"),
     "hill province head by Malinalco", "good", "moderate", ""),

    # ---- Mendoza province capitals carrying the wider system ----------------
    ("tlachco", "Tlachco", "Taxco", "Taxco de Alarcón",
     18.5560, -99.6050, "tributary", "Tlachco",
     (1445, "Moctezuma I", "conquest"),
     "mining province head, Guerrero north", "good", "moderate", ""),
    ("tepequacuilco", "Tepecuacuilco", "Tepecoacuilco", "Tepecoacuilco de Trujano",
     18.2830, -99.4630, "tributary", "Tepequacuilco",
     (1445, "Moctezuma I", "conquest"),
     "Balsas-corridor province head", "moderate", "moderate", ""),
    ("tlappan", "Tlappān", "Tlapa", "Tlapa de Comonfort",
     17.5460, -98.5760, "tributary", "Tlapan",
     (1486, "Ahuítzotl", "conquest of the Tlapanec kingdom"),
     "Tlapanec province head, the Montaña", "good", "moderate", ""),
    ("cihuatlan", "Cihuatlān", "Cihuatlán", "Zihuatanejo region",
     17.6400, -101.5500, "tributary", "Cihuatlan",
     (1497, "Ahuítzotl", "conquest of the coast"),
     "Pacific-coast province, 'place of women'", "contested", "moderate",
     "the Mendoza town's exact site is debated; drawn at the modern bay"),
    ("xilotepec", "Xīlotepēc", "Jilotepec", "Jilotepec de Molina Enríquez",
     19.9520, -99.5320, "tributary", "Xilotepec",
     (1470, "Axayácatl", "conquest of the Otomí north"),
     "Otomí province head, northwest march", "good", "moderate", ""),
    ("chiapan", "Chiyappan", "Chapa de Mota", "Chapa de Mota",
     19.8130, -99.5270, "tributary", "Xilotepec",
     (1470, "Axayácatl", "conquest"),
     "Otomí hill town of the march", "good", "moderate", ""),
    ("xocotitlan", "Xocotitlan", "Jocotitlán", "Jocotitlán",
     19.7070, -99.7870, "tributary", "Xocotitlan",
     (1478, "Axayácatl", "conquest of the Mazahua"),
     "Mazahua province head", "good", "moderate", ""),
    ("axocopan", "Axocopan", "Ajacuba", "Ajacuba",
     20.0930, -99.1210, "tributary", "Axocopan",
     (1435, "Itzcóatl / Moctezuma I", "absorbed northward"),
     "maguey-lands province head", "good", "moderate", ""),
    ("atotonilco-grande", "Ātotonilco", "Atotonilco el Grande", "Atotonilco el Grande",
     20.2890, -98.6690, "tributary", "Atotonilco el Grande",
     (1440, "Moctezuma I", "absorbed northward"),
     "province head toward the Huasteca", "good", "moderate",
     "the Mendoza lists two Atotonilcos; this is the eastern one"),
    ("hueypoxtla", "Hueypōchtlan", "Hueypoxtla", "Hueypoxtla",
     19.9130, -99.0780, "tributary", "Hueypoxtla",
     (1435, "Itzcóatl / Moctezuma I", "absorbed northward"),
     "salt-lands province head", "good", "moderate", ""),
    ("coayxtlahuacan", "Cōāīxtlahuahcan", "Coixtlahuaca", "San Juan Bautista Coixtlahuaca",
     17.7170, -97.3100, "tributary", "Coayxtlahuacan",
     (1458, "Moctezuma I", "conquest — fall of Atonal's Mixtec state"),
     "Mixteca province head, trade hub", "good", "good", ""),
    ("tlachquiauhco", "Tlachquiyauhco", "Tlaxiaco", "Heroica Ciudad de Tlaxiaco",
     17.2710, -97.6800, "tributary", "Tlachquiavco",
     (1511, "Moctezuma II", "conquest — the empire's last expansion"),
     "Mixteca alta province head", "good", "moderate", ""),
    ("coyolapan", "Coyolāpan", "Cuilapan", "Cuilápam de Guerrero",
     16.9970, -96.7820, "tributary", "Coyolapan",
     (1494, "Ahuítzotl", "conquest — Oaxaca valley garrison"),
     "Valley-of-Oaxaca province head", "good", "moderate", ""),
    ("tochtepec", "Tōchtepēc", "Tuxtepec", "San Juan Bautista Tuxtepec",
     18.0880, -96.1250, "tributary", "Tochtepec",
     (1461, "Moctezuma I", "conquest of the lowland trade road"),
     "cacao-and-feathers province head", "good", "moderate", ""),
    ("cuetlaxtlan", "Cuetlaxtlān", "Cotaxtla", "Cotaxtla",
     18.8340, -96.3950, "tributary", "Cuetlaxtlan",
     (1462, "Moctezuma I", "conquest of the Gulf lowlands"),
     "Gulf-coast province head", "good", "moderate", ""),
    ("quauhtochco", "Cuauhtōchco", "Huatusco", "Huatusco (Santiago)",
     19.1480, -96.9660, "tributary", "Quauhtochco",
     (1462, "Moctezuma I", "conquest"),
     "piedmont garrison province", "good", "moderate", ""),
    ("ahuilizapan", "Āhuilizāpan", "Orizaba", "Orizaba",
     18.8490, -97.1000, "tributary", "Quauhtochco",
     (1462, "Moctezuma I", "conquest"),
     "valley town on the trade road", "good", "moderate", ""),
    ("tochpan", "Tōchpan", "Tuxpan", "Túxpam de Rodríguez Cano",
     20.9550, -97.4080, "tributary", "Tochpan",
     (1457, "Moctezuma I", "conquest of the Huasteca coast"),
     "Huastec province head, north Gulf", "good", "moderate", ""),
    ("tzicoac", "Tzicōac", "Chicontepec region", "Chicontepec (approx.)",
     20.8500, -98.1000, "tributary", "Tzicoac",
     (1458, "Moctezuma I", "conquest of the Huasteca"),
     "Huastec frontier province", "contested", "moderate",
     "site identification debated (Gerhard); drawn near Chicontepec"),
    ("xoconochco", "Xoconōchco", "Soconusco", "Soconusco (Chiapas coast)",
     15.0000, -92.6000, "tributary", "Xoconochco",
     (1495, "Ahuítzotl", "long-distance conquest of the cacao coast"),
     "farthest province: cacao and quetzal", "moderate", "moderate",
     "500 km beyond the nearest tributary block — the empire as network, not surface"),
    ("teotitlan", "Teōtitlan", "Teotitlán del Camino", "Teotitlán de Flores Magón",
     18.1320, -97.0780, "independent", None, None,
     "client kingdom on the Oaxaca road", "good", "moderate",
     "allied-client status, not a Mendoza tribute province — the empire's edge was graded, not sharp"),

    # ---- the independent and rival polities — the map's argument ------------
    ("metztitlan", "Mētztitlān", "Metztitlán", "Metztitlán (Hidalgo)",
     20.5940, -98.7640, "independent", None, None,
     "independent Otomí-Nahua valley kingdom", "good", "good",
     "never conquered; a wedge of independence inside the tributary north"),
    ("tototepec", "Tōtotepēc", "Tututepec", "Villa de Tututepec",
     16.1320, -97.6050, "independent", None, None,
     "Mixtec coastal kingdom, never subdued", "good", "good", ""),
    ("yopitzinco", "Yopitzinco", "Yopitzinco", "Costa Chica interior (approx.)",
     16.9500, -98.9500, "independent", None, None,
     "Yope enclave the empire ringed", "contested", "good",
     "location approximate — an unconquered pocket surrounded by tributary provinces"),
    ("tzintzuntzan", "Tzintzuntzan", "Tzintzuntzán", "Tzintzuntzan (Michoacán)",
     19.6280, -101.5790, "rival-state", None, None,
     "Purépecha imperial capital", "good", "good",
     "the other empire: defeated Axayácatl c. 1478; submitted to Spain 1522 without siege"),

    # ---- Spanish foundations inside the window ------------------------------
    ("villa-rica", "—", "Villa Rica de la Vera Cruz", "Villa Rica (Actopan)",
     19.6750, -96.3960, "spanish-foundation", None, None,
     "first Spanish town, April 1519", "good", "good",
     "the legal device that unhooked the company from Cuba"),
]

# Principal tribute of the province, per the Codex Mendoza tribute folios
# ([CM], Berdan & Anawalt 1992) — staples only, phrased as the folios group
# them; confidence 'moderate' (folio-level pinning is register B2-b).
GOODS = {
    "quauhnahuac": "cotton mantles, loincloths and skirts; bark paper",
    "huaxtepec": "cotton cloth; bark paper; warriors' costumes",
    "chalco": "maize, beans and chia — the Basin's granary",
    "xochimilco": "maize and garden produce of the chinampas",
    "cuauhtitlan": "mantles; chillies; lime",
    "axocopan": "maguey syrup; mantles",
    "atotonilco-grande": "maguey syrup; mantles",
    "hueypoxtla": "lime; maguey fibre cloth",
    "xilotepec": "Otomí cloth; live eagles",
    "tolocan": "maize; mantles of maguey fibre",
    "tlachco": "warriors' costumes; copal",
    "tepequacuilco": "copal; gourd bowls; gold discs",
    "tlappan": "gold dust in gourds; jaguar-skin warrior costumes",
    "cihuatlan": "cacao; cotton; red spondylus shells",
    "coayxtlahuacan": "greenstones; quetzal feathers; gold dust; cochineal",
    "coyolapan": "gold dust; cochineal; mantles",
    "tlachquiauhco": "gold dust; quetzal feathers",
    "tochtepec": "quetzal and tropical feathers; cacao; rubber; gold",
    "xoconochco": "cacao; quetzal feathers; jaguar pelts; amber",
    "cuetlaxtlan": "rich mantles; greenstones; feathers",
    "quauhtochco": "mantles; maize",
    "tochpan": "mantles; chillies; Huastec cloth",
    "tzicoac": "mantles; chillies",
    "tepeaca": "lime; carrying-frames; flint blades; captives for sacrifice",
}

ENTRIES = [
    {"slug": r[0], "nahuatl": r[1], "exonym": r[2], "modern": r[3],
     "lat": r[4], "lon": r[5], "group": r[6], "province": r[7],
     "entered": r[8], "role": r[9], "coord_conf": r[10], "entry_conf": r[11],
     "note": r[12], "goods": GOODS.get(r[0]),
     "sources": ["[CM] Codex Mendoza (Berdan & Anawalt 1992)",
                 "[GER] Gerhard (1972)", "[INE] modern successor coordinates"]
                + (["[SB] Smith & Berdan (1996)"] if r[7] else [])
                + (["[HAS] Hassig (2006)"] if r[6] != "tributary" else [])}
    for r in _ROWS
]

BY_SLUG = {e["slug"]: e for e in ENTRIES}

# Bounding box sanity: Mesoamerica, and the Basin for basin-group towns.
MESOAMERICA = (13.0, 23.0, -106.0, -92.0)      # lat0, lat1, lon0, lon1
BASIN = (19.0, 20.0, -99.5, -98.6)

BASIN_PROVINCES = {"Petlacalco", "Acolhuacan", "Cuauhtitlan", "Hueypoxtla",
                   "Chalco", "Xochimilco", "Tlatelolco"}


def provinces():
    """Mendoza provinces present in this tranche, with their towns."""
    out = {}
    for e in ENTRIES:
        if e["province"]:
            out.setdefault(e["province"], []).append(e["slug"])
    return out


def at_1519(slug: str) -> str:
    """Pre-war standing of a polity — the state machine's initial state."""
    return BY_SLUG[slug]["group"]


def _selftest():
    assert len(ENTRIES) == len(_ROWS)
    slugs = [e["slug"] for e in ENTRIES]
    assert len(slugs) == len(set(slugs)), "duplicate slugs"
    la0, la1, lo0, lo1 = MESOAMERICA
    for e in ENTRIES:
        assert e["group"] in GROUPS, e["slug"]
        assert e["coord_conf"] in CONFIDENCE and e["entry_conf"] in CONFIDENCE, e["slug"]
        assert la0 <= e["lat"] <= la1 and lo0 <= e["lon"] <= lo1, \
            f"{e['slug']} outside Mesoamerica bbox: {e['lat']},{e['lon']}"
        assert e["sources"], e["slug"]
        # tributaries carry a province and an entry; independents carry neither
        if e["group"] == "tributary":
            assert e["province"] and e["entered"], f"{e['slug']}: tributary without province/entry"
            y = e["entered"][0]
            assert 1370 <= y <= 1519, f"{e['slug']}: entry year {y} outside empire's span"
        if e["group"] in ("independent", "rival-state"):
            assert e["entered"] is None, f"{e['slug']}: independent with an entry record"
        # basin-province towns must sit inside the Basin bbox
        if e["province"] in BASIN_PROVINCES and e["slug"] != "cempoala":
            assert BASIN[0] <= e["lat"] <= BASIN[1] and BASIN[2] <= e["lon"] <= BASIN[3], \
                f"{e['slug']} tagged a Basin province but sits outside the Basin"
    # Cuetlaxtlan is a coastal province — exempt from the basin check by design.
    assert BY_SLUG["cempoala"]["province"] == "Cuetlaxtlan"

    # goods only on real tributary polities, and every GOODS key resolves
    for slug in GOODS:
        assert slug in BY_SLUG, f"GOODS references unknown {slug}"
        assert BY_SLUG[slug]["group"] == "tributary", f"{slug}: goods on a non-tributary"

    # The argument's anchors must be present and correctly grouped.
    assert at_1519("tlaxcala") == "independent"
    assert at_1519("tzintzuntzan") == "rival-state"
    assert at_1519("tenochtitlan") == "triple-alliance-core"
    assert BY_SLUG["tlatelolco"]["entered"][0] == 1473

    # Entry years never postdate the war.
    print(f"selftest OK — {len(ENTRIES)} polities, {len(provinces())} Mendoza provinces "
          f"represented, groups: "
          + ", ".join(f"{g}={sum(1 for e in ENTRIES if e['group']==g)}" for g in GROUPS))


if __name__ == "__main__":
    _selftest()
    print("\nprovince roster in this tranche:")
    for p, towns in sorted(provinces().items()):
        print(f"  {p:22} {', '.join(towns)}")
