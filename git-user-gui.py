#!/usr/bin/env python3

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

import argparse
import json
import logging
import os
import subprocess
import tkinter as tk
import tkinter.simpledialog


class MyDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title):
        self.e1 = None
        self.e2 = None
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Name:").grid(row=0)
        tk.Label(master, text="EMail:").grid(row=1)

        self.e1 = tk.Entry(master, width=40)
        self.e2 = tk.Entry(master, width=40)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def apply(self):
        first = self.e1.get()
        second = self.e2.get()
        self.result = first, second


class SortedUserInfoList(object):

    def __init__(self):
        self.users = []
        self.dirty = False

    @staticmethod
    def clean(s):
        return s.lower().strip()

    def add(self, name, email):
        e = {'name': name, 'email': email, 'l_name': self.clean(name), 'l_email': self.clean(email),
             'label': name + " <" + email + ">"}
        self.users.append(e)
        self.dirty = True
        self.sort()

    def is_dirty(self):
        return self.dirty

    def clear_dirty(self):
        self.dirty = False

    def find(self, name, email):
        lname = self.clean(name)
        lemail = self.clean(email)
        for i, e in enumerate(self.users):
            if (e['l_name'], e['l_email']) == (lname, lemail):
                return i
        return None

    def remove(self, index):
        del self.users[index]
        self.dirty = True

    def get(self, index):
        return self.users[index]

    def sort(self):
        self.users.sort(key=lambda e: e['l_name'])


