import datetime
from decimal import Decimal
from lxml import etree
from uuid import uuid1 as uuid

__author__ = 'sune'


class Document:
    xmlns = "urn:iso:std:iso:20022:tech:xsd:pain.001.001.03"
    xsi = "http://www.w3.org/2001/XMLSchema-instance"
    oin = ""
    reference = ""
    transaction_information_blocks = {}

    def __init__(self, oin, reference):
        self.reference = reference
        self.root = etree.Element("{%s}Document" % self.xmlns, nsmap={'xsi': self.xsi, None: self.xmlns})
        cstmr_trx_info = etree.SubElement(self.root, "CstmrCdtTrfInitn")
        group_header = etree.SubElement(cstmr_trx_info, "GrpHdr")
        msg_id = etree.SubElement(group_header, "MsgId")
        msg_id.text = reference
        crt_tm = etree.SubElement(group_header, "CreDtTm")
        crt_tm.text = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        no_of_tx = etree.SubElement(group_header, "NbOfTxs")
        control_sum = etree.SubElement(group_header, "CtrlSum")
        initgPty = etree.SubElement(group_header, "InitgPty")
        id = etree.SubElement(initgPty, "Id")
        org_id = etree.SubElement(id, "OrgId")
        othr = etree.SubElement(org_id, "Othr")
        i_p_o_id = etree.SubElement(othr, "Id")
        i_p_o_id.text = oin

        self.group_header = group_header


    def add_debtor_payment_block(self, debtor_name, debtor_account, debtor_agent_bic="AIBKIE2D",
                   payment_date=datetime.date.today):
        reference = str(uuid())[:35]

        pmt_inf_block = etree.SubElement(self.root[0], "PmtInf")
        payment_id = etree.SubElement(pmt_inf_block, "PmtInfId")
        payment_id.text = reference
        method = etree.SubElement(pmt_inf_block, "PmtMtd")
        method.text = "TRF" # Must always be this value
        blck_no_tx = etree.SubElement(pmt_inf_block, "NbOfTxs")
        blck_ctrl_sum = etree.SubElement(pmt_inf_block, "CtrlSum")
        pmt_date = etree.SubElement(pmt_inf_block, "ReqdExctnDt")
        pmt_date.text = payment_date.strftime("%Y-%m-%d")
        dbt = etree.SubElement(pmt_inf_block, "Dbtr")
        dbt_name = etree.SubElement(dbt, "Nm")
        dbt_name.text = debtor_name
        dbt_acct = etree.SubElement(pmt_inf_block, "DbtrAcct")
        dbt_acct_id = etree.SubElement(dbt_acct, "Id")
        dbt_iban = etree.SubElement(dbt_acct_id, "IBAN")
        dbt_iban.text = debtor_account.replace(" ", "")
        dbt_acct_ccy = etree.SubElement(dbt_acct, "Ccy")
        dbt_acct_ccy.text = "EUR" # Must be Euro
        dbt_agt = etree.SubElement(pmt_inf_block, "DbtrAgt")
        fin_inst_id = etree.SubElement(dbt_agt, "FinInstnId")
        bic = etree.SubElement(fin_inst_id, "BIC")
        bic.text = debtor_agent_bic

        self.transaction_information_blocks[reference] = pmt_inf_block

        return reference

    def add_payment_to_debtor_payment_block(self,
                                            debtor_payment_block_reference,
                                            instruction_id,
                                            description,
                                            amount,
                                            creditor_name,
                                            creditor_bic,
                                            creditor_account):
        if " " in instruction_id:
            raise ValueError("instruction_id cannot contain spaces")
        if len(instruction_id) > 35:
            raise ValueError("instruction_id cannot be longer than 35 characters")
        if len(description) > 35:
            raise ValueError("description cannot be longer than 35 characters")
        if isinstance(amount, Decimal):
            if amount.as_tuple().exponent != -2:
                raise ValueError("amount must have exactly two decimal places")
        else:
            raise ValueError("amount must be a Decimal and have exactly two decimal places")
        if len(creditor_bic) > 11:
            raise ValueError("creditor_bic cannot be more than 11 characters long")
        if len(creditor_name) > 70:
            raise ValueError("creditor_name cannot be more than 70 characters long")
        if len(creditor_account) > 34:
            raise ValueError("creditor_account cannot be more than 34 characters long")

        pmt_inf_block = self.transaction_information_blocks[debtor_payment_block_reference]
        tx_inf_blck = etree.SubElement(pmt_inf_block, "CdtTrfTxInf")
        pmt_id = etree.SubElement(tx_inf_blck, "PmtId")
        inst_id = etree.SubElement(pmt_id, "InstrId")
        inst_id.text = instruction_id
        e_to_e_id = etree.SubElement(pmt_id, "EndToEndId")
        e_to_e_id.text = description


        amt = etree.SubElement(tx_inf_blck, "Amt")
        ins_amt = etree.SubElement(amt, "InstdAmt", Ccy="EUR") #Currently only supporting euro
        ins_amt.text = str(amount)

        cdr_agt = etree.SubElement(tx_inf_blck, "CdtrAgt")
        fin_inst_id = etree.SubElement(cdr_agt, "FinInstnId")
        bic = etree.SubElement(fin_inst_id, "BIC")
        bic.text = creditor_bic

        cdtr = etree.SubElement(tx_inf_blck, "Cdtr")
        name = etree.SubElement(cdtr, "Nm")
        name.text = creditor_name

        cdtr_acct = etree.SubElement(tx_inf_blck, "CdtrAcct")
        acct_id = etree.SubElement(cdtr_acct, "Id")
        iban = etree.SubElement(acct_id, "IBAN")
        iban.text = creditor_account

        nb_of_txs = tx_inf_blck.find("../NbOfTxs")
        ctrl_amt = tx_inf_blck.find("../CtrlSum")

        all_amounts = pmt_inf_block.findall(".//InstdAmt")
        if not isinstance(all_amounts, list):
            all_amounts = list(all_amounts)

        nb_of_txs.text = str(len(all_amounts))

        ctrl_amt.text = str(sum([Decimal(elem.text) for elem in all_amounts]))

        self._update_totals()


    def _update_totals(self):
        nb_of_txs = self.group_header.find("./NbOfTxs")
        ctrl_sum = self.group_header.find("./CtrlSum")
        all_nb_of_txs = self.root.findall(".//PmtInf//NbOfTxs")
        all_ctrl_amounts = self.root.findall(".//PmtInf//CtrlSum")

        nb_of_txs.text = str(sum([int(elem.text) for elem in all_nb_of_txs]))
        ctrl_sum.text = str(sum([Decimal(elem.text) for elem in all_ctrl_amounts]))




    def __str__(self):
        return etree.tostring(self.root, pretty_print=True, xml_declaration=True, encoding="utf-8")



class SepaFormatException(Exception):
    pass

