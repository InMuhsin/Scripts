import re

def is_none(input, value_if_none):
    if input is None:
        return value_if_none
    return input

def filename_is_safe(filename):
    filename = is_none(filename, "")

    if filename.strip() == "":
        return False
    
    if ("\r" in filename) or ("\n" in filename):
        return False
    
    # will match if not alphanumeric, -, _, or space
    matches = re.findall("[^a-z0-9\-\_\ ]", filename.lower())
    
    return (len(matches) == 0)

# if return empty string -> invalid filename!
def filename_make_safe(filename):
    filename = is_none(filename, "")
    
    filename = filename.replace("\r", "")
    filename = filename.replace("\n", "")

    filename = filename.strip()

    if filename == "":
        return ""

    # will match if not alphanumeric, -, _, or space
    filename = re.sub("[^a-z0-9\-\_\ ]", "", filename.lower()).strip()

    return filename

if __name__ == "__main__":
    while True:
        test = input("Give a file name:")
        print(test)

        print(filename_is_safe(test))
        print(filename_make_safe(test))

        print()

        test = ("\n\n" + test + "\n")
        print(test)

        print(filename_is_safe(test))
        print(filename_make_safe(test))
        
        print()
        print()
