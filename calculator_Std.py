from tkinter import *
from math import *



class Standard_Calculator:

    def __init__(self):
        self.calculator_std = Tk()
        self.calculator_std.geometry('410x550')
        self.calculator_std.resizable(0,0)
        self.calculator_std.title('Standard Calculator')

        self.ans = 0 #Gan ans = 0

        self.frame_screen = self.frame_screen()
        self.total_expression = ""      #Giá trị đầu của vùng nhập phép tính
        self.current_expression = ""    #Giá trị đầu của vùng hiển thị kết quả

        #total_label là vùng nhập, label là vùng hiện kết quả
        self.total_label, self.label = self.display_label()

        #Frame thanh công cụ:
        self.frame_tools = self.frame_tools()
        #Các nút trên thanh công cụ
        self.button_tools = self.button_tools()

        self.text_standard = {
                              '(':(1,1), ')':(1,2), '\u221A':(1,3), '\u00F7':(1,4), #\u unicode
                              '7':(2,1), '8':(2,2), '9':(2,3), '\u00D7':(2,4),
                              '4':(3,1), '5':(3,2), '6':(3,3), '\u2212':(3,4),
                              '1':(4,1), '2':(4,2), '3':(4,3), '\u002B':(4,4),
                              '0':(5,1), '.':(5,2), 'ans':(5,3), '\u21A9':(5,4)
        }
        #Frame Phím cơ bản cho máy tính
        self.frame_button_standard = self.frame_button_standard()
        #Tạo các phím cơ bản
        self.button_standard = self.button_standard()

        self.frame_history = self.frame_history()
        self.history = self.scrollbar_history()

        self.actualHistoryOperation = StringVar()
        self.actualHistoryOperation.trace('w', self.disable_clearall_button)
        self.input_from_keyboard()

    def frame_screen(self):
        frame = Frame(self.calculator_std, height = 221, bg = '#4781B9')
        frame.configure(relief = 'groove', padx = 3, pady = 2)
        frame.place(x = 0, y = 230)
        return frame

    def frame_history(self):
        frame = Frame(self.calculator_std, height = 200)
        frame.configure(relief = 'groove', padx = 0, pady = 0)
        frame.place(x = 0, y = 0)
        return frame

    #Method tạo frame thanh công cụ
    def frame_tools(self):
        frame = Frame(self.calculator_std, height = 221, bg = '#EDEDED')
        frame.configure(relief = 'groove')
        frame.place(x = 5, y = 280)
        return frame

    def frame_button_standard(self):
        frame = Frame(self.calculator_std, height = 221, bg = '#EDEDED')
        frame.configure(relief = 'groove')
        frame.place(x = 2, y = 325)
        return frame

    def scrollbar_history(self):
        scrollbar = Scrollbar(self.frame_history, orient = VERTICAL)
        scrollbar.pack(side = RIGHT, fill=Y)
        history = Text(self.frame_history, width = 32, heigh = 8, wrap = NONE,
                       font = ("Times", 18),
                       state = "disabled",
                       yscrollcommand = scrollbar.set)
        history.pack(side = TOP, fill = X)
        scrollbar.config(command = history.yview)
        return history

    #Method tạo hiển thị các label để nhập + hiện kết quả trong frame screen
    def display_label(self):
        total_label = Label(self.frame_screen, text = self.total_expression, width = 24, heigh=2, bd = 0, font = ("Times", 14), bg = 'white', anchor = W)
        total_label.pack(side = LEFT)

        label = Label(self.frame_screen, text = self.current_expression, width = 16, heigh = 2, bd = 0, font = ("Times", 14), bg = 'white', anchor = E)
        label.pack(fill = 'both', side = RIGHT)
        return total_label, label

    def button_tools(self):
        global clear_button

        button1 = Button(self.frame_tools, text = 'StdCal', bd = 1, bg = '#EDEDED',
                         font = ('tahoma', 10), width = 8)
        button2 = Button(self.frame_tools, text = 'SciCal', bd = 1, bg = '#EDEDED',
                         font = ('tahoma', 10),width = 8)
        button3 = Button(self.frame_tools, text = 'Plot', bd = 1, bg = '#EDEDED',
                         font = ('tahoma', 10),width = 8)
        button1.pack(padx = 2, pady =2, side = LEFT)
        button2.pack(padx = 2, side = LEFT)
        button3.pack(padx = 2, side = LEFT)

        clear_button = Button(self.frame_tools, text = "clear all", bd = 0, bg = '#EDEDED',
                              font = ("tahoma, 10"), width = 10, state = 'disabled',
                              command = self.clear_all)
        clear_button.pack(padx = 2, side = LEFT)

        AC_button = Button(self.frame_tools, text = "C", bd = 1, bg = '#EDEDED',
                              font = ("tahoma, 10"), width = 5,heigh=2,
                              command = self.C)
        AC_button.pack(padx = 3, side = LEFT)

        backspace_button = Button(self.frame_tools, text = "\u232B", bd = 1, bg = '#EDEDED',
                              font = ("tahoma, 10"), width = 4, heigh = 2,
                              command = self.backsapce)
        backspace_button.pack(padx = 5, side = RIGHT)

    def disable_clearall_button(self, *args):
        global clear_button
        if self.actualHistoryOperation.get():
            clear_button.config(state = 'normal')
        else:
            clear_button.config(state = 'disabled')

    def button_standard(self):
        for text, location in self.text_standard.items():
            
            if location[1] == 4 or text == 'ans':
                button = Button(self.frame_button_standard, text = text, bg = 'white', bd = 1,
                                width = 9, heigh = 1, font = ('Times', 14, 'italic'),
                                command = lambda x = text: self.add_to_expression(x))
                #Hàm ẩn lambda để với mỗi lần nhấn phím thì biểu thức sẽ được add là vùng nhập
                button.grid(row = location[0], column = location[1], padx = 5 , pady=5)
                if text == 'ans':
                    button['width'] = 8

                if text == '\u21A9': #Nut Enter mau xanh
                    button = Button(self.frame_button_standard, text = text, bg = '#4781B9', bd = 1,
                                width = 9, heigh = 1, font = ('Times', 14, 'italic'),
                                command = self.evaluate)
                    button.grid(row = location[0], column = location[1], padx =5 , pady=5)
            else:
                if location[0] == 1:
                    button = Button(self.frame_button_standard, text = text, bg = 'white', bd = 1,
                                width = 8, heigh = 1, font = ('Times', 14),
                                command = lambda x = text: self.add_to_expression(x))
                    button.grid(row = location[0], column = location[1], padx =5 , pady=5)
                else:
                    button = Button(self.frame_button_standard, text = text, bg = '#CACACA', bd = 1,
                                    width = 8, heigh = 1, font = ('Times', 14),
                                    command = lambda x = text: self.add_to_expression(x))
                    button.grid(row = location[0], column = location[1], padx =5 , pady=5)





    #Phương thức để khi nhấn 1 phím thì text sẽ hiện lên trên màn hình hiển thị
    def add_to_expression(self, value): #value là chữ khi nhấn phím thì sẽ hiển thị lên
        if value == '\u221A':
            self.total_expression += str(value)+'('
        else:
            self.total_expression += str(value) #Giá trị của vùng nhập phép tính
        
        self.update_total_label() #Update Label hiển thị phép tính

    #Method tính toán để gán vào phím enter
    def evaluate(self):
        operator = {'\u00F7': '/', '\u00D7':'*', '\u2212':'-', '\u002B':'+', '\u221A':'sqrt'}
        express = self.total_label['text']
        a = express.count('(') - express.count(')')
        if a>0:
            express += ')'*a
            self.total_expression = express
            self.update_total_label()
        #Thay the ans bang gia tri da luu tru trong bien self.ans
        if 'ans' in express:
            express = express.replace('ans', str(self.ans))

        #VÒng lap thay the ky tu Unicode sang ky tu python hieu
        for i in express:
            if str(i) in list(operator.keys()):
                express = express.replace(i, operator[i])

        try:
            self.current_expression = "= "+str(eval(express))[:13]+' '
        except Exception:
            self.current_expression = "Math Error "
        
        finally:
            self.update_label()
        
        if self.current_expression != "Math Error ":
            self.add_history()
            self.add_ans()

    #Method update Label hiện phép tính khi nhập
    def update_total_label(self):
        self.total_label.configure(text = self.total_expression)

    #Method update label kết quả
    def update_label(self):
        self.label.configure(text = self.current_expression)

    def clear_all(self):
        self.actualHistoryOperation.set("")
        self.history.config(state = NORMAL)
        self.history.delete(1.0, END)
        self.history.config(state = DISABLED)

        self.total_expression = ""
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
        self.add_ans()
        return

    def C(self):
        self.total_expression = ""
        self.current_expression = ""
        self.update_total_label()
        self.update_label()
        return

    def backsapce(self):
        if self.total_expression != "":
            self.total_expression = self.total_expression[0:len(self.total_expression)-1]
            self.current_expression = ""
            self.update_total_label()
            self.update_label()
        else:
            pass

    def add_history(self):    
        self.actualHistoryOperation.set('\n'+' '*2+self.total_expression + " \t"*3 + self.current_expression +'\n\n')
        self.history.config(state = NORMAL)
        self.history.insert(INSERT, self.actualHistoryOperation.get())
        self.history.config(state = DISABLED)

    def add_ans(self):
        if self.current_expression == "":
            self.ans = '0'
        else:
            self.ans = self.current_expression[2::]

    def input_from_keyboard(self):
        self.calculator_std.bind('<Return>', lambda event: self.evaluate())
        self.calculator_std.bind('<BackSpace>', lambda event: self.backsapce())
        self.calculator_std.bind('<c>', lambda event: self.C())
        self.calculator_std.bind('<Delete>', lambda event: self.clear_all())
        self.calculator_std.bind('<Key>', lambda event: self.add_to_expression(event.char))


        
        btn_std = ['(',')','.',0,1,2,3,4,5,6,7,8,9]
        btn_opr = {"/":"\u00F7", "*":"\u00D7",
                   "-":'\u2212', '+':'\u002B'
        }

        for key in btn_std:
            self.calculator_std.bind(str(key), lambda event, digit = key: self.add_to_expression(digit))

        for key in btn_opr:
            self.calculator_std.bind(key, lambda event, operator = key: self.add_to_expression(operator))
        

    def run(self):
        self.calculator_std.mainloop()



CalStd = Standard_Calculator()
CalStd.run()