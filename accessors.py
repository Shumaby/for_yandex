import pandas as pd
def calculateCorrectRate():
    data = pd.read_csv("data_task3.csv",delim_whitespace=True)
    resultList = []
    accessors_list = sorted(data.uid.unique()) #сортируем для будущего корректного соотношения результата и индекса листа равного id ассесора
    for i in range(len(accessors_list)): #проходим по всему списку ассесоров
        accessor = accessors_list[i]
        resultList.append(               #добавляем в лист процентное соотношение верных оценок
            len(data.query("(uid == @accessor) and ((jud == 0 and cjud == 0) or (jud == 1 and cjud == 1))")) / len(
                data.query("(uid == @accessor)")))
    frame = pd.DataFrame(resultList, columns=['result'])  # собираем фрейм
    frame.to_csv("results.csv", index=False)              #сохраняем в файл

def viewResults():
    results = pd.read_csv("results.csv", delim_whitespace=True)
    print(results.sort_values('result')) #выводим результаты с сортировкой от худших к лучшим

calculateCorrectRate()
viewResults()





