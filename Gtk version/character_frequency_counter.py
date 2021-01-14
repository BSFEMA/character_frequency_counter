"""
Application:  Character Frequency Counter (Gtk version)
Author:  BSFEMA
Note:  I would appreciate it if you kept my attribution as the original author in any fork or remix that is made.
"""


import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import Gdk as gdk
import os
import sys


counts = dict()
first_31 = {
    0: "<NULL>",
    1: "<SOH>",
    2: "<STX>",
    3: "<ETX>",
    4: "<EOT>",
    5: "<ENQ>",
    6: "<ACK>",
    7: "<BEL>",
    8: "<BS>",
    9: "<HT>",
    10: "<LF>",
    11: "<CT>",
    12: "<FF>",
    13: "<CR>",
    14: "<SO>",
    15: "<SI>",
    16: "<DLE>",
    17: "<DC1>",
    18: "<DC2>",
    19: "<DC3>",
    20: "<DC4>",
    21: "<NAK>",
    22: "<SYN>",
    23: "<ETB>",
    24: "<CAN>",
    25: "<EM>",
    26: "<SUB>",
    27: "<ESC>",
    28: "<FS>",
    29: "<GS>",
    30: "<RS>",
    31: "<US>"
}


class Main():
    def __init__(self):
        # Setup Glade Gtk
        self.builder = gtk.Builder()
        self.builder.add_from_file(os.path.join(sys.path[0], "character_frequency_counter.glade"))  # Looking where the python script is located
        self.builder.connect_signals(self)
        # Get UI components
        window = self.builder.get_object("main_window")
        window.connect("delete-event", gtk.main_quit)
        window.set_title('Character Frequency Counter')
        window.set_default_icon_from_file(os.path.join(sys.path[0], "character_frequency_counter.svg"))  # Setting the "default" icon makes it usable in the about dialog. (This will take .ico, .png, and .svg images.)
        window.show()
        # This allows the use css styling
        provider = gtk.CssProvider()
        provider.load_from_path(os.path.join(sys.path[0], "character_frequency_counter.css"))  # Looking where the python script is located
        gtk.StyleContext().add_provider_for_screen(gdk.Screen.get_default(), provider, gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        # textview_Input stuff
        textview_Input = self.builder.get_object("textview_Input")
        textview_Input.set_size_request(300, 600)
        self.textbuffer_input = textview_Input.get_buffer()
        tag_a_on = self.textbuffer_input.create_tag("a_on", background="#ffffff", foreground="#000000")
        tag_e_on = self.textbuffer_input.create_tag("e_on", background="#dcdcff", foreground="#000000")
        tag_u_on = self.textbuffer_input.create_tag("u_on", background="#ffdcdc", foreground="#000000")
        # textview_Output stuff
        textview_Output = self.builder.get_object("textview_Output")
        self.textbuffer_output = textview_Output.get_buffer()
        tag_a_on = self.textbuffer_output.create_tag("a_on", background="#ffffff", foreground="#000000")
        tag_a_off = self.textbuffer_output.create_tag("a_off", background="#d5d5d5", foreground="#000000")
        tag_e_on = self.textbuffer_output.create_tag("e_on", background="#dcdcff", foreground="#000000")
        tag_e_off = self.textbuffer_output.create_tag("e_off", background="#aaaaff", foreground="#000000")
        tag_u_on = self.textbuffer_output.create_tag("u_on", background="#ffdcdc", foreground="#000000")
        tag_u_off = self.textbuffer_output.create_tag("u_off", background="#ffaaaa", foreground="#000000")
        """
        # Debug:  add all ascii (except null), extended ascii, and 1 unicode character
        ascii = ""
        for i in range(1, 257):
            ascii = ascii + chr(i)
        self.textbuffer_input.set_text(ascii)
        """

    """ ************************************************************************************************************ """
    #  These are the various widget's signal handler functions:  UI elements other than buttons & dialogs
    """ ************************************************************************************************************ """

    def button_Exit_clicked(self, widget):
        # button_Exit = self.builder.get_object("button_Exit")
        gtk.main_quit()

    def button_Clear_Input_clicked(self, widget):
        # button_Clear_Input = self.builder.get_object("button_Clear_Input")
        self.textbuffer_input.set_text("")

    def button_Highlight_clicked(self, widget):
        # button_Highlight = self.builder.get_object("button_Highlight")
        textview_Input = self.builder.get_object("textview_Input")
        textbuffer = textview_Input.get_buffer()
        # Get the current input text:
        text = textbuffer.get_text(textbuffer.get_start_iter(), textbuffer.get_end_iter(), False)
        # Clear the input text
        self.button_Clear_Input_clicked(self)
        # Put the input text back, but with tags
        for i in range(0, len(text)):
            char = text[i]
            num = ord(char)
            if (num >= 0) and (num < 128):
                self.textbuffer_input.insert_with_tags_by_name(self.textbuffer_input.get_end_iter(), char, "a_on")
            elif (num > 127) and (num < 256):
                self.textbuffer_input.insert_with_tags_by_name(self.textbuffer_input.get_end_iter(), char, "e_on")
            else:
                self.textbuffer_input.insert_with_tags_by_name(self.textbuffer_input.get_end_iter(), char, "u_on")

    def button_Count_Frequencies_clicked(self, widget):
        # button_Count = self.builder.get_object("button_Count")
        textview_Input = self.builder.get_object("textview_Input")
        textbuffer = textview_Input.get_buffer()
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        text = textbuffer.get_text(start_iter, end_iter, False)
        create_array()
        for i in range(0, len(text)):
            char = text[i]
            num = ord(char)
            if (num > 0) and (num < 128):
                # print(char + " = ASCII")
                counts[num] = counts[num] + 1
            elif (num > 127) and (num < 256):
                # print(char + " = Extended ASCII")
                counts[num] = counts[num] + 1
            elif num > 255:
                # print(char + " = Unicode")
                counts[256] = counts[256] + 1
        self.print_frequencies(self)

    """ ************************************************************************************************************ """
    # These are the various class functions
    """ ************************************************************************************************************ """

    def print_frequencies(self, widget):
        total_count = 0
        textview_Output = self.builder.get_object("textview_Output")
        self.textbuffer_output = textview_Output.get_buffer()
        self.textbuffer_output.set_text("")
        zebra = True
        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), "Dec\tHex\tChar\tFrequency\n", "a_on")
        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), "---\t---\t------\t---------\n", "a_off")
        for i in range(0, 257):
            if counts[i] > 0:
                hex_char = str(hex(i).split('x')[-1]).upper()
                if i < 32:
                    if zebra:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), str(i) + "\t" + str(hex_char) + "\t" + first_31[i] + "\t" + str(counts[i]) + "\n", "a_on")
                        zebra = False
                    else:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), str(i) + "\t" + str(hex_char) + "\t" + first_31[i] + "\t" + str(counts[i]) + "\n", "a_off")
                        zebra = True
                elif (i > 31) and (i < 128):
                    if zebra:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "a_on")
                        zebra = False
                    else:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "a_off")
                        zebra = True
                elif (i > 127) and (i < 256):
                    if zebra:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "e_on")
                        zebra = False
                    else:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "e_off")
                        zebra = True
                else:
                    if zebra:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), "Unicode\tUnicode\tUnicode\t" + str(counts[i]) + "\n", "u_on")
                        zebra = False
                    else:
                        self.textbuffer_output.insert_with_tags_by_name(self.textbuffer_output.get_end_iter(), "Unicode\tUnicode\tUnicode\t" + str(counts[i]) + "\n", "u_off")
                        zebra = True
                total_count = total_count + counts[i]
        window = self.builder.get_object("main_window")
        if total_count == 0:
            window.set_title('Character Frequency Counter')
        else:
            window.set_title('Character Frequency Counter - Total Count = ' + str(total_count))

""" **************************************************************************************************************** """
# "class Main()" ends here...
# Beyond here lay functions...
""" **************************************************************************************************************** """


def create_array():
    global counts
    counts.clear()
    for i in range(0, 257):
        counts[i] = 0


if __name__ == '__main__':
    create_array()
    main = Main()
    gtk.main()
