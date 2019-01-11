#!/usr/bin/env python2

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import json, logging, subprocess

import Tkinter as tk
import tkMessageBox

class SortedUserInfoList(object):
    def __init__ (self):
        self.users = []
        
    def clean (self, s):
        return s.lower().strip()

    def add (self, name, email):
        e = { 'name': name, 'email': email, 'l_name': self.clean(name), 'l_email': self.clean(email),
              'label': name + " <" + email + ">"}
        self.users.append(e)
        self.sort()

    def find (self, name, email):
        lname = self.clean(name)
        lemail = self.clean(email)
        for i, e in enumerate(self.users):
            if (e['l_name'], e['l_email']) == (lname, lemail):
                return i
        return -1

    def sort(self):
        self.users.sort (key = lambda e: e['l_name'])

class GitUserGui(object):
    def __init__ (self, user_info_list, current, set_function, set_function_data):
        self.user_info_list = user_info_list
        self.current = current
        self.set_function = set_function
        self.set_function_data = set_function_data

        self.rainbow = False

        self.root = root = tk.Tk()
        root.title('Global Git User Setter')
        root.wm_iconbitmap(default='Git-Logo-2Color.ico')
        left = tk.Frame(root, self.kwargs_with_color({}, "cornsilk"))
        left.pack( side=tk.LEFT, fill="both", expand=True)

        listbox_frame = tk.Frame(left, self.kwargs_with_color({}, "orange"))
        listbox_frame.pack(fill="both", expand=True)
        button_frame = tk.Frame(left, self.kwargs_with_color({"height": 30}, "red"))
        button_frame.pack(fill="both")

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.listbox = lb = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, width=80, height=8)
        lb.bind('<<ListboxSelect>>', self.listbox_select)
        for i, entry in enumerate(self.user_info_list.users):
            lb.insert (i+1, entry['label'])
        lb.pack(fill="y", expand=True)

        # attach listbox to scrollbar
        lb.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=lb.yview)

        plus = tk.Button(button_frame, text='+', command=self.plus_callback)
        plus.pack(side=tk.LEFT)
        minus = tk.Button(button_frame, text='-', command=self.minus_callback)
        minus.pack(side=tk.LEFT)

        right = tk.Frame(root, self.kwargs_with_color({}, "bisque"))
        right.pack(side=tk.LEFT, fill="both", expand=True)

        select_details_frame = tk.Frame(right, self.kwargs_with_color({}, "red"))
        select_details_frame.pack(anchor="n", side="top", fill="x", expand=False)
        select_details_frame.grid_columnconfigure(0, weight=1)

        bframe = tk.Frame(right, self.kwargs_with_color({}, "green"))
        bframe.pack(fill="both", expand=True)

        git_frame = tk.Frame(right, self.kwargs_with_color({}, "blue"))
        git_frame.pack(anchor="s", side="bottom", fill="x", expand=False)
        git_frame.grid_columnconfigure(0, weight=1)

        field_width = 60

        tk.Label(select_details_frame, text="Name").grid(row=0, column=0, sticky="en")
        self.selNameVar = tk.StringVar()
        name = tk.Entry(select_details_frame, textvariable=self.selNameVar, state=tk.DISABLED, width=field_width)
        name.grid(row=0, column=1, sticky="en")

        tk.Label(select_details_frame, text="EMail").grid(row=5, column=0, sticky="en")
        self.selEmailVar = tk.StringVar()
        email= tk.Entry(select_details_frame, textvariable=self.selEmailVar, state=tk.DISABLED, width=field_width)
        email.grid(row=5, column=1, sticky="en")

        b = tk.Button(bframe, text='Set', command=self.set_git)
        b.pack(fill="none", expand=True)

        tk.Label(git_frame, text="Current Git Name").grid(row=20, column=0, sticky=tk.E+tk.S)
        self.gitNameVar = tk.StringVar()
        name = tk.Entry(git_frame, textvariable=self.gitNameVar, state=tk.DISABLED, width=field_width)
        name.grid(row=20, column=1, sticky=tk.E+tk.S)

        tk.Label(git_frame, text="Current Git EMail").grid(row=25, column=0, sticky=tk.E+tk.S)
        self.gitEmailVar = tk.StringVar()
        email= tk.Entry(git_frame, textvariable=self.gitEmailVar, state=tk.DISABLED, width=field_width)
        email.grid(row=25, column=1, sticky=tk.E+tk.S)

        if len(user_info_list.users) > 0:
            # https://stackoverflow.com/questions/25415888/default-to-and-select-first-item-in-tkinter-listbox
            self.listbox.select_set(current) #This only sets focus on the first item.
            self.listbox.event_generate("<<ListboxSelect>>")

        # https://stackoverflow.com/questions/10448882/how-do-i-set-a-minimum-window-size-in-tkinter
        root.update()
        # now root.geometry() returns valid size/placement
        root.minsize(root.winfo_width(), root.winfo_height())

    def kwargs_with_color (self, d, color):
        rv = dict(d)
        if self.rainbow:
            rv["background"] = color
        return rv

    def set_git(self):
        logging.info('setGit called')
        index = self.listbox.curselection()[0]
        self.set_function (self, self.set_function_data, self.user_info_list.users[index])

    def set_current(self, name, email):
        self.gitNameVar.set(name)
        self.gitEmailVar.set(email)

    def update_fields(self, index=None):
        if index is None:
            index = self.listbox.curselection()[0]
        self.selNameVar.set(self.user_info_list.users[index].get('name', '???'))
        self.selEmailVar.set(self.user_info_list.users[index].get('email', '???'))

    # https://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
    def listbox_select(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'You selected item %d: "%s"' % (index, value)
        self.update_fields(index=index)

    def plus_callback(self):
        tkMessageBox.showinfo( "Hello Python", "+")

    def minus_callback(self):
        tkMessageBox.showinfo( "Hello Python", "-")

    def go(self):
        self.update_fields()
        self.root.mainloop()

    def quit(self):
        self.root.quit()

def set_function(g, set_function_data, entry):
    logging.info ("set_function: %s %s", set_function_data, entry)
    git = set_function_data.get('git', 'echo')
    git_command(git, ['config', '--global', 'user.name', entry['name']])
    git_command(git, ['config', '--global', 'user.email', entry['email']])
    name = git_command(git, ['config', '--global', '--get', 'user.name']).strip()
    email = git_command(git, ['config', '--global', '--get', 'user.email']).strip()
    logging.info ('current name:%s email:%s', name, email)
    g.set_current(name, email)

def git_command(git, cmd):
    local_cmd = list(git)
    local_cmd.extend(cmd)
    rv = subprocess.check_output (local_cmd)
    return rv

def main():
    logging.basicConfig(level=logging.INFO)

    git = ['git']

    name = git_command(git, ['config', '--global', '--get', 'user.name']).strip()
    email = git_command(git, ['config', '--global', '--get', 'user.email']).strip()
    logging.info ('current name:%s email:%s', name, email)

    with open('git-user-gui.json', 'r') as json_file:
        raw_data = json.load (json_file)

    users = SortedUserInfoList()
    for e in raw_data:
        users.add (e['name'], e['email'])

    index = users.find (name, email)
    if index < 0:
        users.add (name, email)
        index = users.find (name, email)
        if index < 0:
            raise Exception ('Cannot find what I just added')

    set_function_data = { "git": git }
    g = GitUserGui(users, index, set_function, set_function_data)
    g.set_current(name, email)
    g.go()

if __name__ == '__main__':
    main()