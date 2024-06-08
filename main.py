import threading
import Codes.globals as globals
import Codes.register as register

def main():
    thread = threading.Thread(target=globals.print_ascii_art_with_color_cycle)
    thread.daemon = True
    thread.start()
    globals.loading_bar()
    globals.stop_loading = True
    thread.join()
    globals.reset_terminal_color()
    register.account_section()

if __name__ == '__main__':
    main()