
header = 'Date,Open,High,Low,Close,Adj Close,Volume\n'
files = {}
pair_list = ['43350', '82651',
            '44644', '90458',
            '24969', '24985',
            '42585', '83621',
            '60186', '81095',
            '16548', '81577',
             '83186', '89003',
             '81294', '82581',
             '53640', '83597',
             '43350', '82651',
             '12781', '48531',
             '44644', '90458',
             '21742', '76639',
             '51633', '58819',
             '81294', '83186',
             '42585', '83621',
             '10395', '53640',
             '23931', '48531',
             '60186', '81095',
             '13856', '48531']


with open('tetsing_data.csv', 'r') as fb:
    lines = fb.readlines()
    for line in  lines:
        data = line.split(',')
        try:
            permno = data[1]
            if len(data) >= 13 and permno in pair_list:
                if permno in files:
                    fd = files[permno]
                else:
                    fd = open('data/{}.csv'.format(permno), 'w')
                    files[permno] = fd
                    fd.write(header)
                date     = '{}/{}/{}'.format(data[2][:4], data[2][4:6], data[2][6:8])
                price    = data[6]
                dataLine = '{},{},{},{},{},{},{}\n'.format(date, price, price,
                                                           price,
                                                           price, price, data[7]
                                                           )
                print(line)
                print(dataLine)
                fd.write(dataLine)
        except Exception as e:
            pass
        line = fb.readline()
