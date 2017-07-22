import re
import datetime
from book_manager.ser import Ser


class borrow:
    def borrowing(self, book, borrow_person):
        book_num = self.book_list_oprate(-1, book=book)
        self.borrow_list_oprate(-1, person=borrow_person, book=book, book_num=book_num)

    def backing(self, book, borrow_person):
        self.book_list_oprate(1, book=book)
        self.borrow_list_oprate(1, book=book, person=borrow_person)

    def adding(self, book, buyer, place, number):
        temp_list = Ser().search(book, '全部书籍')
        if not temp_list:
            with open('book_list', 'r') as input_file:
                num = str(len(input_file.readlines()) + 1)
                if len(num) == 1:
                    num = '000' + num
                elif len(num) == 2:
                    num = '00' + num
                elif len(num) == 3:
                    num = '0' + num

            self.book_list_oprate(3, book=book, person=buyer, place=place, book_num=num, number=number + '/' + number)
        else:
            self.book_list_oprate(3, book=book, number=number)

    def remove(self, **kwargs):
        if len(kwargs) == 3:
            self.book_list_oprate(4, book=kwargs['book'], delete_num=kwargs['delete_num'], number='0')
            self.borrow_list_oprate(4, book=kwargs['book'], delete_num=kwargs['delete_num'], person=kwargs['person'])
        else:
            self.book_list_oprate(4, book=kwargs['book'], delete_num=kwargs['delete_num'], number=kwargs['delete_num'])

    @staticmethod
    def borrow_list_oprate(oprate, **kwargs):
        """图书管理对 borrow_list 文件的相关操作"""
        if oprate == -1:
            with open('borrow_list', 'a') as output_file:
                now_date = str(datetime.datetime.now()).split(' ')[0].replace('-', '/')
                temp_str = '\n' + kwargs['book_num'] + ' ' + kwargs['book'] + ' ' + kwargs['person'] + ' ' + now_date
                output_file.write(temp_str)

        elif oprate == 1:
            input_file = open('borrow_list', 'r')
            final_list = []
            for str1 in input_file.readlines():
                if re.search(kwargs['book'] + ' ' + kwargs['person'], str1):
                    continue
                final_list.append(str1)
            input_file.close()

            output_file = open('borrow_list', 'w')
            for i in range(len(final_list) - 1):
                output_file.write(final_list[i])
            output_file.write(final_list[-1].replace('\n', ''))
            output_file.close()

        elif oprate == 4:
            final_list = []
            with open('borrow_list', 'r') as input_file:
                for temp_str in input_file.readlines():
                    if re.search(kwargs['book'] + ' ' + kwargs['person'], temp_str) is not None:
                        continue
                    final_list.append(temp_str)

                final_list[-1] = final_list[-1].replace('\n', '')

            with open('borrow_list', 'w') as output_file:
                for str1 in final_list:
                    output_file.write(str1)

    @staticmethod
    def book_list_oprate(oprate, **kwargs):
        """图书管理对 book_list 文件的相关操作"""
        final_list = []
        book_num = ''
        with open('book_list', 'r') as book_file_input:
            if oprate == 3:
                if len(kwargs) == 5:
                    with open('book_list', 'a') as output_file:
                        output_file.write('\n' + kwargs['book_num'] + ' ' + kwargs['book'] + ' ' + kwargs['number'] +
                                          ' ' + kwargs['person'] + ' ' + kwargs['place'])
                elif len(kwargs) == 2:
                    for temp_str in book_file_input.readlines():
                        if re.search(kwargs['book'], temp_str):
                            temp_list = temp_str.split(' ')
                            temp_list1 = temp_list[2].split('/')
                            temp_list[2] = str(int(temp_list1[0]) + int(kwargs['number'])) + '/' + \
                                           str(int(temp_list1[1]) + int(kwargs['number']))
                            temp_str = ''
                            for str1 in temp_list:
                                temp_str += str1 + ' '
                            temp_str = temp_str[:-1]
                        final_list.append(temp_str)
            elif oprate == 4:
                for temp_str in book_file_input.readlines():
                    if re.search(kwargs['book'], temp_str):
                        temp_list = temp_str.split(' ')
                        temp_list1 = temp_list[2].split('/')
                        if int(temp_list1[1]) - int(kwargs['delete_num']) == 0:
                            continue
                        else:
                            temp_list[2] = str(int(temp_list1[0]) - int(kwargs['number'])) + '/' + \
                                           str(int(temp_list1[1]) - int(kwargs['delete_num']))
                        temp_str = ''
                        for str1 in temp_list:
                            temp_str += str1 + ' '
                        temp_str = temp_str[:-1]
                    final_list.append(temp_str)

            for temp_str in book_file_input.readlines():
                if (oprate == 1 or oprate == -1) and re.search(kwargs['book'], temp_str) is not None:
                    temp_list = temp_str.split(' ')
                    date_parts = temp_list[2].split('/')
                    rest_book = int(date_parts[0]) + oprate
                    rest_book = str(rest_book) + '/' + date_parts[1]
                    temp_list[2] = rest_book

                    book_num = temp_list[0]

                    temp_str = ''
                    for str1 in temp_list:
                        temp_str = temp_str + str1 + ' '
                    temp_str = temp_str[:-1]

                final_list.append(temp_str)

        with open('book_list', 'w') as book_file_output:
            for str1 in final_list:
                book_file_output.write(str1)

        return book_num
