import xml.etree.ElementTree as ET
import datetime
import tempfile

def makeXml(mandate, msg_Id):
    Document = ET.Element('Document')
    MndtInitnReq = ET.SubElement(Document, 'MndtInitnReq')
    
    GrpHdr = ET.SubElement(MndtInitnReq, 'GrpHdr')
    MsgId = ET.SubElement(GrpHdr, 'MsgId') #Message Request ID
    CreDtTm = ET.SubElement(GrpHdr, 'CreDtTm') #some sort of time, at which mandate is created in the system?
    
    InstgAgt = ET.SubElement(GrpHdr, 'InstgAgt')
    FinInstnId1 = ET.SubElement(InstgAgt, 'FinInstnId')
    ClrSysMmbId1 = ET.SubElement(FinInstnId1, 'ClrSysMmbId')
    MmbId1 = ET.SubElement(ClrSysMmbId1, 'MmbId') #PUNB0HGB001
    Nm_creditor_bank_head = ET.SubElement(FinInstnId1, 'Nm') #SARVA HARYANA GRAMIN BANK
    
    InstdAgt = ET.SubElement(GrpHdr, 'InstdAgt')
    FinInstnId2 = ET.SubElement(InstdAgt, 'FinInstnId')
    ClrSysMmbId2 = ET.SubElement(FinInstnId2, 'ClrSysMmbId')
    MmbId2 = ET.SubElement(ClrSysMmbId2, 'MmbId') #DEBIT IFSC
    #Nm_debtor_bank_head = ET.SubElement(FinInstnId2, 'Nm') #DEBIT bank
    
    Mndt = ET.SubElement(MndtInitnReq, 'Mndt')
    MndtReqId = ET.SubElement(Mndt, 'MndtReqId') #Message Request ID
    
    Tp = ET.SubElement(Mndt, 'Tp')
    SvcLvl = ET.SubElement(Tp, 'SvcLvl')
    Prtry_S = ET.SubElement(SvcLvl, 'Prtry') #L001
    LclInstrm = ET.SubElement(Tp, 'LclInstrm')
    Prtry_L = ET.SubElement(LclInstrm, 'Prtry') #DEBIT
    
    Ocrncs = ET.SubElement(Mndt, 'Ocrncs')
    SeqTp = ET.SubElement(Ocrncs, 'SeqTp') #RCUR
    Frqcy = ET.SubElement(Ocrncs, 'Frqcy') #MNTH
    Drtn = ET.SubElement(Ocrncs, 'Drtn')
    FrDt = ET.SubElement(Drtn, 'FrDt') #date of mandate
    
    FrstColltnDt = ET.SubElement(Ocrncs, 'FrstColltnDt') #from date
    FnlColltnDt = ET.SubElement(Ocrncs, 'FnlColltnDt') #to date
    
    ColltnAmt = ET.SubElement(Mndt, 'ColltnAmt') #mandate amount
    
    Cdtr = ET.SubElement(Mndt, 'Cdtr')
    Nm_creditor_customer = ET.SubElement(Cdtr, 'Nm') #creditor name
    
    CdtrAcct = ET.SubElement(Mndt, 'CdtrAcct')
    Id_1_creditor = ET.SubElement(CdtrAcct, 'Id')
    Othr = ET.SubElement(Id_1_creditor, 'Othr')
    Id_2_creditor = ET.SubElement(Othr, 'Id') #Utility Code HGBX00002000017848
    
    CdtrAgt = ET.SubElement(Mndt, 'CdtrAgt')
    FinInstnId_creditor = ET.SubElement(CdtrAgt, 'FinInstnId')
    ClrSysMmbId_creditor = ET.SubElement(FinInstnId_creditor, 'ClrSysMmbId')
    MmbId_creditor = ET.SubElement(ClrSysMmbId_creditor, 'MmbId') #PUNB0HGB001
    Nm_creditor_bank = ET.SubElement(FinInstnId_creditor, 'Nm') #SARVA HARYANA GRAMIN BANK
    
    Dbtr = ET.SubElement(Mndt, 'Dbtr')
    Nm_debtor_customer = ET.SubElement(Dbtr, 'Nm')
    #CtctDtls = ET.SubElement(Dbtr, 'CtctDtls')
    #MobNb = ET.SubElement(CtctDtls, 'MobNb')
    
    DbtrAcct = ET.SubElement(Mndt, 'DbtrAcct')
    Id_1_debtor = ET.SubElement(DbtrAcct, 'Id')
    Othr_debtor = ET.SubElement(Id_1_debtor, 'Othr')
    Id_2_debtor = ET.SubElement(Othr_debtor, 'Id') #Account number debtor
    
    Tp_debtor = ET.SubElement(DbtrAcct, 'Tp')
    Prtry_debtor = ET.SubElement(Tp_debtor, 'Prtry') #Account type debtor
    
    DbtrAgt = ET.SubElement(Mndt, 'DbtrAgt')
    FinInstnId_debtor = ET.SubElement(DbtrAgt, 'FinInstnId')
    ClrSysMmbId_debtor = ET.SubElement(FinInstnId_debtor, 'ClrSysMmbId')
    MmbId_debtor = ET.SubElement(ClrSysMmbId_debtor, 'MmbId') #debtor IFSC
    #Nm_debtor_bank = ET.SubElement(FinInstnId_debtor, 'Nm') #debtor bank NAME
    
    Document.set('xmlns', 'urn:iso:std:iso:20022:tech:xsd:pain.009.001.01')
    tree = t = ET.ElementTree(Document) #tree is created
    
    #hard coded values
    MmbId1.text = 'PUNB0HGB001'
    Nm_creditor_bank_head.text = 'SARVA HARYANA GRAMIN BANK'
    MmbId_creditor.text = 'PUNB0HGB001'
    Nm_creditor_bank.text = 'SARVA HARYANA GRAMIN BANK'
    Prtry_L.text = 'DEBIT'
    Id_2_creditor.text = 'HGBX00002000017848'
    SeqTp.text = 'RCUR'
    ColltnAmt.set('Ccy', 'INR')
    Nm_creditor_customer.text = 'SARVA HARYANA GRAMIN BANK'
    
    #variables
    MsgId.text = msg_Id
    MndtReqId.text = mandate.ref
    CreDtTm.text = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30))).replace(microsecond=0).isoformat() #system time in ISO format
    ColltnAmt.text = str(mandate.amount)
    FrDt.text = mandate.date.isoformat()
    FrstColltnDt.text = mandate.start_date.isoformat()
    FnlColltnDt.text = mandate.end_date.isoformat()
    Nm_debtor_customer.text = mandate.complete_name[:40]
    Id_2_debtor.text = mandate.debtor_acc_no
    Prtry_debtor.text = str(mandate.debtor_acc_type)
    MmbId_debtor.text = MmbId2.text = mandate.debtor_acc_ifsc
    Prtry_S.text = mandate.category
    Frqcy.text = mandate.frequency
    
    #indent and save the file
    ET.indent(tree, space='\t')
    outfile = tempfile.TemporaryFile()
    tree.write(outfile, encoding='UTF-8', xml_declaration=True)
    outfile.seek(0)
    return outfile
