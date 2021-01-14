"""
Application:  Character Frequency Counter (Tkinter version)
Author:  BSFEMA
Note:  I would appreciate it if you kept my attribution as the original author in any fork or remix that is made.
"""


from tkinter import *


# Global variables
cbs = dict()
root = Tk()
top_frame = Frame(root)
button_frame = Frame(root)
bottom_frame = Frame(root)
counts = dict()
t1 = ""
t2 = ""
total_count = 0
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
# This is the Base64 of the "character_frequency_counter.svg" file after being converted svg->png->gif. (freeonlinetools24.com/base64-image)
# The tk.PhotoImage function only supports GIF and PGM/PPM filetypes...
favicon = "R0lGODlhYABgAIcAMQQCBBRehHQmBAQqPDwSBAQWJKw6BByKxCQKBByi5Aw+VMxGBJQyBFweBBQGBAQiLAQOFIQuBEwaBLxCBByW1CSu9AxK" \
          "ZAwCBBR+tAw6VDQSBNxKBAwyREQaBCwSBKQ6BGwmBAQmPBye5AQGBBRijHwqBAwqPEQWBAQeLLQ+BCwOBByq9AxCXNRKBJw2BGQiBBwKBAQm" \
          "NIwuBMRCBBya3CSy/AxObBRejHQqBDwWBAQaJKw+BByOzCQOBBym7Aw+XMxKBJQ2BFwiBBQKBAQiNFQeBByW3CSu/AxKbAwGBByCvNxOBAQG" \
          "DAwuRIwyBMRGBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACwAAAAAYABgAAcI/gABCBxIsKDBgwgTKlzIsKHD" \
          "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"


def create_array():
    global counts
    counts.clear()
    for i in range(0, 257):
        counts[i] = 0


def print_frequencies_original():
    global t2
    global total_count
    t2_temp = "Dec\tHex\tChar\tFrequency\n"
    t2_temp = t2_temp + "---\t---\t------\t---------\n"
    for i in range(0, 257):
        if counts[i] > 0:
            hex_char = str(hex(i).split('x')[-1]).upper()
            if i < 32:
                t2_temp = t2_temp + str(i) + "\t" + str(hex_char) + "\t" + first_31[i] + "\t" + str(counts[i]) + "\n"
            elif (i > 31) and (i < 128):
                t2_temp = t2_temp + str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n"
            elif (i > 127) and (i < 256):
                t2_temp = t2_temp + str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n"
            else:
                t2_temp = t2_temp + "Unicode\tUnicode\tUnicode\t" + str(counts[i]) + "\n"
            total_count = total_count + counts[i]
    root.title("Character Frequency Counter - Total Count = " + str(total_count))
    t2.delete('1.0', END)
    t2.insert(END, t2_temp)


def print_frequencies():
    global t2
    global total_count
    t2.tag_config("a_on",  background="#ffffff", foreground="#000000")
    t2.tag_config("a_off", background="#f5f5f5", foreground="#000000")
    t2.tag_config("e_on",  background="#dcdcff", foreground="#000000")
    t2.tag_config("e_off", background="#aaaaff", foreground="#000000")
    t2.tag_config("u_on",  background="#ffdcdc", foreground="#000000")
    t2.tag_config("u_off", background="#ffaaaa", foreground="#000000")
    t2.delete('1.0', END)
    t2.insert(END, "Dec\tHex\tChar\tFrequency\n", "a_on")
    t2.insert(END, "---\t---\t------\t---------\n", "a_off")
    zebra = True
    for i in range(0, 257):
        if counts[i] > 0:
            hex_char = str(hex(i).split('x')[-1]).upper()
            if i < 32:
                if zebra:
                    t2.insert(END, str(i) + "\t" + str(hex_char) + "\t" + first_31[i] + "\t" + str(counts[i]) + "\n", "a_on")
                    zebra = False
                else:
                    t2.insert(END, str(i) + "\t" + str(hex_char) + "\t" + first_31[i] + "\t" + str(counts[i]) + "\n", "a_off")
                    zebra = True
            elif (i > 31) and (i < 128):
                if zebra:
                    t2.insert(END, str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "a_on")
                    zebra = False
                else:
                    t2.insert(END, str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "a_off")
                    zebra = True
            elif (i > 127) and (i < 256):
                if zebra:
                    t2.insert(END, str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "e_on")
                    zebra = False
                else:
                    t2.insert(END, str(i) + "\t" + str(hex_char) + "\t" + chr(i) + "\t" + str(counts[i]) + "\n", "e_off")
                    zebra = True
            else:
                if zebra:
                    t2.insert(END, "Unicode\tUnicode\tUnicode\t" + str(counts[i]) + "\n", "u_on")
                    zebra = False
                else:
                    t2.insert(END, "Unicode\tUnicode\tUnicode\t" + str(counts[i]) + "\n", "u_off")
                    zebra = True
            total_count = total_count + counts[i]
    root.title("Character Frequency Counter - Total Count = " + str(total_count))