class GitUserGui:
    def __init__(self, user_info_list, current, git_facade):
        self.user_info_list = user_info_list
        self.current = current
        self.git_facade = git_facade
        self.logger = logging.getLogger(type(self).__name__)

        self.rainbow = False

        self.root = root = tk.Tk()
        root.title('Global Git User Setter')
        root.wm_iconbitmap(default='Git-Logo-2Color.ico')
        left = tk.Frame(root, self.kwargs_with_color({}, "cornsilk"))
        left.pack(side=tk.LEFT, fill="both", expand=True)

        listbox_frame = tk.Frame(left, self.kwargs_with_color({}, "orange"))
        listbox_frame.pack(fill="both", expand=True)
        button_frame = tk.Frame(left, self.kwargs_with_color({"height": 30}, "red"))
        button_frame.pack(fill="both")

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill="y")

        self.listbox = lb = tk.Listbox(listbox_frame, selectmode=tk.SINGLE, width=60, height=8)
        lb.bind('<<ListboxSelect>>', self.listbox_select)
        lb.bind('<Double-1>', self.listbox_double_click)
        self.fill_listbox()
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

        field_width = 40

        tk.Label(select_details_frame, text="Name").grid(row=0, column=0, sticky="en")
        self.selNameVar = tk.StringVar()
        name = tk.Entry(select_details_frame, textvariable=self.selNameVar, state=tk.DISABLED, width=field_width)
        name.grid(row=0, column=1, sticky="en")

        tk.Label(select_details_frame, text="EMail").grid(row=5, column=0, sticky="en")
        self.selEmailVar = tk.StringVar()
        email = tk.Entry(select_details_frame, textvariable=self.selEmailVar, state=tk.DISABLED, width=field_width)
        email.grid(row=5, column=1, sticky="en")

        b = tk.Button(bframe, text='Set', command=self.set_git)
        b.pack(fill="none", expand=True)

        b = tk.Button(bframe, text='Clear', command=self.clear_git)
        b.pack(fill="none", expand=True)

        tk.Label(git_frame, text="Current Git Name").grid(row=20, column=0, sticky=tk.E+tk.S)
        self.gitNameVar = tk.StringVar()
        name = tk.Entry(git_frame, textvariable=self.gitNameVar, state=tk.DISABLED, width=field_width)
        name.grid(row=20, column=1, sticky=tk.E+tk.S)

        tk.Label(git_frame, text="Current Git EMail").grid(row=25, column=0, sticky=tk.E+tk.S)
        self.gitEmailVar = tk.StringVar()
        email = tk.Entry(git_frame, textvariable=self.gitEmailVar, state=tk.DISABLED, width=field_width)
        email.grid(row=25, column=1, sticky=tk.E+tk.S)

        if current is not None:
            self.gitNameVar.set(user_info_list.get(current).get("name", ""))
            self.gitEmailVar.set(user_info_list.get(current).get("email", ""))

        if len(user_info_list.users) > 0:
            # https://stackoverflow.com/questions/25415888/default-to-and-select-first-item-in-tkinter-listbox
            self.listbox.select_set(0 if current is None else current)  # This only sets focus on the first item.
            self.listbox.event_generate("<<ListboxSelect>>")

        # https://stackoverflow.com/questions/10448882/how-do-i-set-a-minimum-window-size-in-tkinter
        root.update()
        # now root.geometry() returns valid size/placement
        root.minsize(root.winfo_width(), root.winfo_height())

    def fill_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, entry in enumerate(self.user_info_list.users):
            self.listbox.insert(i+1, entry['label'])

    def kwargs_with_color(self, d, color):
        rv = dict(d)
        if self.rainbow:
            rv["background"] = color
        return rv

    def set_git(self):
        self.logger.info('set_git called')
        index = int(self.listbox.curselection()[0])
        entry = self.user_info_list.users[index]
        name = entry['name']
        email = entry['email']
        (new_name, new_email) = self.git_facade.set_name_and_email(name, email)
        self.update_git_name_and_email(new_name, new_email)

    def clear_git(self):
        self.logger.info('clear_git called')
        (new_name, new_email) = self.git_facade.clear_name_and_email()
        self.update_git_name_and_email(new_name, new_email)

    def update_git_name_and_email(self, name, email):
        self.gitNameVar.set(name)
        self.gitEmailVar.set(email)

    def update_selected_name_and_email(self, index=None):
        if index is None:
            self.selNameVar.set('')
            self.selEmailVar.set('')
        else:
            self.selNameVar.set(self.user_info_list.users[index].get('name', '???'))
            self.selEmailVar.set(self.user_info_list.users[index].get('email', '???'))

    def listbox_double_click(self, evt):
        w = evt.widget
        curselection = w.curselection()
        if len(curselection) == 0:
            # don't know if this can happen. don't think so.
            self.logger.info("listbox_double_click: nothing Selected")
        else:
            index = curselection[0]
            value = w.get(index)
            self.logger.info('listbox_double_click: selected item %d: "%s"', index, value)
            self.set_git()

    # https://stackoverflow.com/questions/6554805/getting-a-callback-when-a-tkinter-listbox-selection-is-changed
    def listbox_select(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        curselection = w.curselection()
        if len(curselection) == 0:
            # this happens when filling in the dialog box
            self.logger.info("listbox_select: nothing Selected")
            self.update_selected_name_and_email(index=None)
        else:
            index = curselection[0]
            value = w.get(index)
            self.logger.info('listbox_select: selected item %d: "%s"', index, value)
            self.update_selected_name_and_email(index=index)

    def plus_callback(self):
        d = MyDialog(self.root, 'Add name and email')
        self.logger.info("dialog result: %s", d.result)
        if d.result is not None:
            (name, email) = d.result
            name = name.strip()
            email = email.strip()
            self.user_info_list.add(name, email)
            self.fill_listbox()
            index = self.user_info_list.find(name, email)
            if index is None:
                raise Exception('Cannot find what I just added')
            self.listbox.select_set(index)  # This only sets focus on the first item.
            self.listbox.event_generate("<<ListboxSelect>>")

    def minus_callback(self):
        index = int(self.listbox.curselection()[0])
        e = self.user_info_list.users[index]
        answer = tkinter.messagebox.askyesno("Remove user", "Do you want to remove user {0}?".format(e['label']))
        if answer:
            self.user_info_list.remove(index)
            self.fill_listbox()
            if index >= len(self.user_info_list.users):
                index = len(self.user_info_list.users) - 1
            self.listbox.select_set(index)  # This only sets focus on the first item.
            self.listbox.event_generate("<<ListboxSelect>>")

    def go(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()


def default_json():
    return """[
 {
  "email": "dwegscheid@sbcglobal.net",
  "name": "Doug Wegscheid"
 },
 {
  "email": "DrewKelleher6@gmail.com",
  "name": "Drew Kelleher"
 },
 {
  "email": "15163@stjoebears.com",
  "name": "Liam Allen"
 }
]"""


class GitFacade:
    def __init__(self):
        # change this to "echo" for testing
        self.commands = ["git"]
        self.logger = logging.getLogger(type(self).__name__)

    def do_command(self, cmd, check=True):
        local_cmd = list(self.commands)
        local_cmd.extend(cmd)
        try:
            r = subprocess.run(local_cmd, check=check, stdout=subprocess.PIPE)
            self.logger.info("run %s returned %d", str(local_cmd), r.returncode)
            return r.stdout.decode()

        except subprocess.CalledProcessError:
            self.logger.exception("trouble running %s", str(local_cmd))
            return ""

    def get_name_and_email(self, check=False):
        name = self.do_command(['config', '--global', '--get', 'user.name'], check=check).strip()
        email = self.do_command(['config', '--global', '--get', 'user.email'], check=check).strip()
        self.logger.info('current name:%s email:%s', name, email)
        return name, email

    def set_name_and_email(self, name, email):
        self.logger.info("set_name_and_email: %s %s", name, email)
        self.do_command(['config', '--global', 'user.name', name])
        self.do_command(['config', '--global', 'user.email', email])
        return self.get_name_and_email(check=True)

    def clear_name_and_email(self):
        self.logger.info("clear_name_and_email")
        self.do_command(['config', '--global', '--unset', 'user.name'], check=False)
        self.do_command(['config', '--global', '--unset', 'user.email'], check=False)
        return self.get_name_and_email(check=False)


def do_gui(git_facade):
    name, email = git_facade.get_name_and_email(check=False)
    logging.info('current name:%s email:%s', name, email)

    home = os.path.expanduser("~")
    logging.info("home is %s", home)
    json_file_name = os.path.join(home, 'git-user-gui.json')
    json_tempfile_name = os.path.join(home, 'git-user-gui.tmp')  # type: str

    if os.path.exists(json_file_name):
        with open(json_file_name, 'r') as json_file:
            raw_data = json.load(json_file)
    else:
        logging.info("file %s does not exist, load defaults", json_file_name)
        raw_data = json.loads(default_json())

    users = SortedUserInfoList()
    for e in raw_data:
        users.add(e['name'], e['email'])

    users.clear_dirty()

    if name != "" or email != "":
        index = users.find(name, email)
        if index is None:
            users.add(name, email)
            index = users.find(name, email)
            if index is None:
                raise Exception('Cannot find what I just added')
    else:
        index = None

    gui = GitUserGui(users, index, git_facade)
    # g.set_current(name, email)
    gui.go()

    if users.dirty:
        out = []
        for u in users.users:
            e = {"name": u['name'], 'email': u['email']}
            out.append(e)

        if os.path.exists(json_tempfile_name):
            logging.info("removing %s", json_tempfile_name)
            os.remove(json_tempfile_name)

        with open(json_tempfile_name, 'w') as json_file:
            logging.info("writing %s", json_tempfile_name)
            json.dump(out, json_file, sort_keys=True, indent=1, separators=(',', ': '))

        if os.path.exists(json_file_name):
            logging.info("removing %s", json_file_name)
            os.remove(json_file_name)

        logging.info('renaming %s to %s', json_tempfile_name, json_file_name)
        os.rename(json_tempfile_name, json_file_name)


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description='set up global git user.name and user.email')
    parser.add_argument('--clear', action='store_true', help='clear the properties')
    args = parser.parse_args()

    git_facade = GitFacade()

    if args.clear:
        (name, email) = git_facade.clear_name_and_email()
        logging.info("should be clear: name=%s email=%s", name, email)
    else:
        do_gui(git_facade)


if __name__ == '__main__':
    main()
