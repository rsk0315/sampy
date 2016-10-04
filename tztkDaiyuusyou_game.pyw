#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Tkinter
import tkMessageBox

class Cell(Tkinter.Button):
    def __init__(self, i, j, board=None, parent=None, **kwargs):
        if board is None and parent is None:
            return

        Tkinter.Button.__init__(
            self, parent,
            command=lambda: board.update_state(self, i, j),
            **kwargs
        )

class TicTacToe(Tkinter.Frame):
    def __init__(
            self, parent=None, height=3, width=3, length=3,
            markers=u'\u6deb\u5922'
    ):
        if parent is None:
            return

        # self.is_daiyuusyou_mode = u'True すぎて True になった！ｗ'
        # todo オプションから通常モードでも遊べるやうにする
        #     いまいちね～やる気がないんですよね
        #     やる気もないし～ちょっとめんどくさいしで，
        #     実装はここで終はらせていただきます
        # ^ ここいらない

        self.is_daiyuusyou_mode = Tkinter.BooleanVar(value=True)

        self.parent = parent
        self.height = height
        self.width = width
        self.length = length
        self.markers = markers

        self.new_game()

    def set_size(self, height, width, length):
        Tkinter.Frame.__init__(self, self.parent)
        self.height = height
        self.width = width
        self.length = length

        self.remains = width*height
        self.state = [[None for j in range(width)] for i in range(height)]
        for i in range(height):
            frame = Tkinter.Frame(self)
            for j in range(width):
                cell = Cell(i, j, self, frame, width=2, height=1)
                cell.pack(
                    expand=True,
                    anchor='w',
                    side='left',
                    fill='both',
                    padx=0,
                )

            frame.pack(expand=True, side='top', fill='both', pady=0)
            self.pack(expand=True, fill='both')

        self.combolabel = Tkinter.Label(self)
        self.combolabel.configure(
            text=u'0 {} <次の人   {} 0'.format(*self.markers)
        )
        self.combolabel.pack(fill='both', expand=True)

    def set_marker(self, markers):
        self.markers = markers
        self.cur_marker = markers[0]
        self.next_marker = markers[1]

    def update_state(self, cell, i, j):
        if self.state[i][j] is not None:
            return  # needs showinfo?

        if not self.remains:
            return

        self.state[i][j] = self.cur_marker
        cell.configure(text=self.cur_marker)
        self.remains -= 1

        if self.is_daiyuusyou_mode.get():
            self.update_combo(i, j)
            self.change_turn()
            if not self.remains:
                if self.height * self.width >= 100:
                    tkMessageBox.showinfo(
                        u'\u4e59\uff57\uff57\uff57\uff57\uff57',
                        u'\u6700\u5f8c\u307e\u3067'
                        u'\u904a\u3093\u3067\u304f\u308c\u3066'
                        u'\u3042\u308a\u304c\u3068\u30ca\u30b9\uff01'
                    )
                else:
                    tkMessageBox.showinfo(
                        u'\u4e59\u30f3\u30b4',
                        u'\u3053\u3093\u306a\u30b2\u30fc\u30e0\u3067\u6642'
                        u'\u9593\u3092\u7121\u99c4\u306b\u4f7f\u3063\u305f'
                        u'\u3089\u99c4\u76ee\u3060\u3067'
                    )

            return

        result = self.matched(i, j)
        if result == 1:
            self.show_result(
                u'\u300c{}\u300d\u306e\u52dd\u3061\uff5e\uff01\uff57'.format(
                    self.cur_marker
                )
            )
            self.remains = 0
        elif result == -1:
            self.show_result(
                u'\u6deb\u5922\u304f\u3093\u306e\u5b8c\u5168\u52dd\u5229\uff01'
                u'\uff01\uff01\uff01\u3000\uff35\uff23\uff01\uff01\uff01\uff01'
                u'\uff01\uff01\uff01\uff01'
            )

        self.change_turn()

    def matched(self, i, j):
        # for normal mode
        if not self.remains:
            return -1

        dr = zip((0, 1, 1, 1), (-1, -1, 0, 1))
        for di, dj in dr:
            cur = 1
            I, J = i, j
            for k in range(self.length):
                I += di
                J += dj  # dj dj... （届かぬ想ひ）
                if (not (0<=I<self.height and 0<=J<self.width)):
                    break

                if self.state[I][J] != self.cur_marker:
                    break

                cur += 1
                if cur >= self.length:
                    return True

            I, J = i, j
            for k in range(self.length):
                I -= di
                J -= dj
                if (not (0<=I<self.height and 0<=J<self.width)):
                    break

                if self.state[I][J] != self.cur_marker:
                    break

                cur += 1
                if cur >= self.length:
                    return True
        else:
            return False

    def update_combo(self, i, j):
        combo_diff = 0
        dir8 = zip(
            (-1, -1, -1, 0, 0, 1, 1, 1), (-1, 0, 1, -1, 1, -1, 0, 1)
        )
        for di, dj in dir8:
            combo_diff -= self.get_length(i, j, di, dj, False)

        dir4 = zip((0, 1, 1, 1), (-1, -1, 0, 1))
        for di, dj in dir4:
            combo_diff += self.get_length(i, j, di, dj, True)

        self.combo[self.cur_marker].set(
            self.combo[self.cur_marker].get() + combo_diff
        )

    def get_length(self, i, j, di, dj, bidirectional):
        length = 1 if bidirectional else 0
        #        ^~~~               ~~~~~~ ここいる？
        I, J = i+di, j+dj
        while (0<=I<self.height and 0<=J<self.width):
            if (self.state[I][J] != self.cur_marker):
                break

            I += di
            J += dj
            length += 1

        if not bidirectional:
            return length >= self.length

        I, J = i-di, j-dj
        while (0<=I<self.height and 0<=J<self.width):
            if (self.state[I][J] != self.cur_marker):
                break

            I -= di
            J -= dj
            length += 1

        return length >= self.length

    def show_result(self, text):
        tkMessageBox.showinfo(u'結果', text)

    def change_turn(self):
        self.cur_marker, self.next_marker = self.next_marker, self.cur_marker
        self.combolabel.configure(
            text=u'{} {} {} {} {}'.format(
                self.combo[self.markers[0]].get(),
                self.markers[0],
                u'<次の人  '
                    if self.cur_marker == self.markers[0]
                    else u'  次の人>',

                self.markers[1],
                self.combo[self.markers[1]].get(),
            )
        )

    def option(self):
        root = Tkinter.Toplevel()
        root.title(u'設定')

        wframe = Tkinter.Frame(root)
        self.w = w = Tkinter.IntVar(value=self.width)
        wsbox = Tkinter.Spinbox(
            wframe,
            from_=3, to=19, increment=1, textvariable=w, width=8,
        )
        wsbox.bind('<Return>', lambda e: self.validate(root))
        wsbox.pack(side='right')
        Tkinter.Label(wframe, text=u'幅：').pack(side='right')
        wframe.pack(fill='x')

        hframe = Tkinter.Frame(root)
        self.h = h = Tkinter.IntVar(value=self.height)
        hsbox = Tkinter.Spinbox(
            hframe,
            from_=3, to=19, increment=1, textvariable=h, width=8,
        )
        hsbox.bind('<Return>', lambda e: self.validate(root))
        hsbox.pack(side='right')
        Tkinter.Label(hframe, text=u'高さ：').pack(side='right')
        hframe.pack(fill='x')

        lframe = Tkinter.Frame(root)
        self.l = l = Tkinter.IntVar(value=self.length)
        lsbox = Tkinter.Spinbox(
            lframe,
            from_=3, to=19, increment=1, textvariable=l, width=8,
        )
        lsbox.bind('<Return>', lambda e: self.validate(root))
        lsbox.pack(side='right')
        Tkinter.Label(lframe, text=u'繋げる長さ：').pack(side='right')
        lframe.pack(fill='x')

        Tkinter.Button(
            root,
            command=lambda: self.validate(root), text=u'決定'
        ).pack(side='bottom')

        Tkinter.Checkbutton(
            root,
            text=u'とっとこ大優勝モード', variable=self.is_daiyuusyou_mode,
        ).pack(side='bottom')

    def validate(self, option_window):
        h, w, l = self.h.get(), self.w.get(), self.l.get()
        if l > max(h, w):
            tkMessageBox.showwarning(
                u'\u8b66\u544a\uff1a0\u70b9\u30fb\u30fb\u30fb',
                u'\u305f\u3076\u3093\u30af\u30ea\u30a2\u3067'
                u'\u304d\u306a\u3044\u3068\u601d\u3075\u3093'
                u'\u3067\u3059\u3051\u3069\uff08\u540d\u63a8\u7406\uff09',
            )
            option_window.focus_set()
        elif min(l, h, w) < 3:
            tkMessageBox.showwarning(
                u'\u8b66\u544a\uff1a0\u70b9\u30fb\u30fb\u30fb',
                u'\u3053\u3093\u306a\u3093\u3062\u3083\u30b2'
                u'\u30fc\u30e0\u306b\u306a\u3093\u306a\u3044'
                u'\u3093\u3060\u3088\uff08\u68d2\u8aad\u307f\uff09',
            )
            option_window.focus_set()
        else:
            self.set_size(h, w, l)
            if (self.is_daiyuusyou_mode.get() and h*w<100):
                tkMessageBox.showinfo(
                    u'\u3042\u3063\u3055\u3046\u3060\uff08\u5510\u7a81\uff09',
                    u'\u5927\u512a\u52dd\u30e2\u30fc'
                    u'\u30c9\u306f\u3082\u3063\u3068\u5927\u304d\u3044\u76e4'
                    u'\u3067\u904a\u3093\u3067\u307b\u3057\u3044\u3051\u3069'
                    u'\u306a\uff5e\u4ffa\u3082\u306a\uff5e'
                )

            option_window.grab_release()
            option_window.withdraw()

    def new_game(self):
        self.set_size(self.height, self.width, self.length)
        self.set_marker(self.markers)

        self.combo = {
            self.markers[0]: Tkinter.IntVar(value=0),
            self.markers[1]: Tkinter.IntVar(value=0),
        }


def main():
    root = Tkinter.Tk()
    root.title(u'淫夢くんゲーム')
    board = TicTacToe(root, 19, 19, 5)

    mroot = Tkinter.Menu(root)
    root.configure(menu=mroot)

    mgame = Tkinter.Menu(mroot, tearoff=False)
    mroot.add_cascade(label='Game', menu=mgame, underline=0)

    mgame.add_command(label='New Game', under=0, command=board.new_game)
    mgame.add_command(label='Options', under=0, command=board.option)

    root.mainloop()

if __name__ == '__main__':
    main()
