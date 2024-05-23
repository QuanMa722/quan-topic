# -*- coding: utf-8 -*-

from datetime import datetime
import re


class Process:

    def __init__(self):
        self.file_path = "./data/data.txt"

    def data_date(self):
        try:
            with open(file=self.file_path, mode="r", encoding="utf-8") as f1:
                comment_dict_list: list = f1.readlines()

                for item in comment_dict_list:
                    comment_time = datetime.strptime(eval(item)['评论时间'], '%Y-%m-%d %H:%M:%S')

                    if datetime(2024, 2, 2) <= comment_time < datetime(2024, 2, 13):
                        with open(file="./data/process-date.txt", mode="a", encoding="utf-8") as f2:
                            print(item)
                            f2.write(item)

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def data_clean():
        try:
            with open(file="./data/process-date.txt", mode="r", encoding="utf-8") as f1:
                comment_dict_list: list = f1.readlines()
                comment_dict_list = list(set(comment_dict_list))

                for item in comment_dict_list:
                    with open(file="./data/process-clean.txt", mode="a", encoding="utf-8") as f2:
                        print(item)
                        f2.write(item)

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def data_divide():
        try:
            with open(file="./data/process-clean.txt", mode="r", encoding="utf-8") as f1:
                comment_dict_list = f1.readlines()

                for item in comment_dict_list:
                    comment_dict = eval(item)
                    comment_time = datetime.strptime(comment_dict['评论时间'], '%Y-%m-%d %H:%M:%S')

                    for date in range(2, 13):
                        if datetime(2024, 2, date) <= comment_time < datetime(2024, 2, date + 1):
                            if "@" in comment_dict['评论内容']:
                                continue
                            else:
                                if "[" and "]" in comment_dict['评论内容']:

                                    pattern = r'^(.*?)(?=\[.*\])'
                                    result = re.match(pattern, comment_dict['评论内容'])
                                    comment_dict['评论内容'] = result.group(1)

                                    if comment_dict['评论内容']:
                                        with open(file=f"./data/process{date}.txt", mode="a", encoding="utf-8") as f2:
                                            print(comment_dict)
                                            f2.writelines(str(comment_dict) + "\n")

        except Exception as e:
            print(f"Error: {e}")

    @staticmethod
    def data_count():
        try:
            date_area_dict = {}

            with open(file="./data/process-clean.txt", mode="r", encoding="utf-8") as f1:
                comment_dict_list = f1.readlines()

            for date in range(2, 13):
                area_dict = {}

                for item in comment_dict_list:
                    comment_dict = eval(item)
                    comment_time = datetime.strptime(comment_dict['评论时间'], '%Y-%m-%d %H:%M:%S')

                    if datetime(2024, 2, date) <= comment_time < datetime(2024, 2, date + 1):
                        area = comment_dict['IP属地']
                        area_dict[area] = area_dict.get(area, 0) + 1

                date_area_dict[f"2024-02-{date}"] = area_dict

            for date, area_dict in date_area_dict.items():
                sorted_area_dict = dict(sorted(area_dict.items(), key=lambda x: x[1], reverse=True))

                sorted_data = dict(sorted(sorted_area_dict.items(), key=lambda items: items[1], reverse=True))

                top5 = {k: sorted_data[k] for k in list(sorted_data.keys())[:5]}
                total_top5 = sum(top5.values())
                result = {k: round(v / total_top5, 4) for k, v in top5.items()}

                with open(file=f"./data/process-count.txt", mode="a", encoding="utf-8") as f:
                    print(result)
                    f.write(str(result) + "\n")

        except Exception as e:
            print(f"Error: {e}")


process = Process()
process.data_date()
process.data_clean()
process.data_divide()
process.data_count()









