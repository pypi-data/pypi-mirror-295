__all__ = ['my_table_db', 'my_table_db_full', 'my_table_db_name', 'my_table_db_full_name']


def get_rows(rows, num, control_num):
    return rows[control_num][num]


def my_table_db_name(rows, name_arg1=None, arg1=None, name_arg2=None, arg2=None, name_arg3=None, arg3=None,
                     name_arg4=None,
                     arg4=None, name_arg5=None, arg5=None, name_arg6=None, arg6=None, name_arg7=None, arg7=None):
    max_lengths = [0] * len(rows[0])

    for row in rows:
        for index, item in enumerate(row):
            item_length = len(str(item)) if item is not None else 0
            if item_length > max_lengths[index]:
                max_lengths[index] = item_length

    if (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5 and name_arg6 and name_arg7) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{max_lengths[0]}}{'    | '}{name_arg2}:    {str(arg2):{max_lengths[1]}}{'    | '}{name_arg3}:    {str(arg3):{max_lengths[2]}}{'    | '}{name_arg4}:    {str(arg4):{max_lengths[3]}}{'    | '}{name_arg5}:    {str(arg5):{max_lengths[4]}}{'    | '}{name_arg6}:    {str(arg6):{max_lengths[5]}}{'    | '}{name_arg7}:    {str(arg7):{max_lengths[6]}}")

    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5 and name_arg6) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{max_lengths[0]}}{'    | '}{name_arg2}:    {str(arg2):{max_lengths[1]}}{'    | '}{name_arg3}:    {str(arg3):{max_lengths[2]}}{'    | '}{name_arg4}:    {str(arg4):{max_lengths[3]}}{'    | '}{name_arg5}:    {str(arg5):{max_lengths[4]}}{'    | '}{name_arg6}:    {str(arg6):{max_lengths[5]}}")

    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{max_lengths[0]}}{'    | '}{name_arg2}:    {str(arg2):{max_lengths[1]}}{'    | '}{name_arg3}:    {str(arg3):{max_lengths[2]}}{'    | '}{name_arg4}:    {str(arg4):{max_lengths[3]}}{'    | '}{name_arg5}:    {str(arg5):{max_lengths[4]}}")

    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{max_lengths[0]}}{'    | '}{name_arg2}:    {str(arg2):{max_lengths[1]}}{'    | '}{name_arg3}:    {str(arg3):{max_lengths[2]}}{'    | '}{name_arg4}:    {str(arg4):{max_lengths[3]}}")

    elif (name_arg1 and name_arg2 and name_arg3) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{max_lengths[0]}}{'    | '}{name_arg2}:    {str(arg2):{max_lengths[1]}}{'    | '}{name_arg3}:    {str(arg3)}")

    elif (name_arg1 and name_arg2) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{max_lengths[0]}}{'    | '}{name_arg2}:    {str(arg2):{max_lengths[1]}}")

    elif name_arg1 is not None:
        return (
            f"{name_arg1}:    {str(arg1):{max_lengths[0]}}")


