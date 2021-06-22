from decimal import Decimal

__author__ = 'sune'
from sepa_credit_transfer import Document

document = Document("invoicing-2015-03-25", name="My company name")
my_ref = document.add_debtor_payment_block("Marvin Food Online ltd.", "IE12 AIBK 9334 5721 1531 19")

document.add_payment_to_debtor_payment_block(my_ref, "1082-invoice-dd", "Payment F2200", Decimal('1226.53'),
                                             "Sune's Sunny test deli", "BOFIIE2D", "IE19BOFI90003396375818")

document.add_payment_to_debtor_payment_block(my_ref, "1083-invoice-dd", "Payment F2201", Decimal('1326.00'),
                                             "Sune's Shady test deli", "BOFIIE3D", "IE19BOFI90008396375818")

file = open('/tmp/aibtest.xml', mode='wb')
file.write(str(document))
file.close()
