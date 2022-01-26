import io
import json
import time
import openpyxl as xl

machine = 'v0.1'

fp = 'D:\\My Drive\\3D Printer\\Mainsail\\Jobs History\\' + machine + '.json'
log = 'D:\\My Drive\\3D Printer\\Mainsail\\Jobs History\\history.xlsx'

with open(fp) as f:
    data = json.load(f)

with open(log, 'rb') as f:
    in_mem_file = io.BytesIO(f.read())

wb = xl.load_workbook(in_mem_file)
ws = wb[machine]

for i in data['result']['jobs']:
    if (int(time.strftime('%H', time.gmtime(i['print_duration']))) == 0) and (int(time.strftime('%M', time.gmtime(i['print_duration']))) < 10):
        pass
    else:
        ws.cell(column=1, row=ws.max_row+1, value=i['status'])
        ws.cell(column=2, row=ws.max_row, value=time.strftime('%d.%m.%Y', time.strptime(time.ctime(i['start_time']))))
        ws.cell(column=3, row=ws.max_row, value=int(time.strftime('%H', time.gmtime(i['print_duration']))))
        ws.cell(column=4, row=ws.max_row, value=int(time.strftime('%M', time.gmtime(i['print_duration']))))
        ws.cell(column=5, row=ws.max_row, value=i['filename'])


wb.save(log)
wb.close()



