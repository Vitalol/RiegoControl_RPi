import sensors.rc_protocol as RCP
# Send measure
cadena_bytes = '00 01 04 13 03 00 00 20 41 01 00 00 A0 41 02 00 00 F0 41 03'
bytestream = bytes.fromhex(cadena_bytes.replace(' ', ''))
print(bytestream)
# send_measure =RCP.RCProtocolSendMeasure(
#     message=bytestream,
#     header=RCP.RCProtocolHeader(bytestream)
# )
# atributos = vars(send_measure)
# for atributo, valor in atributos.items():
#     print(atributo, ":", valor)

RCP.rc_protocol_handle_received_msg(bytestream)