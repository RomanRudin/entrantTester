from parser import Parser

if __name__ == "__main__":
    parser = Parser(file_name='data3')
    parser.set_me('139-145-737 75')
    parser.set_place(21)
    answer = parser.start()
    for line in answer:
        print(line[0])
    parser.save_unique()
    