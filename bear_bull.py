import numpy as np
import pandas as pd
import energy_indicator as ei
import csv

lookback = 2
initial_money = 1000000.0
total_money = 0
taxe = 0.0005
alpha_val = 2
# input_list = ['ETHUSDT-5m-2022-08', 'ETHUSDT-5m-2022-09', 'ETHUSDT-5m-2022-10', 'ETHUSDT-5m-2022-11',
#               'ETHUSDT-5m-2022-12', 'ETHUSDT-5m-2023-01',']
# 'ETHUSDT-1d-2022-08', 'ETHUSDT-1d-2022-09', 'ETHUSDT-1d-2022-10', 'ETHUSDT-1d-2022-11',
# 'ETHUSDT-1d-2022-12', 'ETHUSDT-1d-2023-01'

input_list = ['ETHUSDT-1h-2022-08', 'ETHUSDT-1h-2022-09', 'ETHUSDT-1h-2022-10', 'ETHUSDT-1h-2022-11',
              'ETHUSDT-1h-2022-12', 'ETHUSDT-1h-2023-01']

# input_list = ['ETHUSDT-1h-2022-10']

for files in input_list:
    money = initial_money
    coins = 0
    file_path = f'.\Binance_data\{files}\{files}.csv'
    with open(file_path) as csv_file:
        my_data = np.genfromtxt(file_path, delimiter=',')

    # bull_bear_power(data, lookback, high, low, close, where):
    # Open time	Open	High	Low	Close	Volume	Close time
    # Quote asset volume	Number of trades
    # Taker buy base asset volume	Taker buy quote asset volume	Ignore
    # data_len = my_data
    data1 = ei.bull_bear_power(my_data[:, 0:6], alpha_val, lookback, 2, 3, 4, 6)
    data1[:, 8] = data1[:, 6] - data1[:, 7]

    data1 = ei.adder(data1, 2)
    i_s = 0
    rise_cases = 0
    fall_cases = 0
    bull_cases = 0
    bear_cases = 0
    for i in range(len(data1) - 1):
        if data1[i, 7] < 5:
            bull_cases += 1
            money = money - (1 + taxe) * data1[i, 4]
            # money = money - (1 + taxe) * (data1[i, 1] + data1[i, 4]) / 2
            coins += 1
        if data1[i, 7] > 5:
            money = money + (1 - taxe) * data1[i, 4]
            # money = money + (1 - taxe) * (data1[i, 1] + data1[i, 4]) / 2
            coins -= 1
        # print(f'money = {money}, coins={coins}')
        data1[i, 9] = money
        data1[i, 10] = coins
    data1[i, 9] = money + (1 - taxe) * coins * (data1[i, 4] + data1[i, 1]) / 2
    data1[i, 10] = 0
    total_money += money + (1 - taxe) * coins * (data1[i, 4] + data1[i, 1]) / 2

    print(f'{files}, total = {i} bull_c={bull_cases}')

    # print(f'money = {money + (1-taxe)*coins * (data1[i, 1] + data1[i, 4]) / 2}, coins={0}')
    print(f'money = {money + (1 - taxe) * coins * (data1[i, 3])}, coins={coins}')
    # ei.indicator_plot_double_bull_bear(data1)
    headerlist = ['Open time', 'Open', 'High', 'Low', 'Close', 'Volume',
                  'Bull power', 'Bear power', '-----', 'Money', 'Coins']

    file_path_out = f'.\Binance_data\{files}\{files}_out.csv'
    with open(file_path_out, 'w') as csv_file_out:

        csvwriter = csv.writer(csv_file_out, delimiter=',')
        csvwriter.writerow(headerlist)
        csv_file_out.write("\n")

        np.savetxt(csv_file_out, data1, delimiter=',')
        # np.savetxt(file_path_out, 'a',  header=headerlist, delimiter=",")
        # np.savetxt(file_path_out, data1, delimiter=",")
        # np.savetxt(file_path_out, data1, delimiter=",", header=headerlist)
        # converting data frame to csv
        # csv_file_out.to_csv(file_path_out, header=header, index=False)
        # dw = csv.DictWriter(csv_file_out, delimiter=',', fieldnames=headerlist)
        # dw.writeheader()

        # with open("test.txt", "ab") as f:
        #     numpy.savetxt(f, a)
        csv_file_out.close()
print(f'AVG Total money ={total_money / len(input_list)}')
