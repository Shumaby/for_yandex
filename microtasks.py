import pandas as pd
import datetime as dt
#
def calculate(filename):
    data = pd.read_csv(filename,sep='\t', engine='c')
    accessors_list = data.login.unique()
    result_list = []
    for i in range(len(accessors_list)):
        accessor_data_start = dict(data.query("login == @accessor_id").aggregate({'closed_ts':'min'}))
        accessor_data_end = dict(data.query("login == @accessor_id").aggregate({'closed_ts': 'max'}))
        #получаем количество рабочих дней каждого асессора путем вычитания конечной даты от начальной
        days = dt.datetime.strptime(accessor_data_end.get("closed_ts"), '%Y-%m-%d %H:%M:%S') - dt.datetime.strptime(accessor_data_start.get("closed_ts"), '%Y-%m-%d %H:%M:%S')
        microtasks = int(data.query("login == @accessor_id").aggregate({'Microtasks': 'sum'}))
        result_list.append([accessors_list[i],microtasks ,days.days+1, microtasks/(days.days+1)]) #добавляем list с данными для каждого асессора
    frame = pd.DataFrame(result_list, columns=['login', 'completed_tasks', 'job_days', 'day_avg'])  # собираем фрейм
    frame.to_csv("results2.csv", index=False)

def viewResults():
    data = pd.read_csv("results2.csv", sep=',', engine='c')
    print(data.describe())
    print(data.quantile(0.95))  # используем квантиль 95% дабы исключить явные выбросы. Итого имеем 288 микротасков в
    # среднем за день выполняется. Будем считать за 8 часов(рабочий день)
    #При условии оплаты N рублей за 30 секунд: 28 800 (секунд в рабочем дне) / 288 / 30 = 3.33
    # Справедливая цена одного микротаска: 3.33N
#calculate("data_task4_old.csv")
viewResults()