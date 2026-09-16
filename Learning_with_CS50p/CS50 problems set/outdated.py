months = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
}

def main():
    while True:
        try:
            date = input("Date: ")
            if "/" in date:
                transform_usa_to_europe(date)
            elif date[3].isalpha():
                transform_write_in_number(date)
            break
        except (ValueError, IndexError):
            continue
             

def transform_usa_to_europe(date):
    month, day, year = date.split("/")
    b = day.zfill(2)
    if 1 <= month <= 12 and 1 <= day <= 31:
        raise ValueError
    else:
        print(f"{year}-{month.zfill(2)}-{day.zfill(2)}".strip())

def transform_write_in_number(date):
    month, day, year = date.split(" ")
    day = day.replace(",","")
    if 1 <= month <= 12 and 1 <= day <= 31:
        raise ValueError
    if month in months:
            num_month = months[month]
            print(f"{year}-{num_month.zfill(2)}-{day.zfill(2)}".strip())
    else: raise ValueError
    
main()

