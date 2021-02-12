import xlsxwriter


def getReport(ticker_dict):
    print('writing report')
    workbook = xlsxwriter.Workbook('./xlsxwrite/report.xlsx')
    worksheet = workbook.add_worksheet('ticker_reports')

    row = 1
    col = 1

    red_format = workbook.add_format({
        'font_color': 'red',
        'bold': 1,
    })

    # formatting
    ticker_format = workbook.add_format({'font_color': 'red', 'font_size': 15, 'align': 'center', 'bg_color': '#55CDEA', 'border': 1, 'border_color': 'black'})
    news_format = workbook.add_format()
    news_format.set_text_wrap()
    worksheet.set_zoom(150)

    # writing to the excel workbook
    for ticker, values in ticker_dict.items():
        worksheet.write(row, col, ticker, ticker_format)
        worksheet.set_column(col, col,  30)
        for news, link in values.items():
            row += 1
            worksheet.write_url(row, col, link, news_format, string=news)
        col += 1
        row = 1

    workbook.close()


if __name__ == "__main__":
    test_dict= {'INTC': {'news': 'https://xlsxwriter.readthedocs.io/example_hyperlink.html', 'news2': 'https://www.excel-easy.com/examples/line-break.html'}, 'AAPL': {'news': 'link', 'news': 'link'}}
    getReport(test_dict)