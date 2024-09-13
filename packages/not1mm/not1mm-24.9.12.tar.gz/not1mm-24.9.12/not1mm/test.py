import xmltodict

# import xmlrpc.client

# target = "http://127.0.0.1:8421"
# server = xmlrpc.client.ServerProxy(target)
# adif = "<QSO_DATE:8>20150721<QSO_DATE_OFF:8>20150721<TIME_ON:4>1333<TIME_OFF:6>133436<CALL:5>N3FJP<FREQ:8>3.081500<MODE:0><RST_SENT:0><RST_RCVD:0><TX_PWR:0><NAME:5>Glenn<QTH:7>Bel Air<STATE:2>MD<VE_PROV:0><COUNTRY:13>United States<GRIDSQUARE:6>FM19tm<STX:0><SRX:0><SRX_STRING:0><STX_STRING:0><NOTES:0><IOTA:0><DXCC:0><QSL_VIA:0><QSLRDATE:0><QSLSDATE:0><eor>"
# response = server.log.add_record(adif)


xml = '<?xml version="1.0"?>\n<HamQTH version="2.8" xmlns="https://www.hamqth.com">\n    <search>\n        <callsign>K6GTE</callsign>\n        <nick>Mike</nick>\n        <qth>Anaheim</qth>\n        <country>United States</country>\n        <adif>291</adif>\n        <itu>6</itu>\n        <cq>3</cq>\n        <grid>DM13AT</grid>\n        <adr_name>Michael C Bridak</adr_name>\n        <adr_street1>2854 W Bridgeport Ave</adr_street1>\n        <adr_city>Anaheim</adr_city>\n        <adr_zip>92804</adr_zip>\n        <adr_country>United States</adr_country>\n        <adr_adif>291</adr_adif>\n        <us_state>CA</us_state>\n        <us_county>Orange</us_county>\n        <lotw>Y</lotw>\n        <qsldirect>Y</qsldirect>\n        <qsl>?</qsl>\n        <eqsl>N</eqsl>\n        <email>michael.bridak@gmail.com</email>\n        <birth_year>1967</birth_year>\n        <lic_year>2017</lic_year>\n        <latitude>33.81</latitude>\n        <longitude>-117.97</longitude>\n        <continent>NA</continent>\n        <utc_offset>-8</utc_offset>\n        <picture>https://www.hamqth.com/userfiles/k/k6/k6gte/_header/header.jpg?ver=3</picture>\n    </search>\n</HamQTH>'
result = xmltodict.parse(xml)
print(f"{result=}")
