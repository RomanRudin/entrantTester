from parser import Parser

if __name__ == "__main__":
    parser = Parser(file_name='data0')
    parser.set_me('')
    parser.set_place(86)
    answer = parser.start()
    for line in answer:
        print(line[0])
    parser.save_unique()
    