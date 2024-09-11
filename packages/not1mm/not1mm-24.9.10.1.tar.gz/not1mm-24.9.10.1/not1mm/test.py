import xmlrpc.client

target = "http://127.0.0.1:8421"
server = xmlrpc.client.ServerProxy(target)
adif = "<QSO_DATE:8>20150721<QSO_DATE_OFF:8>20150721<TIME_ON:4>1333<TIME_OFF:6>133436<CALL:5>N3FJP<FREQ:8>3.081500<MODE:0><RST_SENT:0><RST_RCVD:0><TX_PWR:0><NAME:5>Glenn<QTH:7>Bel Air<STATE:2>MD<VE_PROV:0><COUNTRY:13>United States<GRIDSQUARE:6>FM19tm<STX:0><SRX:0><SRX_STRING:0><STX_STRING:0><NOTES:0><IOTA:0><DXCC:0><QSL_VIA:0><QSLRDATE:0><QSLSDATE:0><eor>"
response = server.log.add_record(adif)