def my_table_db_full_name(rows, colum_name):
    max_lengths = [0] * len(rows[0])

    for row in rows:
        for index, item in enumerate(row):
            item_length = len(str(item)) if item is not None else 0
            if item_length > max_lengths[index]:
                max_lengths[index] = item_length
    control_num = 0
    num1 = 0
    num2 = 1
    num3 = 2
    num4 = 3
    num5 = 4
    num6 = 5
    num7 = 6
    for i in range(len(rows)):
        if len(colum_name) == 7:
            print(
                f"{colum_name[0]}:    {str(get_rows(rows, num1, control_num)):{max_lengths[0]}}{'    | '}{colum_name[1]}:    {str(get_rows(rows, num2, control_num)):{max_lengths[1]}}{'    | '}{colum_name[2]}:    {str(get_rows(rows, num3, control_num)):{max_lengths[2]}}{'    | '}{colum_name[3]}:    {str(get_rows(rows, num4, control_num)):{max_lengths[3]}}{'    | '}{colum_name[4]}:    {str(get_rows(rows, num5, control_num)):{max_lengths[4]}}{'    | '}{colum_name[5]}:    {str(get_rows(rows, num6, control_num)):{max_lengths[5]}}{'    | '}{colum_name[6]}:    {str(get_rows(rows, num7, control_num)):{max_lengths[6]}}")
            control_num += 1

        if len(colum_name) == 6:
            print(
                f"{colum_name[0]}:    {str(get_rows(rows, num1, control_num)):{max_lengths[0]}}{'    | '}{colum_name[1]}:    {str(get_rows(rows, num2, control_num)):{max_lengths[1]}}{'    | '}{colum_name[2]}:    {str(get_rows(rows, num3, control_num)):{max_lengths[2]}}{'    | '}{colum_name[3]}:    {str(get_rows(rows, num4, control_num)):{max_lengths[3]}}{'    | '}{colum_name[4]}:    {str(get_rows(rows, num5, control_num)):{max_lengths[4]}}{'    | '}{colum_name[5]}:    {str(get_rows(rows, num6, control_num)):{max_lengths[5]}}")
            control_num += 1

        if len(colum_name) == 5:
            print(
                f"{colum_name[0]}:    {str(get_rows(rows, num1, control_num)):{max_lengths[0]}}{'    | '}{colum_name[1]}:    {str(get_rows(rows, num2, control_num)):{max_lengths[1]}}{'    | '}{colum_name[2]}:    {str(get_rows(rows, num3, control_num)):{max_lengths[2]}}{'    | '}{colum_name[3]}:    {str(get_rows(rows, num4, control_num)):{max_lengths[3]}}{'    | '}{colum_name[4]}:    {str(get_rows(rows, num5, control_num)):{max_lengths[4]}}")
            control_num += 1

        if len(colum_name) == 4:
            print(
                f"{colum_name[0]}:    {str(get_rows(rows, num1, control_num)):{max_lengths[0]}}{'    | '}{colum_name[1]}:    {str(get_rows(rows, num2, control_num)):{max_lengths[1]}}{'    | '}{colum_name[2]}:    {str(get_rows(rows, num3, control_num)):{max_lengths[2]}}{'    | '}{colum_name[3]}:    {str(get_rows(rows, num4, control_num)):{max_lengths[3]}}")
            control_num += 1

        if len(colum_name) == 3:
            print(
                f"{colum_name[0]}:    {str(get_rows(rows, num1, control_num)):{max_lengths[0]}}{'    | '}{colum_name[1]}:    {str(get_rows(rows, num2, control_num)):{max_lengths[1]}}{'    | '}{colum_name[2]}:    {str(get_rows(rows, num3, control_num)):{max_lengths[2]}}")
            control_num += 1

        if len(colum_name) == 2:
            print(
                f"{colum_name[0]}:    {str(get_rows(rows, num1, control_num)):{max_lengths[0]}}{'    | '}{colum_name[1]}:    {str(get_rows(rows, num2, control_num)):{max_lengths[1]}}")
            control_num += 1

        if len(colum_name) == 1:
            print(
                f"{colum_name[0]}:    {str(get_rows(rows, num1, control_num)):{max_lengths[0]}}")
            control_num += 1


