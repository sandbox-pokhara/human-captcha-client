import tkinter as tk
from typing import Any

from PIL import ImageTk

from human_captcha_client.utils import b64_to_tk


class BboxSolver(tk.Tk):
    def __init__(self, data: dict[str, Any]) -> None:
        super().__init__()
        self.data = data
        self.title("Captcha")
        self.solution: list[int] = []
        self.stop = False

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
                image=photo,  # type: ignore
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

        # BBOX
        self.image_frame: tk.Frame = tk.Frame()
        self.image_frame.pack()

        # Load the image and display it
        img: str = self.data["captcha_obj"]["sample_images"][0]
        self.photo = b64_to_tk(img)
        self.canvas: tk.Canvas = tk.Canvas(
            self.image_frame,
            width=self.photo.width(),
            height=self.photo.height(),
        )

        self.canvas.create_image(  # type:ignore
            0, 0, anchor=tk.NW, image=self.photo
        )
        self.canvas.pack()

        # Store marked points as (x, y) coordinates
        self.marked_points: list[tuple[int, int]] = []

        # Bind click event to canvas to mark points
        self.canvas.bind("<Button-1>", self.mark_point)

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

        self.clear_button: tk.Button = tk.Button(
            self.button_frame,
            text="Clear",
            command=self.clear_points,
        )
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Hotkeys
        self.bind("<Return>", lambda e: self.submit())
        self.bind("<Escape>", lambda e: self.skip())

    def mark_point(self, event: Any) -> None:
        """Mark a point where the user clicks on the canvas."""
        x, y = event.x, event.y
        self.marked_points.append((x, y))
        # Draw a small circle at the clicked location
        self.canvas.create_oval(
            x - 5, y - 5, x + 5, y + 5, outline="red", fill="red"
        )

    def clear_points(self) -> None:
        """Clear all marked points from the canvas."""
        self.marked_points.clear()
        self.canvas.delete("all")
        self.canvas.create_image(  # type:ignore
            0, 0, anchor=tk.NW, image=self.photo
        )

    def submit(self) -> None:
        self.solution.clear()
        for x, y in self.marked_points:
            self.solution.append(x)
            self.solution.append(y)
        self.destroy()

    def skip(self) -> None:
        self.destroy()

    def submit_and_stop(self) -> None:
        self.stop = True
        self.submit()

    def skip_and_stop(self) -> None:
        self.stop = True
        self.skip()
