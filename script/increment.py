
PATH_ = "test_app/buildozer.spec"
LOCAL_ = "buildozer.spec"

def main():
    with open(PATH_, "r") as read_:
        lines = read_.readlines()

    content = "".join(lines)

    my_line = ""

    for line in lines:
        if line.startswith("version"):
            my_line = line

    if not my_line:
        return print("Line not found...")
    
    value_ = my_line.split("=")[-1].strip()
    value_split = value_.split(".")
    stable_ = int(value_split[0])
    beta_ = int(value_split[1])
    try:
        alpha_ = int(value_split[2])
    except:
        version_line = "version = 0.0.1\n"
    else:
        if alpha_ == 99:
            alpha_ = 0
            beta_ += 1
        else:
            alpha_ += 1
        if beta_ == 10:
            beta_ = 0
            stable_ += 1
        version_line = f"version = {stable_}.{beta_}.{alpha_}\n"

    content = content.replace(my_line, version_line)

    with open(PATH_, "w") as write_:
        write_.write(content)

main()