def my_table_db(rows, name_arg1=None, arg1=None, name_arg2=None, arg2=None, name_arg3=None, arg3=None, name_arg4=None,
                arg4=None, name_arg5=None, arg5=None, name_arg6=None, arg6=None, name_arg7=None, arg7=None):
    max_lengths = [0] * len(rows[0])

    for row in rows:
        for index, item in enumerate(row):
            item_length = len(str(item)) if item is not None else 0
            if item_length > max_lengths[index]:
                max_lengths[index] = item_length

    max_lengths_column_name = [] * len(rows[0])

    if (name_arg1, name_arg2, name_arg3, name_arg4, name_arg5, name_arg6, name_arg7) is not None:
        max_lengths_column_name.append(name_arg1)
        max_lengths_column_name.append(name_arg2)
        max_lengths_column_name.append(name_arg3)
        max_lengths_column_name.append(name_arg4)
        max_lengths_column_name.append(name_arg5)
        max_lengths_column_name.append(name_arg6)
        max_lengths_column_name.append(name_arg7)

    elif (name_arg1, name_arg2, name_arg3, name_arg4, name_arg5, name_arg6) is not None:
        max_lengths_column_name.append(name_arg1)
        max_lengths_column_name.append(name_arg2)
        max_lengths_column_name.append(name_arg3)
        max_lengths_column_name.append(name_arg4)
        max_lengths_column_name.append(name_arg5)
        max_lengths_column_name.append(name_arg6)

    elif (name_arg1, name_arg2, name_arg3, name_arg4, name_arg5,) is not None:
        max_lengths_column_name.append(name_arg1)
        max_lengths_column_name.append(name_arg2)
        max_lengths_column_name.append(name_arg3)
        max_lengths_column_name.append(name_arg4)
        max_lengths_column_name.append(name_arg5)

    elif (name_arg1, name_arg2, name_arg3, name_arg4) is not None:
        max_lengths_column_name.append(name_arg1)
        max_lengths_column_name.append(name_arg2)
        max_lengths_column_name.append(name_arg3)
        max_lengths_column_name.append(name_arg4)
    elif (name_arg1, name_arg2, name_arg3) is not None:
        max_lengths_column_name.append(name_arg1)
        max_lengths_column_name.append(name_arg2)
        max_lengths_column_name.append(name_arg3)
    elif (name_arg1, name_arg2) is not None:
        max_lengths_column_name.append(name_arg1)
        max_lengths_column_name.append(name_arg2)
    elif name_arg1 is not None:
        max_lengths_column_name.append(name_arg1)

    return_len_max_lengths_list = [0] * len(rows[0])

    for index, item in enumerate(max_lengths):
        len_max_lengths = max_lengths[index]
        len_max_lengths_column_name = len(str(max_lengths_column_name[index]))

        if len_max_lengths >= len_max_lengths_column_name:
            return_len_max_lengths_list[index] = len_max_lengths_column_name + (
                    len_max_lengths - len_max_lengths_column_name)
        elif len_max_lengths <= len_max_lengths_column_name:
            return_len_max_lengths_list[index] = (len_max_lengths + (len_max_lengths_column_name - len_max_lengths))

    result = (
        f"{str(name_arg1):{return_len_max_lengths_list[0]}}{'    | '}{str(name_arg2):{return_len_max_lengths_list[1]}}{'    | '}{str(name_arg3):{return_len_max_lengths_list[2]}}{'    | '}{str(name_arg4):{return_len_max_lengths_list[3]}}{'    | '}{str(name_arg5):{return_len_max_lengths_list[4]}}{'    | '}{str(name_arg6):{return_len_max_lengths_list[5]}}{'    | '}{str(name_arg7):{return_len_max_lengths_list[6]}}")

    print(result)

    print('-' * len(result))

    if (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5 and name_arg6 and name_arg7) is not None:
        return (
            f"{str(arg1):{return_len_max_lengths_list[0]}}{'    | '}{str(arg2):{return_len_max_lengths_list[1]}}{'    | '}{str(arg3):{return_len_max_lengths_list[2]}}{'    | '}{str(arg4):{return_len_max_lengths_list[3]}}{'    | '}{str(arg5):{return_len_max_lengths_list[4]}}{'    | '}{str(arg6):{return_len_max_lengths_list[5]}}{'    | '}{str(arg7):{return_len_max_lengths_list[6]}}")

    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5 and name_arg6) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{return_len_max_lengths_list[0]}}{'    | '}{name_arg2}:    {str(arg2):{return_len_max_lengths_list[1]}}{'    | '}{name_arg3}:    {str(arg3):{return_len_max_lengths_list[2]}}{'    | '}{name_arg4}:    {str(arg4):{return_len_max_lengths_list[3]}}{'    | '}{name_arg5}:    {str(arg5):{return_len_max_lengths_list[4]}}{'    | '}{name_arg6}:    {str(arg6):{return_len_max_lengths_list[5]}}")

    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4 and name_arg5) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{return_len_max_lengths_list[0]}}{'    | '}{name_arg2}:    {str(arg2):{return_len_max_lengths_list[1]}}{'    | '}{name_arg3}:    {str(arg3):{return_len_max_lengths_list[2]}}{'    | '}{name_arg4}:    {str(arg4):{return_len_max_lengths_list[3]}}{'    | '}{name_arg5}:    {str(arg5):{return_len_max_lengths_list[4]}}")

    elif (name_arg1 and name_arg2 and name_arg3 and name_arg4) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{return_len_max_lengths_list[0]}}{'    | '}{name_arg2}:    {str(arg2):{return_len_max_lengths_list[1]}}{'    | '}{name_arg3}:    {str(arg3):{return_len_max_lengths_list[2]}}{'    | '}{name_arg4}:    {str(arg4):{return_len_max_lengths_list[3]}}")

    elif (name_arg1 and name_arg2 and name_arg3) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{return_len_max_lengths_list[0]}}{'    | '}{name_arg2}:    {str(arg2):{return_len_max_lengths_list[1]}}{'    | '}{name_arg3}:    {str(arg3)}")

    elif (name_arg1 and name_arg2) is not None:
        return (
            f"{name_arg1}:    {str(arg1):{return_len_max_lengths_list[0]}}{'    | '}{name_arg2}:    {str(arg2):{return_len_max_lengths_list[1]}}")

    elif name_arg1 is not None:
        return (
            f"{name_arg1}:    {str(arg1):{return_len_max_lengths_list[0]}}")


