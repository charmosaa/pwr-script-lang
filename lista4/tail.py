import argparse
import sys
import time
import os

DEFAULT_LINES = 10

def tail(lines, n=DEFAULT_LINES):
    for line in lines[-n:]:
        print(line, end="")  # to avoid double newlines

def follow(file):
    file.seek(0, os.SEEK_END)
    
    try:
        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)
                continue
            print(line, end="")  
    except KeyboardInterrupt:
        print("\nFile monitoring ended.")

def main():
    parser = argparse.ArgumentParser(description="Simplified tail command")
    parser.add_argument("path", nargs="?", help="Path to the file")
    parser.add_argument("--lines", "-n", type=int, default=DEFAULT_LINES, help="Number of lines to display")
    parser.add_argument("--follow", "-f", action="store_true", help="Keep displaying new lines as they are being added")

    args = parser.parse_args()

    if not args.path and sys.stdin.isatty():
        parser.error("No input provided. Provide a file path or use stdin.")

    # input from file 
    if args.path:
        try:
            with open(args.path, encoding="utf-8") as file:
                lines = file.readlines()
                tail(lines, args.lines)

                if args.follow:
                    follow(file)

        except FileNotFoundError:
            print(f"Error: File '{args.path}' not found.", file=sys.stderr)
            sys.exit(1)
        except PermissionError:
            print(f"Error: No permission to read '{args.path}'.", file=sys.stderr)
            sys.exit(1)

    # input from stdin 
    else:
        lines = sys.stdin.readlines()
        tail(lines, args.lines)

if __name__ == "__main__":
    main()
