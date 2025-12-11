# from tkinter import Tk, Label, Button, Frame
# from tkinter.font import Font

# class EntryPopUp:
#     def __init__(self):
#         self.ans = ""
#         self.window = Tk()
#         self.window.title("Sign Language Converter")
#         self.window.geometry("400x250")
#         self.window.config(bg="#f0f2f5")
#         self.window.resizable(False, False)

#         # Custom Fonts
#         title_font = Font(family="Helvetica", size=16, weight="bold")
#         button_font = Font(family="Arial", size=12, weight="bold")

#         # Main Frame (for better padding)
#         main_frame = Frame(self.window, bg="#f0f2f5", padx=20, pady=20)
#         main_frame.pack(expand=True, fill="both")

#         # Title Label
#         Label(
#             main_frame,
#             text="Choose Conversion Mode",
#             font=title_font,
#             fg="#2c3e50",
#             bg="#f0f2f5"
#         ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

#         # Buttons with better styling
#         Button(
#             main_frame,
#             text="Sign to Alphabet",
#             font=button_font,
#             bg="#3498db",
#             fg="white",
#             activebackground="#2980b9",
#             activeforeground="white",
#             relief="flat",
#             padx=20,
#             pady=10,
#             command=self.cam
#         ).grid(row=1, column=0, padx=10, pady=10, sticky="ew")

#         Button(
#             main_frame,
#             text="Alphabet to Sign",
#             font=button_font,
#             bg="#2ecc71",
#             fg="white",
#             activebackground="#27ae60",
#             activeforeground="white",
#             relief="flat",
#             padx=20,
#             pady=10,
#             command=self.ui
#         ).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

#         # Configure grid weights for responsiveness
#         main_frame.grid_columnconfigure(0, weight=1)
#         main_frame.grid_columnconfigure(1, weight=1)

#         self.window.mainloop()

#     def cam(self):
#         self.ans = "cam"
#         self.window.destroy()

#     def ui(self):
#         self.ans = "ui"
#         self.window.destroy()

#     def getAns(self):
#         return self.ans

# # Example usage
# if __name__ == "__main__":
#     app = EntryPopUp()