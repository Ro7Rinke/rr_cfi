tables = {
    category: {
        title: 'text',
        description: 'text',
        color: 'text'
    },
    tag: {
        user_id: user.id,
        title: 'text',
        description: 'text',
        color: 'text'
    },
    transactionTypr: {
        title: 'text',
        is_debit: 'bool',
        reference: 'text',
        is_paid: 'bool'
    },
    entry: {
        title: 'text',
        description: 'text',
        date: 'datetime',
        is_periodic: 'bool',
        total_value: 'float',
        total_installments: 'int',
        transaction_type_id: transactionType.id,
        category_id: category.id
    },
    entryTag: {
        entry_id: entry.id,
        tag_id: tag.id
    },
    periodicType: {
        title: 'text',
        reference: 'text',
        value: 'int'
    },
    periodicEntry: {
        entry_id: entry.id,
        start_date: 'datetime',
        end_date: 'datetime',
        reference_day: 'int',
        reference_month: 'int',
        reference_year: 'int'
    },
    installment: {
        entry_id: entry.id,
        value: 'float',
        reference_date: 'datetime',
        installment_number: 'int'
    }
}
