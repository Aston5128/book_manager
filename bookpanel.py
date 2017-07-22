import wx
from wx import grid
from book_manager.borrow import borrow
from book_manager.ser import Ser


class MyGrid(grid.Grid):
    """表格类，处理一个新建一个表格"""

    def __init__(self, parent):
        grid.Grid.__init__(self, parent, -1)

        self.CreateGrid(200, 5)

        self.SetPosition((20, 100))
        self.SetSize((520, 200))

        for i in range(5):
            self.SetColSize(i, 84)


class BookPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)

        self.SetBackgroundColour((235, 235, 235))

        # 选项的标签
        label_list1 = ['全部书籍', '未借书籍', '已借书籍', '需还书籍']

        # 选择盒子, majorDimension 参数表示默认选择为第一个选项
        self.r_box = wx.RadioBox(self, label='图书查询', pos=(20, 20), choices=label_list1, majorDimension=1,
                                 style=wx.RA_SPECIFY_ROWS)

        # 搜索框
        self.text1 = wx.TextCtrl(self, -1, pos=(370, 36))
        self.se_btn = wx.Button(self, -1, label='搜索', pos=(478, 32), size=(60, 30))
        self.text1.SetFocus()

        # 书籍信息表格
        self.my_grid = MyGrid(self)

        # 表格相关属性
        self.lan1 = [
            [(0, '书号'), (1, '书名'), (2, '剩余/总数'), (3, '购书人'), (4, '放置位置')],
            [(0, '书号'), (1, '书名'), (2, '借书人'), (3, '借书日期'), (4, '借出天数')],
            [(0, '书号'), (1, '书名'), (2, '借书人'), (3, '超出天数'), (4, '罚款')]
        ]

        # 书籍信息表格默认显示未借书籍
        for i, lan in self.lan1[0]:
            self.my_grid.SetColLabelValue(i, lan)

        # 默认显示未借书籍表格
        final_list = Ser().get('book_list', 1)

        # 显示表格
        self.display_list(final_list)

        # 借出与归还书籍选框
        label_list2 = ['借       出', '归       还', '添加书籍', '删除书籍']

        self.r_box2 = wx.RadioBox(self, label='图书管理', pos=(20, 320),
                                  choices=label_list2, majorDimension=1, style=wx.RA_SPECIFY_COLS)

        self.static_text1 = wx.StaticText(self, -1, pos=(125, 335), label='借出的书名：')
        self.text2 = wx.TextCtrl(self, -1, pos=(300, 335), size=(150, 20))

        self.static_text2 = wx.StaticText(self, -1, pos=(125, 360), label='借书人：')
        self.text3 = wx.TextCtrl(self, -1, pos=(300, 360), size=(150, 20))

        self.static_text3 = wx.StaticText(self, -1, pos=(125, 385))
        self.text4 = wx.TextCtrl(self, -1, pos=(300, 385), size=(150, 20))
        self.static_text3.Show(False)
        self.text4.Show(False)

        # 单独为添加书籍的数量的选择框
        choices = [str(i) for i in range(1, 21)]

        self.static_text4 = wx.StaticText(self, -1, label='添加数量：', pos=(460, 335))
        self.choice_box = wx.Choice(self, -1, choices=choices, pos=(460, 360))
        self.static_text4.Show(False)
        self.choice_box.Show(False)

        self.comit_btn = wx.Button(self, -1, pos=(250, 410), label='借出')

        # self.Bind(wx.EVT_MOTION, self.on_motion)
        self.r_box.Bind(wx.EVT_RADIOBOX, self.on_r_box)
        self.r_box2.Bind(wx.EVT_RADIOBOX, self.on_r_box2)
        self.se_btn.Bind(wx.EVT_BUTTON, self.on_btn_clicked)
        self.text1.Bind(wx.EVT_TEXT, self.on_btn_clicked)
        self.comit_btn.Bind(wx.EVT_BUTTON, self.on_comit_btn)

    def on_r_box(self, evt):
        evt.GetInt()

        self.flash_grid()

    def on_r_box2(self, evt):
        evt.GetInt()
        selected_btn = self.r_box2.GetStringSelection()

        self.text2.Clear()
        self.text3.Clear()
        self.text4.Clear()

        self.static_text2.Show()
        self.text3.Show()
        self.static_text3.Show(False)
        self.text4.Show(False)
        self.static_text4.Show(False)
        self.choice_box.Show(False)

        self.text2.SetFocus()

        if selected_btn == '借       出':
            # 更改 static_text1 的文字
            self.static_text1.SetLabel('借出的书名：')
            # 更改 static_text2 的文字
            self.static_text2.SetLabel('借书人：')
            # 更改提交按钮的文字
            self.comit_btn.SetLabel('借出')

        elif selected_btn == '归       还':
            self.static_text1.SetLabel('归还的书名：')
            self.static_text2.SetLabel('还书人：')
            self.comit_btn.SetLabel('归还')

        elif selected_btn == '添加书籍':
            self.static_text1.SetLabel('书名：')
            self.static_text2.SetLabel('购书人：')
            self.static_text3.SetLabel('放置位置：')

            self.static_text3.Show()
            self.text4.Show()

            self.static_text4.SetLabel('添加数量：')

            self.static_text4.Show()
            self.choice_box.Show()

            self.comit_btn.SetLabel('添加')

        else:
            self.static_text1.SetLabel('书名：')
            self.static_text2.SetLabel('借书人(选填)：')

            self.static_text4.SetLabel('删除数量：')

            self.static_text4.Show()
            self.choice_box.Show()

            self.comit_btn.SetLabel('删除')

    def on_btn_clicked(self, evt):
        evt.GetInt()
        # 取得当前输入的值
        text1_str = self.text1.GetLineText(0)

        self.my_grid.ClearGrid()

        # 获得当前选框中被选择的选项内容
        selected_btn = self.r_box.GetStringSelection()

        final_list = Ser().search(text1_str, selected_btn)

        try:
            for i in range(len(final_list)):
                for j in range(len(final_list[i])):
                    self.my_grid.SetCellValue(i, j, final_list[i][j])
        finally:
            pass

    def on_comit_btn(self, evt):
        evt.GetInt()
        btn_str = self.comit_btn.GetLabel()

        t1 = self.text2.GetLineText(0)
        t2 = self.text3.GetLineText(0)
        t3 = self.text4.GetLineText(0)
        t4 = self.choice_box.GetStringSelection()

        if btn_str == '借出':
            temp_list = Ser().search(t1, '全部书籍')
            if t1 == '':
                self.alarm('书名不能为空', True)
            elif len(temp_list) == 0:
                self.alarm('《' + t1 + '》在书库中不存在', True)
            elif t2 == '':
                self.alarm('借书人不能为空', True)
            elif temp_list != [] and t2 is not None:
                rest_book = int(temp_list[0][2].split('/')[0])
                if rest_book == 0:
                    self.alarm('《' + t1 + '》全部被借出', True)
                else:
                    self.alarm('《' + t1 + '》借出成功，借书人：' + t2, False)

                    # 更改数据
                    borrow().borrowing(t1, t2)

        elif btn_str == '归还':
            temp_list1 = Ser().search(t1, '全部书籍')
            temp_list2 = Ser().search(t1, '已借书籍')
            temp_list3 = Ser().search(t1, '需选书籍')
            if t1 == '':
                self.alarm('书名不能为空', True)
            elif t2 == '':
                self.alarm('还书人不能为空', True)
            elif len(temp_list1) == 0:
                self.alarm('输入书籍在书库中不存在', True)
            elif len(temp_list2) == 0:
                self.alarm('该书未被借出', True)
            elif temp_list2:
                temp = []
                for borrow_list in temp_list2:
                    if borrow_list[2] == t2:
                        temp = borrow_list
                if not temp:
                    self.alarm(t2 + ' 没有借' + '《' + t1 + '》', True)
                else:
                    if not temp_list3:
                        self.alarm(t2 + ' 归还' + '《' + t1 + '》成功', False)
                    else:
                        temp_list3 = temp_list3[0]
                        borrow_time = temp_list3[-2]
                        pay = int(float(temp_list3[-1]))
                        self.alarm(t2 + ' 归还' + '《' + t1 + '》，超出' + borrow_time + '天，欠费：' + str(pay), False)

                    # 更新数据
                    borrow().backing(t1, t2)

        elif btn_str == '添加':
            if t1 == '':
                self.alarm('书名不能为空', True)
            elif t2 == '':
                self.alarm('购书人不能为空', True)
            elif t3 == '':
                self.alarm('放置位置不能为空', True)
            else:
                self.alarm('添加《' + t1 + '》成功', False)
                borrow().adding(t1, t2, t3, t4)

        elif btn_str == '删除':
            temp_list1 = Ser().search(t1, '全部书籍')
            if t1 == '':
                self.alarm('书名不能为空', True)
            elif not temp_list1:
                self.alarm(('《' + t1 + '》在书库中不存在'), True)
            else:
                if t2 == '':
                    if int(temp_list1[0][2].split('/')[0]) < int(t4):
                        self.alarm('删除书籍数超界', True)
                    else:
                        self.alarm('删除书籍成功', False)
                        borrow().remove(book=t1, delete_num=t4)
                else:
                    temp_list2 = Ser().search(t1 + ' ' + t2, '已借书籍')
                    if not temp_list2:
                        self.alarm('《' + t1 + '》未被' + t2 + '借走', True)
                    else:
                        self.alarm('删除书籍成功', False)
                        borrow().remove(book=t1, delete_num=t4, person=t2)

        # 刷新表格显示新状态
        self.flash_grid()

    @staticmethod
    def on_motion(evt):
        print(evt.GetPosition())

    def alarm(self, alarm_text, is_alarm):
        """弹出对话框，告诉用户传入的一段信息"""
        width = 300
        height = 100

        screen_size = wx.DisplaySize()

        if is_alarm:
            title = '错误'
        else:
            title = '成功'

        temp_frame = wx.Frame(self, -1, title=title, size=(width, height),
                              pos=((screen_size[0] - width) / 2, (screen_size[1] - height) / 2),
                              style=wx.CAPTION | wx.CLOSE_BOX)

        temp_panel = wx.Panel(temp_frame, -1)
        temp_panel.SetBackgroundColour((255, 255, 255))

        # 显示错误图像
        if is_alarm:
            img = wx.Image('alarm.jpg', wx.BITMAP_TYPE_JPEG)
            wx.StaticBitmap(temp_panel, -1, label=img.ConvertToBitmap(), pos=(20, 10))
            wx.StaticText(temp_panel, -1, label=alarm_text, pos=(80, 30))
        else:
            wx.StaticText(temp_panel, -1, label=alarm_text, pos=(20, 30))

        temp_frame.Show()

    def display_list(self, list1):
        """显示表格的函数"""
        for i in range(0, len(list1)):
            for j in range(0, 5):
                self.my_grid.SetCellValue(i, j, list1[i][j])

    def flash_grid(self):
        selected_btn = self.r_box.GetStringSelection()

        # 每次点击清空列表
        self.my_grid.ClearGrid()

        # 每次点击清空输入框
        self.text1.Clear()

        if selected_btn == '全部书籍':
            for i, lan in self.lan1[0]:
                self.my_grid.SetColLabelValue(i, lan)

            # 表格处理类对象
            final_list = Ser().get('book_list', 1)

            # 显示表格
            self.display_list(final_list)

        elif selected_btn == '未借书籍':
            for i, lan in self.lan1[0]:
                self.my_grid.SetColLabelValue(i, lan)

            # 表格处理类对象
            final_list = Ser().get('book_list', 2)

            # 显示表格
            self.display_list(final_list)

        elif selected_btn == '已借书籍':
            for i, lan in self.lan1[1]:
                self.my_grid.SetColLabelValue(i, lan)

            final_list = Ser().get('borrow_list', 3)

            self.display_list(final_list)

        else:
            for i, lan in self.lan1[2]:
                self.my_grid.SetColLabelValue(i, lan)

            final_list = Ser().get('borrow_list', 4)

            self.display_list(final_list)
