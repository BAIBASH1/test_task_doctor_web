class DB:
    def __init__(self):
        self.db = {}
        self.transactions = []

    def set_key(self, key, value):
        if self.transactions:
            if key not in self.transactions[-1]:
                self.transactions[-1][key] = self.db.get(key, None)
        self.db[key] = value

    def unset_key(self, key):
        if key in self.db:
            if self.transactions:
                if key not in self.transactions[-1]:
                    self.transactions[-1][key] = self.db.get(key, None)
            del self.db[key]

    def get_key(self, key):
        return self.db.get(key, None)

    def counts(self, value):
        return sum(1 for v in self.db.values() if v == value)

    def find(self, value):
        return [k for k, v in self.db.items() if v == value]


def main():
    session_db = DB()
    while True:
        line = input().strip()
        if not line:
            continue  # пропускаем пустые строки
        parts = line.split()
        command = parts[0].upper()

        match command:
            case "END":
                break

            case "SET":
                if len(parts) != 3:
                    print("Ошибка: неверное количество аргументов для SET")
                    continue
                key, value = parts[1], parts[2]
                session_db.set_key(key, value)

            case "GET":
                if len(parts) != 2:
                    print("Ошибка: неверное количество аргументов для GET")
                    continue
                key = parts[1]
                val = session_db.get_key(key)
                print(val if val is not None else "NULL")

            case "UNSET":
                if len(parts) != 2:
                    print("Ошибка: неверное количество аргументов для UNSET")
                    continue
                key = parts[1]
                session_db.unset_key(key)

            case "COUNTS":
                if len(parts) != 2:
                    print("Ошибка: неверное количество аргументов для COUNTS")
                    continue
                value = parts[1]
                print(session_db.counts(value))

            case "FIND":
                if len(parts) != 2:
                    print("Ошибка: неверное количество аргументов для FIND")
                    continue
                value = parts[1]
                found = session_db.find(value)
                print(" ".join(found) if found else "NULL")

            case "BEGIN":
                session_db.transactions.append({})

            case "ROLLBACK":
                if not session_db.transactions:
                    print("NO TRANSACTION")
                else:
                    changes = session_db.transactions.pop()
                    for key, old_value in changes.items():
                        if old_value is None:
                            if key in session_db.db:
                                del session_db.db[key]
                        else:
                            session_db.db[key] = old_value

            case "COMMIT":
                if not session_db.transactions:
                    print("NO TRANSACTION")
                else:
                    changes = session_db.transactions.pop()
                    if session_db.transactions:
                        for key, old_value in changes.items():
                            if key not in session_db.transactions[-1]:
                                session_db.transactions[-1][key] = old_value
            case _:
                print("Неизвестная команда:", command)


if __name__ == "__main__":
    main()
