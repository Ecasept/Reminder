#!/usr/bin/env python3

import logging
from gi import require_version

require_version("Notify", "0.7")
require_version("Gtk", "3.0")

from gi.repository import Gtk, Notify

global reminder_engine, window, logger

logger = logging.getLogger("MainLogger")
logger.setLevel(logging.DEBUG)  # Set to Warning for real execution


class Reminder:
    TYPE_NOTIFICATION = 0
    TYPE_DIALOG = 1
    TYPE_VIDEO = 2
    TYPE_LOCK = 3
    NOTIFICATION_TYPES = {
        "notification", TYPE_NOTIFICATION,
        "dialog", TYPE_DIALOG,
        "video", TYPE_VIDEO,
        "lock", TYPE_LOCK
    }

    def remind_notification(self, title, message):
        notification = Notify.Notification.new(title, message)
        notification.show()

    def remind(self, title, message, type_):
        window.reload()
        if type_ == Reminder.TYPE_NOTIFICATION:
            self.remind_notification(title, message)


reminders = [
    {"name": "Rausgehen", "type": Reminder.TYPE_NOTIFICATION, "content": "Geh Raus jetzt!!!", "index": 0},
    {"name": "Programmieren", "type": Reminder.TYPE_NOTIFICATION, "content": "Programmiere was tolles", "index": 1},
    {"name": "Brainstorming", "type": Reminder.TYPE_NOTIFICATION, "content": "Ich brauche ideen", "index": 2}
]

Notify.init("reminder")


def add_not_implemented(widget):
    Notify.Notification.new("Not Implemented", "Adding Reminders hasn't been implemented yet...").show()


class MainWindow(Gtk.Window):
    def reload(self):
        logger.debug("Reloading Window")
        self.win.destroy()
        self.add_widgets()
        self.win.show_all()

    def get_current_index(self) -> int:
        return self.index

    def destroy_add_reminder_window(self, widget, event):
        self.add_reminder_window.destroy()

    """Save a reminder. Be careful and always get the index using get_current_index()!"""

    def save_reminder(self, name: str, type_: int, content: str, index: int):
        reminders.append({"name": name, "type": type_, "content": content, "index": index})
        logger.debug("Saved Reminder")
        self.reload()

    def add_reminder(self, name: str, type_: int, content: str):
        self.save_reminder(name, type_, content, self.index)
        self.index += 1

    def add_reminder_from_button(self, widget):
        info = self.prompt_reminder_info()
        if info[0] != Gtk.ResponseType.OK:
            return
        self.add_reminder(
            info[1],  # Name
            Reminder.TYPE_NOTIFICATION,  # Type (info[2])
            info[2],  # Content (info[3])
        )
        # TODO: Implement save_reminder and use add_reminder

    def prompt_reminder_info(self):
        dialog = AddReminderWindow(self)
        response = dialog.run()
        dialog.destroy()
        return response

    def notification(self, widget):
        Notify.Notification.new("Test", "test2").show()

    def __init__(self):
        Gtk.Window.__init__(self, title="Reminders")  # Initialize Window
        self.add_widgets()
        self.index = 3  # TODO: 0

    def add_widgets(self):
        logger.debug("Adding Widgets...")
        self.win = Gtk.Grid()  # Grid so multiple items can fit in the window
        self.win.set_border_width(10)  # Set border so everything isn't right at the window edge
        self.listbox = Gtk.ListBox()  # Create new ListBox
        self.win.add(self.listbox)  # Add ListBox to Window
        for reminder in reminders:
            # Add a box with a label and a button to a box
            # This box is added to the listbox
            # Technically the box is added to a listboxrow which is added to the listbox
            reminder_box = Gtk.Box(spacing=10)
            reminder_label = Gtk.Label(reminder["name"])
            reminder_edit = Gtk.Button(label=u"\U0001F58A")
            reminder_edit.connect("clicked", self.remind_from_button)
            reminder_delete = Gtk.Button(label=u"\U0001F5D1")
            reminder_delete.connect("clicked", self.remind_from_button)  # execute remind_from_button when clicked
            reminder_box.add(reminder_label)
            reminder_box.add(reminder_edit)
            reminder_box.add(reminder_delete)
            self.listbox.add(reminder_box)
        add_btn = Gtk.Button(label="+")
        add_btn.connect("clicked", self.add_reminder_from_button)
        self.win.add(add_btn)
        self.add(self.win)
        logger.debug("Added Widgets")

    def remind_from_button(self, widget):
        # Widget should be the button
        listboxrow = widget.get_parent().get_parent()  # Parent of button is a box; parent of the box is the listboxrow
        index = self.listbox.get_children().index(listboxrow)  # Get the index of the reminder in the reminders
        entries = [x for x in reminders if x["index"] == index]  # get all the info by only getting the items from the
        # reminders dict where the index is the same
        if len(entries) > 1:
            logger.info(str(len(entries)) + " entries found; Defaulting to the first one")
        if len(entries) < 1:
            logger.warning("No entry found")
            return
        entry = entries[0]  # Always take first entry in case of multiple (shouldn't happen)
        reminder_engine.remind(entry["name"], entry["content"], entry["type"])


class AddReminderWindow(Gtk.Dialog):
    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Add Reminder", parent, Gtk.DialogFlags.MODAL, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        ))  # Initialize Window

        win = self.get_content_area()
        grid = Gtk.Grid(column_spacing=10, row_spacing=10)  # Grid so multiple items can fit in the window
        self.name_entry = Gtk.Entry()
        self.name_label = Gtk.Label("Name")
        self.content_label = Gtk.Label("Description")
        self.content_entry = Gtk.Entry()
        grid.add(self.name_label)
        grid.attach(self.name_entry, 1, 0, 1, 1)
        grid.attach(self.content_label, 0, 1, 1, 1)
        grid.attach(self.content_entry, 1, 1, 1, 1)
        for notification_type in reminder_engine.NOTIFICATION_TYPES:
            pass
        win.set_border_width(10)
        win.add(grid)
        self.show_all()

    def run(self):
        modified_response = []
        response = super(AddReminderWindow, self).run()
        modified_response.append(response)
        if response == Gtk.ResponseType.OK:
            modified_response.append(self.name_entry.get_text())
            modified_response.append(self.content_entry.get_text())
        return modified_response


def start():
    global reminder_engine, window
    reminder_engine = Reminder()
    window = MainWindow()
    window.connect("delete-event", Gtk.main_quit)
    window.show_all()
    Gtk.main()
