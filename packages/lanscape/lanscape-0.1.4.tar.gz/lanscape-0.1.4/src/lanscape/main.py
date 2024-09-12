from .webviewer import start_webview
from .app import start_webserver_thread
import webbrowser
import argparse
import time



    
def main():
    args = parse_args()
    def no_gui():
        proc = start_webserver_thread(
            debug=args.debug,
            port=args.port
        )
        # Wait for flask to start
        time.sleep(1)
        webbrowser.open(f'http://127.0.0.1:{args.port}', new=2)
        proc.join()
        
        
    try:
        if args.nogui:
            no_gui()
        else:
            start_webview(
                debug=args.debug,
                port=args.port
            )
    except Exception as e:
        print(e)
        print('falling back to no gui mode')
        no_gui()
        

def parse_args():
    parser = argparse.ArgumentParser(description='LANscape')
    parser.add_argument('--debug', action='store_true', help='Run in debug mode')
    parser.add_argument('--port', type=int, default=5001, help='Port to run the webserver on')
    parser.add_argument('--nogui', action='store_true', help='Run in standalone mode')

    return parser.parse_args()


if __name__ == "__main__":
    main()
        