def count_frequencies():
    global root
    global t1
    global t2
    global total_count
    total_count = 0
    create_array()
    print("Count Frequencies function")
    t1_temp = t1.get('1.0', END)
    t1_temp = t1_temp.strip()
    for i in range(0, len(t1_temp)):
        char = t1_temp[i]
        num = ord(char)
        if (num > 0) and (num < 128):
            # print(char + " = Ascii")
            counts[num] = counts[num] + 1
        elif (num > 127) and (num < 256):
            # print(char + " = Extended Ascii")
            counts[num] = counts[num] + 1
        elif num > 255:
            # print(char + " = Unicode")
            counts[256] = counts[256] + 1
    print_frequencies()


def clear_input():
    print("Clear Input function")
    global t1
    t1.delete('1.0', END)
    t1.insert(END, "")


def highlight_input():
    global t1
    t1.tag_config("a_on",  background="#ffffff", foreground="#000000")
    t1.tag_config("a_off", background="#f5f5f5", foreground="#000000")
    t1.tag_config("e_on",  background="#dcdcff", foreground="#000000")
    t1.tag_config("e_off", background="#aaaaff", foreground="#000000")
    t1.tag_config("u_on",  background="#ffdcdc", foreground="#000000")
    t1.tag_config("u_off", background="#ffaaaa", foreground="#000000")
    t1_temp = t1.get('1.0', END)
    clear_input()
    # remove training newline
    if (t1_temp[len(t1_temp) - 1] == "\n"):
        t1_temp = t1_temp[0:len(t1_temp) - 1]
    for i in range(0, len(t1_temp)):
        char = t1_temp[i]
        num = ord(char)
        if (num >= 0) and (num < 128):
            t1.insert(END, str(char), "a_on")
        elif (num > 127) and (num < 256):
            t1.insert(END, str(char), "e_on")
        else:
            t1.insert(END, str(char), "u_on")


def main():
    global t1
    global t2
    create_array()
    # Build GUI
    root.title("Character Frequency Counter")
    top_frame.pack(side=TOP)
    button_frame.pack(side=TOP)
    bottom_frame.pack(side=BOTTOM)
    # Top Frame
    s1 = Scrollbar(top_frame)
    t1 = Text(top_frame, height=10, width=80)
    s1.pack(side=RIGHT, fill=Y)
    t1.pack(side=LEFT, fill=Y)
    s1.config(command=t1.yview)
    t1.config(yscrollcommand=s1.set)
    # Button Frame
    b_convert = Button(button_frame, text="Count Frequencies", fg="red", padx=20, command=count_frequencies)
    b_convert.pack(side=LEFT)
    b_highlight = Button(button_frame, text="Highlight Non-ASCII", fg="red", padx=20, command=highlight_input)
    b_highlight.pack(side=LEFT)
    b_clear = Button(button_frame, text="Clear Input", fg="red", padx=20, command=clear_input)
    b_clear.pack(side=LEFT)
    b_exit = Button(button_frame, text="Exit", fg="red", padx=20, command=root.destroy)
    b_exit.pack(side=LEFT)
    # Bottom Frame
    s2 = Scrollbar(bottom_frame)
    t2 = Text(bottom_frame, height=40, width=80)
    s2.pack(side=RIGHT, fill=Y)
    t2.pack(side=LEFT, fill=Y)
    s2.config(command=t2.yview)
    t2.config(yscrollcommand=s2.set)
    t2.insert(END, "")
    # Run GUI
    img = PhotoImage(data=favicon)
    root.call('wm', 'iconphoto', root._w, img)
    root.resizable(False, False)
    root.mainloop()


if __name__ == "__main__":
    main()