# The purpose of this file is to generalise the creation of standard account values from the strategy

def create_standard_account_values(transaction_df, initial_cash):
    '''

    :return: A pandas dataframe with Cash and portfolio values
    '''
    # Check for required inputs, Close and Transaction
    cols = transaction_df.columns
    if 'Close' not in cols:
        raise Exception('A Close value is required to calculate account values')
    if 'Transaction' not in cols:
        raise Exception('A Transaction value is required to calculate account values')

    # Initialise Required Columns
    transaction_df['Cash'] = 0
    transaction_df['Share Value'] = 0
    transaction_df['Number of Shares Owned'] = 0

    # Get index location of each column as needed
    cash_index = transaction_df.columns.get_loc('Cash')
    transaction_index = transaction_df.columns.get_loc('Transaction')
    close_index = transaction_df.columns.get_loc('Close')

    # Calculate Number of Shares Owned
    transaction_df['Number of Shares Owned'] = transaction_df['Transaction'].cumsum()

    # Calculate amount of Cash in portfolio, assume close price is what we get
    transaction_df.iloc[0, cash_index] = initial_cash
    transaction_df.iloc[1:, cash_index] = -1 * transaction_df.iloc[1:,transaction_index] * transaction_df.iloc[1:,close_index]
    transaction_df['Cash'] = transaction_df['Cash'].cumsum()

    # Calculate Share Value
    transaction_df['Share Value'] = transaction_df['Number of Shares Owned'] * transaction_df['Close']

    # Calculate Portfolio Value
    transaction_df['Portfolio Value'] = transaction_df['Cash'] + transaction_df['Share Value']

    return transaction_df