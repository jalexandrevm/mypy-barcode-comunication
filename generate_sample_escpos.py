from pathlib import Path

receipt = b''
# initialize printer
receipt += b'\x1b\x40'
# header centered and bold
receipt += b'\x1b\x61\x01'  # align center
receipt += b'\x1b\x45\x01'  # bold on
receipt += b'\x1d\x21\x11'  # double width+height
receipt += b'DOCUMENTO AUXILIAR NFC-e\n'
receipt += b'\x1b\x45\x00'  # bold off
receipt += b'\x1d\x21\x00'  # normal size
receipt += b'\x1b\x61\x00'  # align left
receipt += b'\n'
receipt += b'EMPRESA TESTE LTDA\n'
receipt += b'CNPJ: 12.345.678/0001-99\n'
receipt += b'IE: 123.456.789.012\n'
receipt += b'--------------------------------\n'
receipt += b'DESTINATARIO\n'
receipt += b'NOME: JOSE DA SILVA\n'
receipt += b'CPF: 000.000.000-00\n'
receipt += b'END: RUA EXEMPLO, 100\n'
receipt += b'BAIRRO: CENTRO  CEP: 12345-678\n'
receipt += b'--------------------------------\n'
receipt += b'ITEM                      TOTAL\n'
receipt += b'01 PRODUTO A      2 x 12,00  24,00\n'
receipt += b'02 SERVICO B      1 x 15,00  15,00\n'
receipt += b'03 ITEM C        3 x  5,50  16,50\n'
receipt += b'--------------------------------\n'
receipt += b'SUBTOTAL                 55,50\n'
receipt += b'DESCONTO                 0,00\n'
receipt += b'TOTAL                    55,50\n'
receipt += b'--------------------------------\n'
receipt += b'FORMA DE PAGAMENTO\n'
receipt += b'DINHEIRO                 30,00\n'
receipt += b'CARTAO DEBITO           25,50\n'
receipt += b'\n'
receipt += b'CHAVE DE ACESSO:\n'
receipt += b'1234 5678 9012 3456 7890 1234 5678 9012 3456 7890 1234 5678\n'
receipt += b'\n'
receipt += b'OBS: NFC-e EMITIDA APENAS PARA TESTE\n'
receipt += b'\n'
receipt += b'OBRIGADO PELA PREFERENCIA!\n'
receipt += b'\n'
receipt += b'\x1b\x61\x01'  # center again
receipt += b'VOLTE SEMPRE!\n'
receipt += b'\x1b\x61\x00'
receipt += b'\n\n\n'
receipt += b'\x1d\x56\x01'  # cut

path = Path('cupom_nfce_escpos.txt')
path.write_bytes(receipt)
print(f'Created {path} ({path.stat().st_size} bytes)')