def my_table_db_full(rows, colum_name):
    max_lengths = [0] * len(rows[0])

    for row in rows:
        for index, item in enumerate(row):
            item_length = len(str(item)) if item is not None else 0
            if item_length > max_lengths[index]:
                max_lengths[index] = item_length

    return_len_max_lengths_list = [0] * len(rows[0])

    for index, item in enumerate(max_lengths):
        len_max_lengths = max_lengths[index]
        len_max_lengths_column_name = len(str(colum_name[index]))

        if len_max_lengths >= len_max_lengths_column_name:
            return_len_max_lengths_list[index] = len_max_lengths_column_name + (
                    len_max_lengths - len_max_lengths_column_name)
        elif len_max_lengths <= len_max_lengths_column_name:
            return_len_max_lengths_list[index] = (len_max_lengths + (len_max_lengths_column_name - len_max_lengths))

    control_num = 0
    num1 = 0
    num2 = 1
    num3 = 2
    num4 = 3
    num5 = 4
    num6 = 5
    num7 = 6

    result = None

    if len(colum_name) == 7:
        result = (
            f"{str(colum_name[0]):{return_len_max_lengths_list[0]}}{'    | '}{str(colum_name[1]):{return_len_max_lengths_list[1]}}{'    | '}{str(colum_name[2]):{return_len_max_lengths_list[2]}}{'    | '}{str(colum_name[3]):{return_len_max_lengths_list[3]}}{'    | '}{str(colum_name[4]):{return_len_max_lengths_list[4]}}{'    | '}{str(colum_name[5]):{return_len_max_lengths_list[5]}}{'    | '}{str(colum_name[6]):{return_len_max_lengths_list[6]}}")

    if len(colum_name) == 6:
        result = (
            f"{str(colum_name[0]):{return_len_max_lengths_list[0]}}{'    | '}{str(colum_name[1]):{return_len_max_lengths_list[1]}}{'    | '}{str(colum_name[2]):{return_len_max_lengths_list[2]}}{'    | '}{str(colum_name[3]):{return_len_max_lengths_list[3]}}{'    | '}{str(colum_name[4]):{return_len_max_lengths_list[4]}}{'    | '}{str(colum_name[5]):{return_len_max_lengths_list[5]}}")

    if len(colum_name) == 5:
        result = (
            f"{str(colum_name[0]):{return_len_max_lengths_list[0]}}{'    | '}{str(colum_name[1]):{return_len_max_lengths_list[1]}}{'    | '}{str(colum_name[2]):{return_len_max_lengths_list[2]}}{'    | '}{str(colum_name[3]):{return_len_max_lengths_list[3]}}{'    | '}{str(colum_name[4]):{return_len_max_lengths_list[4]}}")

    if len(colum_name) == 4:
        result = (
            f"{str(colum_name[0]):{return_len_max_lengths_list[0]}}{'    | '}{str(colum_name[1]):{return_len_max_lengths_list[1]}}{'    | '}{str(colum_name[2]):{return_len_max_lengths_list[2]}}{'    | '}{str(colum_name[3]):{return_len_max_lengths_list[3]}}")

    if len(colum_name) == 3:
        result = (
            f"{str(colum_name[0]):{return_len_max_lengths_list[0]}}{'    | '}{str(colum_name[1]):{return_len_max_lengths_list[1]}}{'    | '}{str(colum_name[2]):{return_len_max_lengths_list[2]}}")

    if len(colum_name) == 2:
        result = (
            f"{str(colum_name[0]):{return_len_max_lengths_list[0]}}{'    | '}{str(colum_name[1]):{return_len_max_lengths_list[1]}}")

    if len(colum_name) == 1:
        result = (
            f"{str(colum_name[0]):{return_len_max_lengths_list[0]}}")

    print(result)
    print('-' * len(result))
    for i in range(len(rows)):
        if len(colum_name) == 7:
            print(
                f"{str(get_rows(rows, num1, control_num)):{return_len_max_lengths_list[0]}}{'    | '}{str(get_rows(rows, num2, control_num)):{return_len_max_lengths_list[1]}}{'    | '}{str(get_rows(rows, num3, control_num)):{return_len_max_lengths_list[2]}}{'    | '}{str(get_rows(rows, num4, control_num)):{return_len_max_lengths_list[3]}}{'    | '}{str(get_rows(rows, num5, control_num)):{return_len_max_lengths_list[4]}}{'    | '}{str(get_rows(rows, num6, control_num)):{return_len_max_lengths_list[5]}}{'    | '}{str(get_rows(rows, num7, control_num)):{return_len_max_lengths_list[6]}}")
            control_num += 1

        if len(colum_name) == 6:
            print(
                f"{str(get_rows(rows, num1, control_num)):{return_len_max_lengths_list[0]}}{'    | '}{str(get_rows(rows, num2, control_num)):{return_len_max_lengths_list[1]}}{'    | '}{str(get_rows(rows, num3, control_num)):{return_len_max_lengths_list[2]}}{'    | '}{str(get_rows(rows, num4, control_num)):{return_len_max_lengths_list[3]}}{'    | '}{str(get_rows(rows, num5, control_num)):{return_len_max_lengths_list[4]}}{'    | '}{str(get_rows(rows, num6, control_num)):{return_len_max_lengths_list[5]}}")
            control_num += 1

        if len(colum_name) == 5:
            print(
                f"{str(get_rows(rows, num1, control_num)):{return_len_max_lengths_list[0]}}{'    | '}{str(get_rows(rows, num2, control_num)):{return_len_max_lengths_list[1]}}{'    | '}{str(get_rows(rows, num3, control_num)):{return_len_max_lengths_list[2]}}{'    | '}{str(get_rows(rows, num4, control_num)):{return_len_max_lengths_list[3]}}{'    | '}{str(get_rows(rows, num5, control_num)):{return_len_max_lengths_list[4]}}")
            control_num += 1

        if len(colum_name) == 4:
            print(
                f"{str(get_rows(rows, num1, control_num)):{return_len_max_lengths_list[0]}}{'    | '}{str(get_rows(rows, num2, control_num)):{return_len_max_lengths_list[1]}}{'    | '}{str(get_rows(rows, num3, control_num)):{return_len_max_lengths_list[2]}}{'    | '}{str(get_rows(rows, num4, control_num)):{return_len_max_lengths_list[3]}}")
            control_num += 1

        if len(colum_name) == 3:
            print(
                f"{str(get_rows(rows, num1, control_num)):{return_len_max_lengths_list[0]}}{'    | '}{str(get_rows(rows, num2, control_num)):{return_len_max_lengths_list[1]}}{'    | '}{str(get_rows(rows, num3, control_num)):{return_len_max_lengths_list[2]}}")
            control_num += 1

        if len(colum_name) == 2:
            print(
                f"{str(get_rows(rows, num1, control_num)):{return_len_max_lengths_list[0]}}{'    | '}{str(get_rows(rows, num2, control_num)):{return_len_max_lengths_list[1]}}")
            control_num += 1

        if len(colum_name) == 1:
            print(
                f"{str(get_rows(rows, num1, control_num)):{return_len_max_lengths_list[0]}}")
            control_num += 1
