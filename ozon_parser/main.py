#import ozon_parser.sheets as sheets
import ozon_parser.parser as parser


def main():
    """
    creds = sheets.connect()

    service = sheets.build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()


    response = sheets.get_range(sheet, "Лист1", "A1:B1")
    print(response["values"])

    response = sheets.batch_update(sheet, "Лист1", "A2:B2", [["Привет", "Мир"]])
    print(response)
    """
    parser.main()

if __name__ == "__main__":
    main()