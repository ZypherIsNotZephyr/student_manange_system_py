import pymysql


# 学生账号密码匹配
def SqlConnect_Login(sid, pwd):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    try:
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.callproc("p", (sid, 0))  # 参数为存储过程名称和存储过程接收的参数
        db.commit()
        password = cursor.fetchall()[0]['password']
        if pwd == password:
            return 1



    except:
        db.rollback()
        return 0

    cursor.close()
    db.close()


# 查询学生信息
def SqlConnect_Person(sid):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    sql = """
       select *
       from student
       where sid = '%d'
    """ % sid
    try:
        cursor.execute(sql)
        studentmessage = cursor.fetchall()[0]
        # return studentmessage[0],studentmessage[1],studentmessage[2],studentmessage[3],studentmessage[4],studentmessage[5],studentmessage[6],studentmessage[7]
        return studentmessage
    except:
        db.rollback()
        return (0, 0, 0, 0, 0, 0, 0)

    cursor.close()
    db.close()


# 更新学生信息
def SqlConnect_Save_Student(student):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    lock = """
        lock tables student write
        """
    cursor.execute(lock)
    sql = """
        update student
        set sname = '%s',password = '%s',phone = '%ld',email='%s',homepage='%s',profile='%s'
        where sid = '%d'
    """ % (student[1], student[2], int(student[3]), student[4], student[5], student[6], int(student[0]))
    try:
        cursor.execute(sql)
        db.commit()
        unlock = """
            unlock tables
        """
        cursor.execute(unlock)
        return 1
    except:
        db.rollback()
        return 0
    cursor.close()
    db.close()


# 查看所有课程
def SqlConnect_Allcourses():
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    sql = """
            select courses.cid,courses.cname,teacher.tname,courses.hours,courses.credit
            from courses,teacher
            where courses.cid = teacher.cid
            order by courses.cid asc
            
        """
    try:
        cursor.execute(sql)
        all = cursor.fetchall()
        return all
    except:
        db.rollback()
        return None
    cursor.close()
    db.close()


# 搜索课程
def SqlConnect_Search_Courses(index, message):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    if index == 0:
        sql = """
                    select courses.cid,courses.cname,teacher.tname,courses.hours,courses.credit
                    from courses,teacher
                    where courses.cid = teacher.cid and courses.cid= '%d'
            """ % int(message)
    if index == 1:
        sql = """
                    select courses.cid,courses.cname,teacher.tname,courses.hours,courses.credit
                    from courses,teacher
                    where courses.cid = teacher.cid and courses.cname= '%s'
            """ % message
    if index == 2:
        sql = """
                    select courses.cid,courses.cname,teacher.tname,courses.hours,courses.credit
                    from courses,teacher
                    where courses.cid = teacher.cid and teacher.tname= '%s'
            """ % message
    try:
        cursor.execute(sql)
        all = cursor.fetchall()
        return all
    except:
        db.rollback()
        return None
    cursor.close()
    db.close()


# 添加课程
def SqlConnect_Add_Course(cid, tname, sid):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    cursor1 = db.cursor()
    sql0 = """
        select tid
        from teacher
        where tname='%s'
    """ % tname
    try:
        cursor.execute(sql0)
        tid = cursor.fetchall()[0][0]
        # print(tid)
    except:
        return 0
    sql = """
                insert into choices
                values('%d','%d','%d')
            """ % (int(cid), int(sid), int(tid))
    try:
        # print(cid,sid,tid)
        cursor1.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return 1
    except:
        db.rollback()
        return 0


# 查看已选课程
def SqlConnect_Seecourses(sid):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    sql = """
                select courses.cname,teacher.tname,courses.ctime,teacher.tplace
                from courses,teacher,choices
                where choices.sid = '%d' and courses.cid = choices.cid and choices.tid = teacher.tid
                order by courses.cid asc

            """ % int(sid)
    try:
        cursor.execute(sql)
        all = cursor.fetchall()
        return all
    except:
        db.rollback()
        return None
    cursor.close()
    db.close()


# 删除课程
def SqlConnect_Del_Course(cid, tname, sid):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    cursor1 = db.cursor()
    sql0 = """
            select tid
            from teacher
            where tname='%s'
        """ % tname
    try:
        cursor.execute(sql0)
        tid = cursor.fetchall()[0][0]
    except:
        return 0
    sql = """
                    delete from choices
                    where cid = '%d' and sid = '%d' and tid = '%d'
                """ % (int(cid), int(sid), int(tid))
    try:
        cursor1.execute(sql)
        db.commit()
        cursor.close()
        db.close()
        return 1
    except:
        db.rollback()
        return 0


# 考试查询
def SqlConnect_Seeexam(sid):
    db = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        database='hw',
        charset='utf8'
    )
    cursor = db.cursor()
    sql = """
                select exam.eid,exam.ename,exam.etime,exam.eplace
                from choices,exam
                where choices.sid = '%d' and choices.cid = exam.cid
                order by exam.eid asc

            """ % int(sid)
    try:
        cursor.execute(sql)
        all = cursor.fetchall()
        return all
    except:
        db.rollback()
        return None
    cursor.close()
    db.close()

# student = (20180001, "张三","123456",17860397176,'787@163.com','1','1')
# SqlConnect_Save_Student(student)
# SqlConnect_Allcourses()
# SqlConnect_Add_Course(9999, '清晓哥', 20180002)
