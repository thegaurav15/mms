for p in Presentation.objects.filter(npci_status='Active').filter(mandate__debit_date='11'):
    
    list = (
        p.npci_umrn,
        p.mandate.start_date.isoformat(),
        p.mandate.start_date.isoformat(),
        p.mandate.end_date.isoformat(),
        p.mandate.debtor_name,
        p.mandate.debtor_bank.name,
        p.mandate.debtor_acc_no,
        p.mandate.debtor_acc_ifsc,
        p.mandate.credit_account,
        str(p.mandate.amount.str),
        p.mandate.ref
    )
    
    print('|'.join(list))