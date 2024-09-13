import sys

def create_custom_link():
    if len(sys.argv) != 3:
        print("Usage: linkMod {link} {custom_link}")
        return

    raw = sys.argv[1]
    usr = sys.argv[2]

    # Remove 'https://' if present
    if raw.startswith("https://"):
        raw = raw[8:]

    # Combine the custom link and original link
    link = usr + "@" + raw
    print(link)

if __name__ == "__main__":
    create_custom_link()
