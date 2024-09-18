import tkinter as tk
from typing import Any

from PIL import ImageTk

from human_captcha_client.utils import b64_to_tk


class GridSolver(tk.Tk):
    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__()
        self.data = data
        self.title("Captcha")
        self.solution: list[int] = []

        # Keep the references of PhotoImage to prevent garbage collection
        self.photos: list[ImageTk.PhotoImage] = []

        # Instruction
        self.instruction_label = tk.Label(
            text=self.data["captcha_obj"]["instruction"],
        )
        self.instruction_label.pack()

        # Example images
        self.example_image_frame = tk.Frame()
        self.example_image_frame.pack()
        for i, img in enumerate(self.data["captcha_obj"]["example_images"]):
            col = i % 3
            row = i // 3

            photo = b64_to_tk(img)
            self.photos.append(photo)
            btn: tk.Button = tk.Button(
                self.example_image_frame,
                image=photo,  # type:ignore
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

        # Grid images
        self.grid_image_frame = tk.Frame()
        self.grid_image_frame.pack()

        self.selected_images: list[int] = []
        self.image_buttons: list[tk.Button] = []

        # Create a 3x3 grid of images
        for i, img in enumerate(self.data["captcha_obj"]["sample_images"]):
            col = i % 3
            row = i // 3
            photo = b64_to_tk(img)
            self.photos.append(photo)

            btn: tk.Button = tk.Button(
                self.grid_image_frame,
                image=photo,  # type:ignore
                command=lambda i=row, j=col: self.toggle_image(i, j),
            )
            btn.grid(row=row, column=col, padx=10, pady=10)
            self.image_buttons.append(btn)

        # Buttons
        self.button_frame = tk.Frame()
        self.button_frame.pack(pady=20)

        self.submit_button: tk.Button = tk.Button(
            self.button_frame,
            text="Submit",
            command=self.submit,
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.skip_button: tk.Button = tk.Button(
            self.button_frame,
            text="Skip",
            command=self.skip,
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)

        self.submit_button: tk.Button = tk.Button(
            self.button_frame,
            text="Submit and Stop",
            command=self.submit_and_stop,
        )
        self.submit_button.pack(side=tk.LEFT, padx=5)

        self.skip_button: tk.Button = tk.Button(
            self.button_frame,
            text="Skip and Stop",
            command=self.skip_and_stop,
        )
        self.skip_button.pack(side=tk.LEFT, padx=5)

        # hotkeys
        self.bind("<Return>", lambda e: self.submit())
        self.bind("<Escape>", lambda e: self.skip())

    def toggle_image(self, i: int, j: int) -> None:
        """Toggle the selection of an image in the grid."""
        index: int = i * 3 + j
        if index in self.selected_images:
            self.selected_images.remove(index)
            self.image_buttons[index].config(relief="raised")
        else:
            self.selected_images.append(index)
            self.image_buttons[index].config(relief="sunken")

    def submit(self) -> None:
        self.solution = self.selected_images
        self.destroy()

    def skip(self) -> None:
        self.destroy()

    def submit_and_stop(self) -> None:
        self.stop = True
        self.submit()

    def skip_and_stop(self) -> None:
        self.stop = True
        self.skip()
