from datetime import datetime, date
from .models import *

def to_midnight(d):
    return datetime(d.year, d.month, d.day)

def zip_object_factory(npci_username):
    try:
        seq = Zip.objects.filter(date__gte=date.today()).latest("seq_no").seq_no + 1
    except Zip.DoesNotExist:
        seq = 1

    filename = 'MMS-CREATE-HGBX-' + npci_username + '-' + date.today().strftime(r'%d%m%Y') + '-' + str(seq).zfill(6) + '-INP.zip'

    zip_obj = Zip(
        date = date.today(),
        seq_no = seq,
        npci_username = npci_username,
        filename = filename
    )

    zip_obj.save()

    return zip_obj

def presentation_object_factory(npci_username):
    try:
        seq = Presentation.objects.filter(date__gte=date.today()).latest("seq_no").seq_no + 1
    except Presentation.DoesNotExist:
        seq = 1

    filename_prefix = 'MMS-CREATE-HGBX-' + npci_username + '-' + date.today().strftime(r'%d%m%Y') + '-' + str(seq).zfill(6)

    npci_MsgId = 'HGBX' + date.today().strftime(r'%d%m%Y') + str(seq).zfill(6)

    presentation_obj = Presentation(
        date = date.today(),
        seq_no = seq,
        npci_username = npci_username,
        npci_MsgId = npci_MsgId,
        filename_prefix = filename_prefix
    )

    return presentation_obj

def process_ack(file):
    print('Processing NPCI ACK File inside function', file['filename'])
    try:
        p = Presentation.objects.get(npci_MsgId = file['OriginalMsgId'])
    except Presentation.DoesNotExist:
        print('Not found', file['OriginalMsgId'])
        return

    # print(p.mandate.date == file['Dt'])
    # print(p.mandate.start_date == file['FrstColltnDt'])
    # print(p.mandate.end_date == file['FnlColltnDt'])
    # print(p.mandate.amount == file['Amt'])
    # print(p.mandate.debtor_name == file['DbtrName'])
    # print(p.mandate.debtor_acc_no == file['DbtrAcct'])
    # print(p.mandate.debtor_acc_type == file['DbtrAcctType'])
    # print(p.mandate.debtor_acc_ifsc == file['DbtrAcctIFSC'])

    if p.npci_upload_time:
        print('already updated')
        return
    p.npci_upload_time = file['AcqCreDtTm']
    if file['Accptd'] == 'true':
        p.npci_umrn = file['UMRN']
        print('UMRN updated', file['UMRN'])
    elif file['Accptd'] == 'false':
        p.npci_upload_error = file['Error']
        print('Error updated', file['Error'])
    else:
        print('Accpd other than true/false')
    p.save()
    print('Presentation object saved.')