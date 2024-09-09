import pyautogui as pg
import time

def multipleMeg(message, count, delay=10):
    """
    Send / write  multiple meg using pyautogui.
    Args:
    - message (str): The message to send.
    - count (int): The number of times to send the message.
    - delay (int, optional): Delay before starting to send messages. Default is 10 seconds.
    """
    print(f"Program will run after {delay} seconds")
    time.sleep(delay)
    print("Running")

    for i in range(1, count + 1):
        pg.write(f"{i}.{message}")
        pg.press("Enter")