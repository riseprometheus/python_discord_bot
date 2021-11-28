import os


def main():
    print("Setting up Discord Bot")
    token_file = "token.json"
    if not os.path.exists(token_file):
        print("Unable to locate token.json file\nGenerating new json file")
        f = open(token_file, "w")
        f.write('{\n"token": TOKEN_HERE\n}')
        f.close()
        print(f"Please update {token_file} with your discord bot token and rerun setup.py")
        exit(1)

    print(f"{token_file} looks good\nStarting to build docker image")
    try:
        os.system("docker build -t discord_bot_python:latest .")
    except Exception as e:
        print(e)
    print("Successfully built docker image")


if __name__ == '__main__':
    main()
