def make_accrual_interest_entry_for_term_loans(posting_date, process_loan_interest, term_loan=None, loan_type=None, accrual_type='Regular'):
    curr_date = posting_date or add_days(nowdate(), 1)
    term_loans = get_term_loans(curr_date, term_loan, loan_type)
    accrued_entries = []
    for loan in term_loans:
        accrued_entries.append(loan.payment_entry)
        args = frappe._dict({'loan': loan.name, 'applicant_type': loan.applicant_type, 'applicant': loan.applicant, 'interest_income_account': loan.interest_income_account, 'loan_account': loan.loan_account, 'interest_amount': loan.interest_amount, 'payable_principal': loan.principal_amount, 'process_loan_interest': process_loan_interest, 'repayment_schedule_name': loan.payment_entry, 'posting_date': posting_date, 'accrual_type': accrual_type})
        make_loan_interest_accrual_entry(args)
    if accrued_entries:
        frappe.db.sql(
            'UPDATE `tabRepayment Schedule`\n\t\t\tSET is_accrued = 1 where name in (%s)' % ', '.join(['%s'] * len(accrued_entries)), tuple(accrued_entries))