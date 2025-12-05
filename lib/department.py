from lib.db import CONN, CURSOR


class Department:

    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    # ----------------------------
    # TABLE METHODS
    # ----------------------------
    @classmethod
    def create_table(cls):
        CURSOR.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            );
        """)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS departments;")
        CONN.commit()

    # ----------------------------
    # CRUD METHODS
    # ----------------------------
    def save(self):
        if self.id is None:
            CURSOR.execute(
                "INSERT INTO departments (name, location) VALUES (?, ?)",
                (self.name, self.location)
            )
            self.id = CURSOR.lastrowid
        else:
            self.update()

        Department.all[self.id] = self
        CONN.commit()

    @classmethod
    def create(cls, name, location):
        dept = cls(name, location)
        dept.save()
        return dept

    def update(self):
        CURSOR.execute(
            "UPDATE departments SET name=?, location=? WHERE id=?",
            (self.name, self.location, self.id)
        )
        CONN.commit()
        Department.all[self.id] = self

    def delete(self):
        """Delete the table row and update local dictionary and object state"""
        CURSOR.execute("DELETE FROM departments WHERE id=?", (self.id,))
        CONN.commit()

        # Remove from local dictionary if present
        Department.all.pop(self.id, None)

        # Set the instance id to None
        self.id = None

    # ----------------------------
    # QUERY METHODS
    # ----------------------------
    @classmethod
    def instance_from_db(cls, row):
        id, name, location = row

        if id in cls.all:
            instance = cls.all[id]
            instance.name = name
            instance.location = location
        else:
            instance = cls(name, location, id)
            cls.all[id] = instance

        return instance

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM departments").fetchall()
        return [cls.instance_from_db(r) for r in rows]

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE id=?", (id,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute(
            "SELECT * FROM departments WHERE name=?", (name,)
        ).fetchone()
        return cls.instance_from_db(row) if row else None

    # ----------------------------
    # RELATIONSHIP METHOD
    # ----------------------------
    def employees(self):
        from lib.employee import Employee  # fix import relative to lib
        return [emp for emp in Employee.get_all() if emp.department_id == self.id]
