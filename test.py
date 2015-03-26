from decimal import Decimal

__author__ = 'sune'
from sepa_credit_transfer import Document


document = Document("my-oin-no", "invoicing-2015-03-25")
my_ref = document.add_debtor_payment_block("Marvin Food Online ltd.", "My Iban Account no")

document.add_payment_to_debtor_payment_block(my_ref,"1082-invoice-dd", "Payment F2200", Decimal('1226.53'),
                                             "Sune's Sunny test deli", "som-bic", "Sunes iban account")


print document

