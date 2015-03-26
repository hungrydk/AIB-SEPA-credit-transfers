# AIB-SEPA-credit-transfers
Small python library with the purpose of creating SEPA Credit Transfer files specifically for AIB (Allied Irish Banks)

## Warning
This is work in progress. Output has not yet been validated.

##Usage
Initialize a new payment document

```
document = Document(OIN, reference)
```

* OIN - (str) Originator identification number, supplied by AIB
* reference - (str) you reference for the payment document.

Add a payment information block

```
payment_block_ref = document.add_debtor_payment_block(debtor_name, debtor_account, debtor_agent_bic="AIBKIE2D",
                   payment_date=datetime.date.today())
```

* debtor_name - (str) The business name of the debtor
* debtor_account - (str) The IBAN account of the debtor
* debtor_agent_bic - (str) The BIC of the debtors bank. defaults to AIB's bic
* payment_date - (date) The intended payment date. 

Returns a uuid str which references the payment block within the payment document

```
document.add_payment_to_debtor_payment_block(debtor_payment_block_reference,
                                             instruction_id,
                                             description,
                                             amount,
                                             creditor_name,
                                             creditor_bic,
                                             creditor_account)
```

* debtor_payment_block_reference - (str) The reference returned from add_debtor_payment_block()
* instruction_id - (str) your reference id for the payment. Cannot contain whitespaces.
* description - (str) The payment id sent to the receiving bank
* amount - (Decimal) The amount to pay to the creditor
* creditor_name - (str) Must be accurate
* creditor_bic - (str) The BIC of the receiving bank
* creditor_account - (str) The creditors IBAN account

##References
Based on the AIB's specification found [here](http://business.aib.ie/content/dam/aib/business/docs/products/payments/AIB%20SEPA%20Credit%20Transfers%20XML%20File%20Specification.pdf)

##Dependencies
Depends on lxml, www.lxml.de (pip install lxml)
