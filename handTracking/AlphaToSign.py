# from tkinter import Tk, Label, Button, Canvas, PhotoImage, Frame
# from tkinter.font import Font

# class AlphaToSign:
#     def __init__(self):
#         self.window = Tk()
#         self.window.title("Sign Language Translator")
#         self.window.geometry("600x700")
#         self.window.config(bg="#f0f2f5")
#         self.window.resizable(False, False)

#         # Custom Fonts
#         title_font = Font(family="Helvetica", size=18, weight="bold")
#         button_font = Font(family="Arial", size=12, weight="bold")

#         # Main Frame
#         main_frame = Frame(self.window, bg="#f0f2f5", padx=20, pady=20)
#         main_frame.pack(expand=True, fill="both")

#         # Title
#         Label(
#             main_frame,
#             text="Alphabet to Sign Language",
#             font=title_font,
#             fg="#2c3e50",
#             bg="#f0f2f5"
#         ).grid(row=0, column=0, columnspan=5, pady=(0, 20))

#         # Image Canvas
#         self.canvas = Canvas(
#             main_frame,
#             height=250,
#             width=250,
#             bg="#ffffff",
#             highlightthickness=2,
#             highlightbackground="#3498db"
#         )
#         self.canvas.grid(row=1, column=0, columnspan=5, pady=20)

#         # Load default image
#         try:
#             self.logo_img = PhotoImage(file="handTracking/Sign/image.png")
#             self.backgroundPic = self.canvas.create_image(125, 125, image=self.logo_img)
#         except:
#             # Fallback if image not found
#             self.canvas.create_text(125, 125, text="Sign Image", font=button_font)

#         # Button Grid
#         letters = [
#             ['A', 'B', 'C', 'D', 'E'],
#             ['F', 'G', 'H', 'I', 'J'],
#             ['K', 'L', 'M', 'N', 'O'],
#             ['P', 'Q', 'R', 'S', 'T'],
#             ['U', 'V', 'W', 'X', 'Y'],
#             ['Z', '', '', 'Clear', '']
#         ]

#         # Create buttons in a loop
#         self.buttons = {}
#         for row_idx, row in enumerate(letters, start=2):
#             for col_idx, letter in enumerate(row):
#                 if letter:
#                     btn = Button(
#                         main_frame,
#                         text=letter,
#                         font=button_font,
#                         width=4,
#                         bg="#3498db" if letter == "Clear" else "#2c3e50",
#                         fg="white",
#                         activebackground="#2980b9",
#                         activeforeground="white",
#                         relief="flat",
#                         command=lambda l=letter: self.show_sign(l.lower() if l != "Clear" else "clear")
#                     )
#                     btn.grid(row=row_idx, column=col_idx, padx=5, pady=5, sticky="nsew")
#                     self.buttons[letter] = btn

#         # Configure grid weights
#         for i in range(5):
#             main_frame.grid_columnconfigure(i, weight=1)
#         for i in range(8):
#             main_frame.grid_rowconfigure(i, weight=1)

#         self.window.mainloop()

#     def show_sign(self, letter):
#         if letter == "clear":
#             try:
#                 self.logo_img = PhotoImage(file=f"handTracking/Sign/{letter}.png")

#                 self.canvas.itemconfig(self.backgroundPic, image=self.logo_img)
#             except:
#                 self.canvas.delete("all")
#                 self.canvas.create_text(125, 125, text="Default Image", font=("Arial", 12))
#         else:
#             try:
#                 self.logo_img = PhotoImage(file=f"handTracking/Sign/{letter}.png")
#                 self.canvas.itemconfig(self.backgroundPic, image=self.logo_img)
#             except:
#                 self.canvas.delete("all")
#                 self.canvas.create_text(125, 125, text=f"Sign for {letter.upper()}", font=("Arial", 12))

# # Run the application
# if __name__ == "__main__":
#     app = AlphaToSign()