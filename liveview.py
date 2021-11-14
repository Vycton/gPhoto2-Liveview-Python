import sys
from io import BytesIO
from threading import Thread
from queue import Queue
import tkinter as tk
from PIL import Image, ImageTk

JPEG_START_CODE = b'\xff\xd8'
JPEG_END_CODE = b'\xff\xd9'


class FrameReader():
    """
    Object that reads jpegs from an mjpeg input stream, puts them in a queue
    and then displays them on a tk panel. Will not stop until the input does.
    """

    def __init__(self, panel, instream):
        self.panel = panel
        self.instream = instream
        self.framecount = 0
        self.frame_queue = Queue()
        self._started = False

    def start_threads(self):
        """
        Starts one thread to read input frames from the stream, and one to
        update the panel with those frames.
        """
        if self._started:
            return

        thread_frames = Thread(target=self.read_jpegs, args=())
        thread_frames.daemon = True
        thread_image = Thread(target=self.update_image, args=())
        thread_image.daemon = True

        thread_frames.start()
        thread_image.start()

        self._started = True

    def read_jpegs(self):
        """
        For as long as there is input, reads jpegs and adds them to the queue.
        """
        frame = self.read_jpeg()
        while frame:
            frame = self.read_jpeg()
            self.frame_queue.put(frame)

        self.frame_queue.put(None)  # signal end of frames

    def read_jpeg(self):
        """
        Reads a single jpeg from the stream.
        Adapted from https://github.com/aqiank/gphoto2-liveview-example/blob/master/main.c
        """
        frame_buffer = bytearray(JPEG_START_CODE)

        # Discard data until the start of a frame
        code = self.instream.read(2)
        while code and code != JPEG_START_CODE:
            code = self.instream.read(2)

        while code != JPEG_END_CODE:
            code = self.instream.read(2)
            frame_buffer += code
            if not code:
                # Stream has been cut off
                return None  # Signal end
        return BytesIO(frame_buffer)

    def update_image(self):
        """
        Continually takes frames from the queue, and adds them to the
        given panel.
        """
        frame = self.frame_queue.get()
        while frame:
            img = Image.open(frame)
            img = ImageTk.PhotoImage(img)
            self.panel.configure(image=img)
            self.panel.image = img
            frame = self.frame_queue.get()


def main():
    """
    Creates a panel and starts the framereader
    """
    # For our purposes, this is where the mjpeg stream will come from
    instream = sys.stdin.buffer

    # Setup tk panel with corresponding reader
    root = tk.Tk()
    panel = tk.Label(root)
    reader = FrameReader(panel, instream)

    # Read a frame and pack the panel in order to have the right window dimensions
    frame = reader.read_jpeg()
    img = Image.open(frame)
    img = ImageTk.PhotoImage(img)
    panel.configure(image=img)
    panel.image = img
    panel.pack(side="bottom", fill="both", expand="yes")

    # Start the reader and tk's main loop
    reader.start_threads()
    tk.mainloop()


if __name__ == "__main__":
    main()

