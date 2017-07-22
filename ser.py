import re
import datetime


class Ser:
    def get(self, file_name, mod):
        final_list = []
        with open(file_name, 'r') as in_file:
            for str1 in in_file.readlines():
                temp_str = str1.replace('\n', '')
                temp_list = temp_str.split(' ')

                if mod == 2 and temp_list[2].split('/')[0] is '0':
                    continue

                elif mod == 3:
                    temp_list.append(self.get_borrow_time(temp_list))

                elif mod == 4:
                    borrow_time = int(self.get_borrow_time(temp_list).split(' ')[0])
                    if borrow_time < 60:
                        continue
                    else:
                        temp_list = temp_list[:3]
                        temp_list.append(str(borrow_time-60))
                        temp_list.append(str(int(borrow_time*0.2)))

                final_list.append(temp_list)

        return final_list

    def search(self, search_text, selected_str):
        if selected_str == '全部书籍':
            return self.search_detail(search_text, 'book_list', 1)
        elif selected_str == '未借书籍':
            return self.search_detail(search_text, 'book_list', 2)
        elif selected_str == '已借书籍':
            return self.search_detail(search_text, 'borrow_list', 3)
        else:
            return self.search_detail(search_text, 'borrow_list', 4)

    @staticmethod
    def get_borrow_time(temp_list):
        time_list = [int(num) for num in temp_list[-1].split('/')]
        temp_date = datetime.datetime(time_list[0], time_list[1], time_list[2], 0, 0, 0, 0)
        borrow_time = str((datetime.datetime.now() - temp_date)).split(',')[0]
        if re.search('day', borrow_time):
            return borrow_time
        else:
            return '0 day'

    def search_detail(self, search_text, file_name, mod):
        final_list = []
        with open(file_name, 'r') as input_file:
            for str1 in input_file.readlines():
                temp_str = str1.replace('\n', '')
                if re.search(search_text, temp_str) is not None:
                    temp_list = temp_str.split(' ')
                    if mod == 2 and temp_list[2].split('/')[0] is '0':
                        continue

                    elif mod == 3:
                        temp_list.append(self.get_borrow_time(temp_list))

                    elif mod == 4:
                        borrow_time = int(self.get_borrow_time(temp_list).split(' ')[0])
                        if borrow_time < 60:
                            continue
                        else:
                            temp_list = temp_list[:3]
                            temp_list.append(str(borrow_time - 60))
                            temp_list.append(str(borrow_time * 0.2))

                    final_list.append(temp_list)

        return final_list


if __name__ == '__main__':
    Ser().search('book2', '需还书籍')
