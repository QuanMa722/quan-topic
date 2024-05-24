# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


data = {
    '2024-02-02': {'湖北': 0.7804, '广东': 0.0722, '河南': 0.0647, '湖南': 0.048, '江苏': 0.0347},
    '2024-02-03': {'湖北': 0.7393, '广东': 0.0837, '河南': 0.0691, '湖南': 0.0594, '江苏': 0.0485},
    '2024-02-04': {'湖北': 0.6413, '湖南': 0.1244, '广东': 0.0985, '河南': 0.0859, '江苏': 0.0499},
    '2024-02-05': {'湖北': 0.4561, '广东': 0.1582, '河南': 0.151, '湖南': 0.1384, '江苏': 0.0963},
    '2024-02-06': {'湖北': 0.5013, '河南': 0.1436, '湖南': 0.1377, '广东': 0.1259, '江苏': 0.0914},
    '2024-02-07': {'湖北': 0.3029, '河南': 0.2016, '广东': 0.1903, '江苏': 0.1544, '山东': 0.1507},
    '2024-02-08': {'湖北': 0.3136, '河南': 0.2253, '山东': 0.1749, '江苏': 0.1482, '广东': 0.138},
    '2024-02-09': {'湖北': 0.315, '河南': 0.2348, '山东': 0.1797, '广东': 0.1425, '江苏': 0.1281},
    '2024-02-10': {'湖北': 0.435, '河南': 0.1949, '广东': 0.142, '山东': 0.1239, '江苏': 0.1042},
    '2024-02-11': {'湖北': 0.2865, '河南': 0.2125, '山东': 0.1813, '广东': 0.1735, '湖南': 0.1462},
    '2024-02-12': {'湖北': 0.3918, '广东': 0.2268, '山东': 0.1409, '河南': 0.1237, '广西': 0.1168}
}

dates = list(data.keys())
provinces = ['湖北', '广东', '河南', '湖南', '江苏', '山东', '广西']
all_data = np.zeros((len(dates), len(provinces)))

for i, date in enumerate(dates):
    date_data = data[date]
    for j, province in enumerate(provinces):
        all_data[i, j] = date_data.get(province, 0)

col_sum = np.sum(all_data, axis=1, keepdims=True)

percentages = all_data / col_sum * 100


fig, ax = plt.subplots(figsize=(10, 8))

bottom = np.zeros(len(dates))
for i, province in enumerate(provinces):
    color = plt.cm.viridis(i / len(provinces))
    ax.bar(dates, percentages[:, i], width=0.4, bottom=bottom, label=province, color=color)
    bottom += percentages[:, i]


hubei_index = provinces.index('湖北')
ax.plot(dates, percentages[:, hubei_index], color='red', marker='o')

ax.set_xlabel('日期')
ax.set_ylabel('百分比 (%)')
ax.set_title('各省份随时间的百分比分布')
ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
