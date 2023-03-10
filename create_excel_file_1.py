import xlsxwriter
from openpyxl import load_workbook, Workbook

def writer_1 (function_name, name_page):
    
    book = xlsxwriter.Workbook(r"C:/Users/admin/Desktop/parser_tsn_base/prodaja_kvartiri.xlsx")
    page = book.add_worksheet(name_page)
            
    page.set_column("A:A", 40)
    page.set_column("B:B", 40)
    page.set_column("C:C", 40)
    page.set_column("D:D", 40)
    page.set_column("E:E", 40)
    page.set_column("F:F", 40)
    page.set_column("G:G", 40)
    page.set_column("H:H", 40)
    page.set_column("I:I", 40)
    page.set_column("J:J", 40)
    page.set_column("K:K", 40)
    page.set_column("L:L", 40)
    page.set_column("M:M", 40)
    page.set_column("N:N", 40)
    page.set_column("O:O", 40)
    page.set_column("P:P", 40)
    page.set_column("Q:Q", 40)

    row = 0 
    column = 0
    
    for item in function_name():
       page.write(row, column, item[0])
       page.write(row, column+1, item[1])
       page.write(row, column+2, item[2])
       page.write(row, column+3, item[3])
       page.write(row, column+4, item[4])
       page.write(row, column+5, item[5])
       page.write(row, column+6, item[6])
       page.write(row, column+7, item[7])
       page.write(row, column+8, item[8])
       page.write(row, column+9, item[9])
       page.write(row, column+10, item[10])
       page.write(row, column+11, item[11])
       page.write(row, column+12, item[12])
       page.write(row, column+13, item[13])
       page.write(row, column+14, item[14])
       page.write(row, column+15, item[15])
       page.write(row, column+16, item[16])
       row+=1

    book.close()