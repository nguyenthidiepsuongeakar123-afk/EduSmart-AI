import sqlite3

DB_NAME = "esa.db"

def init_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        file_name TEXT,

        file_type TEXT,

        file_size REAL,

        subject TEXT,

        grade TEXT,

        category TEXT,

        keywords TEXT,

        ai_summary TEXT,

        confidence REAL,

        upload_time TEXT,

        file_path TEXT

    )
    """)

    # Bảng thư mục
    # ==========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS folders (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        name TEXT NOT NULL,

        parent_id INTEGER,

        root TEXT,

        system_folder INTEGER DEFAULT 0,

        created_at TEXT

    )
    """)

    # ======================================
    # Bảng cài đặt hệ thống ESA
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS system_settings(

        id INTEGER PRIMARY KEY CHECK(id=1),

        department TEXT,

        school TEXT,

        department_group TEXT,

        teacher TEXT,

        school_year TEXT,

        logo TEXT,

        font_name TEXT,

        paper_size TEXT,

        margin_size TEXT

    )

    """)
    # ======================================
    # BẢNG TRI THỨC ESA
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS lesson_master(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        lesson_code TEXT UNIQUE,

        subject TEXT,

        grade TEXT,

        book TEXT,

        chapter TEXT,

        lesson_no INTEGER,

        lesson_name TEXT,

        requirements TEXT,

        knowledge TEXT,

        skills TEXT,

        competencies TEXT,

        qualities TEXT,

        keywords TEXT,

        summary TEXT,

        created_at TEXT,

        updated_at TEXT

    )

    """)


    # ======================================
    # NGUỒN TRI THỨC ESA
    # ======================================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS knowledge_sources(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        lesson_code TEXT,

        source_name TEXT,

        source_type TEXT,

        confidence REAL,

        verified INTEGER DEFAULT 1,

        updated_at TEXT

    )

    """)
    conn.commit()
    conn.close()

def insert_document(file_name,
                    file_type,
                    file_size,
                    file_path):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO documents(

            file_name,

            file_type,

            file_size,

            file_path

        )

        VALUES(?,?,?,?)

    """,(file_name,

         file_type,

         file_size,

         file_path))

    conn.commit()

    conn.close()

def get_all_documents():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM documents

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


def insert_folder(name, parent_id=None, system_folder=0):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO folders(name, parent_id, system_folder)

        VALUES(?,?,?)

    """, (name, parent_id, system_folder))

    conn.commit()

    conn.close()


def get_all_folders():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            id,

            name,

            parent_id,

            root,

            system_folder,

            created_at

        FROM folders

        ORDER BY

            root,

            name

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def create_default_folders():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM folders")

    total = cursor.fetchone()[0]

    if total == 0:

        folders = [

            ("Văn bản Bộ GDĐT", None, "system", 1, ""),
            ("Văn bản Sở GDĐT", None, "system", 1, ""),
            ("Luật - Thông tư", None, "system", 1, ""),
            ("Chương trình GDPT 2018", None, "system", 1, ""),
            ("Chỉ số năng lực số", None, "system", 1, ""),
            ("Biểu mẫu chuẩn", None, "system", 1, ""),
            ("Tài liệu chuẩn khác", None, "system", 1, ""),

            ("Yêu thích", None, "user", 1, ""),
            ("Gần đây", None, "user", 1, ""),
            ("Giáo án", None, "user", 1, ""),
            ("Đề kiểm tra", None, "user", 1, ""),
            ("Ma trận", None, "user", 1, ""),
            ("Bảng đặc tả", None, "user", 1, ""),
            ("Rubric", None, "user", 1, ""),
            ("Học liệu", None, "user", 1, ""),
            ("STEM", None, "user", 1, ""),
            ("KHKT", None, "user", 1, ""),
            ("Hình ảnh", None, "user", 1, ""),
            ("Video", None, "user", 1, ""),
            ("Khác", None, "user", 1, ""),
            ("Thùng rác", None, "user", 1, "")

        ]

        cursor.executemany("""

        INSERT INTO folders(

            name,
            parent_id,
            root,
            system_folder,
            created_at

        )

        VALUES(?,?,?,?,?)

        """, folders)

    conn.commit()

    conn.close()

# ======================================
# SYSTEM SETTINGS
# ======================================

def has_system_settings():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM system_settings
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total > 0


def get_system_settings():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM system_settings
        WHERE id = 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row


def save_system_settings(
    department,
    school,
    department_group,
    teacher,
    school_year,
    logo="",
    font_name="Times New Roman",
    paper_size="A4",
    margin_size="2"
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        INSERT OR REPLACE INTO system_settings(

            id,
            department,
            school,
            department_group,
            teacher,
            school_year,
            logo,
            font_name,
            paper_size,
            margin_size

        )

        VALUES(1,?,?,?,?,?,?,?,?,?)

    """, (

        department,
        school,
        department_group,
        teacher,
        school_year,
        logo,
        font_name,
        paper_size,
        margin_size

    ))

    conn.commit()
    conn.close()


def update_system_settings(
    department,
    school,
    department_group,
    teacher,
    school_year,
    logo,
    font_name,
    paper_size,
    margin_size
):

    save_system_settings(
        department,
        school,
        department_group,
        teacher,
        school_year,
        logo,
        font_name,
        paper_size,
        margin_size
    )

# ======================================
# LESSON MASTER
# ======================================

def get_lessons(subject, grade):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            lesson_code,
            lesson_no,
            lesson_name

        FROM lesson_master

        WHERE subject=?
        AND grade=?

        ORDER BY lesson_no

    """, (subject, grade))

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_lesson(lesson_code):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM lesson_master

        WHERE lesson_code=?

    """, (lesson_code,))

    row = cursor.fetchone()

    conn.close()

    return row

# ======================================
# KNOWLEDGE SOURCES
# ======================================

def save_knowledge_source(

    lesson_code,

    source_name,

    source_type,

    confidence,

    verified,

    updated_at

):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO knowledge_sources(

            lesson_code,

            source_name,

            source_type,

            confidence,

            verified,

            updated_at

        )

        VALUES(?,?,?,?,?,?)

    """,(

        lesson_code,

        source_name,

        source_type,

        confidence,

        verified,

        updated_at

    ))

    conn.commit()

    conn.close()

def search_lessons(keyword):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

            lesson_code,

            lesson_name,

            subject,

            grade

        FROM lesson_master

        WHERE

            lesson_name LIKE ?

            OR

            keywords LIKE ?

    """,(

        "%"+keyword+"%",

        "%"+keyword+"%"

    ))

    rows = cursor.fetchall()

    conn.close()

    return rows