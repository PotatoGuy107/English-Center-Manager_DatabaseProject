USE EnglishCenterDB;


---Create student-----
CREATE TABLE Student (
    student_id VARCHAR(10) PRIMARY KEY,
    full_name NVARCHAR(100),
    date_of_birth DATE,
    gender VARCHAR(10),
    address NVARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    register_date DATE,
    status VARCHAR(20)
);

------Create Course-----
CREATE TABLE Course (
    course_id VARCHAR(10) PRIMARY KEY,
    course_name NVARCHAR(100) NOT NULL,
    description NVARCHAR(255),
    level NVARCHAR(50),
    duration_weeks INT,
    tuition_fee DECIMAL(12,2),
    status VARCHAR(20)
);

------------Create skill-------------
CREATE TABLE Skill (
    skill_id VARCHAR(10) PRIMARY KEY,
    course_id VARCHAR(10) NOT NULL,
    skill_name NVARCHAR(100),
    description NVARCHAR(255),

    CONSTRAINT FK_Skill_Course
        FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

--------Create teacher-------------
CREATE TABLE Teacher (
    teacher_id VARCHAR(10) PRIMARY KEY,
    full_name NVARCHAR(100),
    phone_number VARCHAR(20),
    email VARCHAR(100),
    specialization NVARCHAR(100),
    hire_date DATE,
    status VARCHAR(20)
);

-----------Create room-------------------
CREATE TABLE Room (
    room_id VARCHAR(10) PRIMARY KEY,
    room_name NVARCHAR(50),
    capacity INT,
    location NVARCHAR(100),
    status VARCHAR(20)
);

--------------Create class------------------
CREATE TABLE Class (
    class_id VARCHAR(10) PRIMARY KEY,
    class_name NVARCHAR(100),
    skill_id VARCHAR(10) NOT NULL,
    teacher_id VARCHAR(10) NOT NULL,
    start_date DATE,
    end_date DATE,
    max_student INT,
    status VARCHAR(20),

    CONSTRAINT FK_Class_Skill
        FOREIGN KEY (skill_id) REFERENCES Skill(skill_id),

    CONSTRAINT FK_Class_Teacher
        FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

--------------Create schedule---------------
CREATE TABLE Schedule (
    schedule_id VARCHAR(10) PRIMARY KEY,
    class_id VARCHAR(10) NOT NULL,
    room_id VARCHAR(10) NOT NULL,
    study_date DATE,
    time_slot NVARCHAR(50),
    start_time TIME,
    end_time TIME,

    CONSTRAINT FK_Schedule_Class
        FOREIGN KEY (class_id) REFERENCES Class(class_id),

    CONSTRAINT FK_Schedule_Room
        FOREIGN KEY (room_id) REFERENCES Room(room_id)
);

-----------------Create enrollment--------------------
CREATE TABLE Enrollment (
    enrollment_id VARCHAR(10) PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    course_id VARCHAR(10) NOT NULL,
    enrollment_date DATE,
    start_date DATE,
    end_date DATE,
    enrollment_status VARCHAR(20),

    CONSTRAINT FK_Enrollment_Student
        FOREIGN KEY (student_id) REFERENCES Student(student_id),

    CONSTRAINT FK_Enrollment_Course
        FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

---------------Create payment-------------------
CREATE TABLE Payment (
    payment_id VARCHAR(10) PRIMARY KEY,
    enrollment_id VARCHAR(10) NOT NULL,
    payment_date DATE,
    amount DECIMAL(12,2),
    payment_status VARCHAR(20),
    note NVARCHAR(255),

    CONSTRAINT FK_Payment_Enrollment
        FOREIGN KEY (enrollment_id) REFERENCES Enrollment(enrollment_id)
);

----------------create class_enrollment-------------------
CREATE TABLE Class_Enrollment (
    class_enrollment_id VARCHAR(10) PRIMARY KEY,
    student_id VARCHAR(10) NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    join_date DATE,
    status VARCHAR(20),

    CONSTRAINT FK_ClassEnroll_Student
        FOREIGN KEY (student_id) REFERENCES Student(student_id),

    CONSTRAINT FK_ClassEnroll_Class
        FOREIGN KEY (class_id) REFERENCES Class(class_id)
);

----------------create exam-----------------
CREATE TABLE Exam (
    exam_id VARCHAR(10) PRIMARY KEY,
    class_id VARCHAR(10) NOT NULL,
    exam_type NVARCHAR(50),
    exam_date DATE,
    description NVARCHAR(255),

    CONSTRAINT FK_Exam_Class
        FOREIGN KEY (class_id) REFERENCES Class(class_id)
);

---------------create exam results ---------------------
CREATE TABLE Exam_Result (
    exam_result_id VARCHAR(10) PRIMARY KEY,
    exam_id VARCHAR(10) NOT NULL,
    class_enrollment_id VARCHAR(10) NOT NULL,
    overall_score DECIMAL(5,2),
    result_status VARCHAR(20),

    CONSTRAINT FK_Result_Exam
        FOREIGN KEY (exam_id) REFERENCES Exam(exam_id),

    CONSTRAINT FK_Result_ClassEnroll
        FOREIGN KEY (class_enrollment_id) REFERENCES Class_Enrollment(class_enrollment_id)
);

-------------------create exam results detailed-------------------
CREATE TABLE Exam_Result_Detailed (
    exam_result_detail_id VARCHAR(10) PRIMARY KEY,
    exam_result_id VARCHAR(10) NOT NULL,
    skill_id VARCHAR(10) NOT NULL,
    score DECIMAL(5,2),

    CONSTRAINT FK_ResultDetail_Result
        FOREIGN KEY (exam_result_id) REFERENCES Exam_Result(exam_result_id),

    CONSTRAINT FK_ResultDetail_Skill
        FOREIGN KEY (skill_id) REFERENCES Skill(skill_id)
);

