from pprint import pprint
import csv
import re


def change_full_name_and_phone(cont_list: list):
    """
    Разбиение ФИО по соответствующим столбцам и приведение телефона к нужному формату
    :param cont_list: list
    :return: None
    """
    pattern = r"(\+7|8)[^\w]*(\d{3})[^\w]*(\d{3})[^\w]*(\d{2})[^\w]*(\d*)[ (]*(доб\.)*\s*(\d*)\)*"
    substitution = r"+7(\2)\3-\4-\5 \6\7"

    for contact in cont_list[1:]:
        phone = contact[-2]
        contact[-2] = re.sub(pattern, substitution, phone).strip()
        full_name_list = ' '.join(contact[:3]).strip().split()
        if len(full_name_list) == 3:
            contact[0], contact[1], contact[2] = full_name_list
        else:
            contact[0], contact[1] = full_name_list


def join_duplicates(cont_list: list):
    """
    Объединение дублирующихся записей
    :param cont_list: list
    :return: None
    """
    idx_list = []
    for i in range(1, len(cont_list) - 1):
        for j in range(i + 1, len(cont_list)):
            if (cont_list[i][0], cont_list[i][1]) == (cont_list[j][0], cont_list[j][1]):
                for k in range(len(cont_list[i])):
                    if not cont_list[i][k]:
                        cont_list[i][k] = cont_list[j][k]
                idx_list.append(j)

    for idx in idx_list[::-1]:
        cont_list.pop(idx)


if __name__ == "__main__":
    # читаем адресную книгу в формате CSV в список contacts_list
    with open("phonebook_raw.csv", encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)

    change_full_name_and_phone(contacts_list)
    join_duplicates(contacts_list)

    # код для записи файла в формате CSV
    with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(contacts_list)

    pprint(contacts_list)
