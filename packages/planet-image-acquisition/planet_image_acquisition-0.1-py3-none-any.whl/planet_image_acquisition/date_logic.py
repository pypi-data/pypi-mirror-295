def expand_dates(date):
    months = range(1, 13)
    if date < 2020:
        return [f'{date-1}-12_{date}-05', f'{date}-06_{date}-11']
    elif date == 2020:
        return [f'{date-1}-12_{date}-05'] +[f'{date}-06_{date}-08']+[f'{date}-{i:02}' for i in range(9, 13)]
    else:
        return [f'{date}-{i:02}' for i in months]

def create_dates(date_list):
    new_date_list = []
    for date in date_list:
        new_date_list.extend(expand_dates(date))
    return new_date_list




       