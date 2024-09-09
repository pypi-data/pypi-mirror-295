import base64
import webbrowser


def never_gonna_give_you_up():
    never = "aHR0cHM6Ly95b3V0dS5iZS9kUXc0dzlXZ1hjUT9zaT1SRHo1QV81WW5VeTBfVkEt"
    gonna = base64.b64decode(never).decode("utf-8")
    webbrowser.open(gonna)


if __name__ == "__main__":
    never_gonna_give_you_up()
