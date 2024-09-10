import sqlite3
from threading import Lock


class PQDatabase():
    _instance = None
    _lock = Lock()  # 다중 스레드 환경에서 안전하게 동작하도록 잠금(Lock) 사용

    def __new__(cls, *args, **kwargs):
        with cls._lock:  # 여러 스레드에서 동시에 접근하지 않도록 Lock
            if cls._instance is None:
                cls._instance = super(PQDatabase, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # 인스턴스가 이미 초기화되었는지 확인 (싱글톤 패턴에서는 이 중복 호출을 방지해야 함)
        if not hasattr(self, 'initialized'):
            self.connection = None
            self.cursor = None
            self.database = None
            self.initialized = True  # 한 번만 초기화되도록 플래그 설정

    def connect(self, database="Database"):
        retVal = False
        try:
            self.database = database + ".db"
            self.connection = sqlite3.connect(self.database)
            self.cursor = self.connection.cursor()
            retVal = True
        except Exception as e:
            print("[DB][CONNECT][ERROR] Connection : ", e)
        return retVal

    def close(self):
        if self.connection is not None:
            self.connection.close()

    def rollback(self):
        if self.connection is not None:
            self.connection.rollback()
            print("[DB] Rollback!")

    def commit(self):
        if self.connection is not None:
            self.connection.commit()
        else:
            print("[DB][COMMIT][ERROR] Connection is None")

    ##########################################################################################################
    # How to use
    # fields = [
    #     ("id", "INTEGER PRIMARY KEY AUTOINCREMENT"),
    #     ("fields1", "TEXT"),
    #     ("fields2", "TEXT"),
    #     ("fields3", "TEXT"),
    #     ("fields4", "TEXT")
    # ]
    # create_table("test", fields)
    ##########################################################################################################
    def create(self, tableName=None, fieldData=None):
        if fieldData is not None:
            fieldDef = ", ".join([f"{fieldName} {fieldType}" for fieldName, fieldType in fieldData])
        else:
            print("[DB][CREATE][ERROR] Field value is None!")
        if tableName is not None:
            sqlCreateTable = f"""CREATE TABLE IF NOT EXISTS {tableName} ({fieldDef});"""
        else:
            print("[DB][CREATE][ERROR] Table name is None!")

        if self.connection is not None:
            self.cursor.execute(sqlCreateTable)
        else:
            print("[DB][CREATE][ERROR] Connection is None!")

    def select(self, tableName=None, fieldId=None, fieldIndex=1, sort=False, reverse=False):
        retVal = None
        if self.connection is not None:
            if tableName is not None:
                if fieldId is None:
                    self.cursor.execute(f"""SELECT * FROM {tableName}""")
                else:
                    self.cursor.execute(f"""SELECT * FROM {tableName} WHERE {fieldId} like %{fieldId}%,?""")
                listTable = self.cursor.fetchall()
                if sort:
                    listTable.sort(key=lambda item: item[fieldIndex], reverse=reverse)
                retVal = listTable
            else:
                print("[DB][SELECT][ERROR] Field name is None!")
        else:
            print("[DB][SELECT][ERROR] Connection is None!")
        return retVal

    def insert(self, tableName=None, fieldData=None):
        if self.connection is not None:
            columns = ', '.join(fieldData.keys())
            placeHolders = ', '.join(['?' for _ in fieldData])
            values = list(fieldData.values())
            if tableName is not None:
                sqlInsert = f"""INSERT INTO {tableName} ({columns}) VALUES ({placeHolders});"""
            try:
                self.cursor.execute(sqlInsert, values)
                self.connection.commit()
            except Exception as e:
                print(f"[DB][INSERT][ERROR] Inserting into {tableName}: {e}")
        else:
            print("[DB][INSERT][ERROR] Connection is None!")

    def update(self, tableName=None, fieldId=None, value=None):
        if self.connection is not None:
            try:
                if tableName is not None:
                    if fieldId is not None:
                        if value is not None:
                            self.cursor.execute(f"""SELECT * FROM {tableName} WHERE id={fieldId}""")
                            exists = self.cursor.fetchall()
                            if exists:
                                self.cursor.execute(f"""UPDATE {tableName} SET {fieldId}={value} WHERE id={fieldId}""")
                            else:
                                print("[DB][UPDATE][ERROR] Field is not exist!")
                        else:
                            print("[DB][UPDATE][ERROR] Value is None!")
                    else:
                        print("[DB][UPDATE][ERROR] Field ID is None!")
                else:
                    print("[DB][UPDATE][ERROR] Table name is None!")
            except Exception as e:
                print(f"[DB][UPDATE][ERROR] Exception:{str(e)}")
        else:
            print("[DB][UPDATE][ERROR] Connection is None!")

    def count(self, tableName=None):
        listCount = 0
        if self.connection is not None:
            if tableName is not None:
                self.cursor.execute(f"""SELECT * FROM {tableName}""")
                list = self.cursor.fetchall()
                listCount = len(list)
            else:
                print("[DB][COUNT][ERROR] Table name is None!")
        else:
            print("[DB][COUNT][ERROR] Connection is None!")
        return listCount

    def sort(self, tableName=None, fieldIndex=1, reverse=False):
        retVal = None
        if self.connection is not None:
            if tableName is not None:
                self.cursor.execute(f"""SELECT * FROM {tableName}""")
                listTable = self.cursor.fetchall()
                listTable.sort(key=lambda item: item[fieldIndex], reverse=reverse)
                retVal = listTable
            else:
                print("[DB][SORT][ERROR] Table name is None!")
        else:
            print("[DB][SORT][ERROR] Connection is None!")
        return retVal

    def delete(self, tableName=None, fieldId=None):
        if self.connection is not None:
            if tableName is not None:
                sqlDeleteTable = f"DELETE FROM {tableName} WHERE id = ?"

                self.cursor.execute(f"""SELECT id FROM {tableName} WHERE id=?""", (fieldId,))
                exists = self.cursor.fetchall()
                if exists:
                    self.cursor.execute(sqlDeleteTable, (fieldId,))
                    self.connection.commit()
                else:
                    print(f"[DB][DELETE][ERROR] Not exist : {fieldId}")
            else:
                print("[DB][DELETE][ERROR] Table name is None!")
        else:
            print("[DB][DELETE][ERROR] Connection is None!")
