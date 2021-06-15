import json
import os
import hashlib


blockchain_dir = os.curdir + '/blockchain/'


def get_hash(filename):
    '''Вычисляется хэш входящего файла'''
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.md5(file).hexdigest()


def check_integrity():
    '''Проверяет целостность блоков, стоящих друг за другом, возвращает список с результатом'''
    files = os.listdir(blockchain_dir)
    files = sorted([int(i) for i in files])
    results = []

    for file in files[1:]:
        h = json.load(open(blockchain_dir + str(file)))["hash"]
        actual_hash = get_hash(str(file - 1))
        if h == actual_hash:
            results.append(f'Block {file} is OK')
        else:
            results.append(f'Block {file} is CORRUPTED')
    return results


def write_block(name, amount, to_whom, prev_hash=''):
    def max_number():
        '''Ищет последний порядковый номер в файлах папки blockchain и возвращает его номер числом'''
        files = os.listdir(blockchain_dir)
        last_file = int(files[0])
        for el in files:
            if int(el) > last_file:
                last_file = int(el)
        return last_file

    last_block_name = str(max_number())
    new_block_name = str(int(last_block_name) + 1)
    prev_hash = get_hash(str(last_block_name))

    data = {
        "name": name,
        "amount": amount,
        "to_whom": to_whom,
        "hash": prev_hash,
    }
    with open(blockchain_dir + new_block_name, 'w') as file:
        # indent - отступы, ensure_ascii - нужна кириллица
        json.dump(data, file, indent=4, ensure_ascii=False)


def main():
    # write_block('Liza', 15, 'Petya')
    print(check_integrity())


if __name__ == '__main__':
    main()