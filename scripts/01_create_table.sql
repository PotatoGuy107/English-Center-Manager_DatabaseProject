-- 1. Student
CREATE TABLE Student (
    student_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    date_of_birth DATE,
    gender NVARCHAR(10),
    address NVARCHAR(255),
    phone_number NVARCHAR(20),
    email NVARCHAR(100) UNIQUE,
    register_date DATE DEFAULT GETDATE(),
    status NVARCHAR(20) 
        CHECK (status IN ('active','inactive')) 
        DEFAULT 'active'
);

-- 2. Course
CREATE TABLE Course (
    course_id INT IDENTITY(1,1) PRIMARY KEY,
    course_name NVARCHAR(150) NOT NULL,
    description NVARCHAR(MAX),
    level NVARCHAR(50),
    duration_weeks INT,
    tuition_fee DECIMAL(12,2),
    status NVARCHAR(20) 
        CHECK (status IN ('active','inactive')) 
        DEFAULT 'active'
);

-- 3. Enrollment
CREATE TABLE Enrollment (
    enrollment_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE DEFAULT GETDATE(),
    start_date DATE,
    end_date DATE,
    enrollment_status NVARCHAR(30)
        CHECK (enrollment_status IN ('pending','studying','completed','cancelled'))
        DEFAULT 'pending',

    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- 4. Payment
CREATE TABLE Payment (
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
    enrollment_id INT NOT NULL,
    payment_date DATE DEFAULT GETDATE(),
    amount DECIMAL(12,2) NOT NULL,
    payment_status NVARCHAR(30)
        CHECK (payment_status IN ('unpaid','paid','partial','refunded'))
        DEFAULT 'unpaid',
    note NVARCHAR(255),

    FOREIGN KEY (enrollment_id) REFERENCES Enrollment(enrollment_id)
);

-- 5. Skill
CREATE TABLE Skill (
    skill_id INT IDENTITY(1,1) PRIMARY KEY,
    course_id INT NOT NULL,
    skill_name NVARCHAR(150) NOT NULL,
    description NVARCHAR(MAX),

    FOREIGN KEY (course_id) REFERENCES Course(course_id)
);

-- 6. Teacher
CREATE TABLE Teacher (
    teacher_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name NVARCHAR(100) NOT NULL,
    phone_number NVARCHAR(20),
    email NVARCHAR(100),
    specialization NVARCHAR(150),
    hire_date DATE,
    status NVARCHAR(20)
        CHECK (status IN ('active','inactive'))
        DEFAULT 'active'
);

-- 7. Class
CREATE TABLE Class (
    class_id INT IDENTITY(1,1) PRIMARY KEY,
    skill_id INT NOT NULL,
    teacher_id INT NOT NULL,
    class_name NVARCHAR(150),
    start_date DATE,
    end_date DATE,
    max_student INT,
    status NVARCHAR(20)
        CHECK (status IN ('planned','ongoing','completed','cancelled'))
        DEFAULT 'planned',

    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id),
    FOREIGN KEY (teacher_id) REFERENCES Teacher(teacher_id)
);

-- 8. Class_Enrollment
CREATE TABLE Class_Enrollment (
    class_enrollment_id INT IDENTITY(1,1) PRIMARY KEY,
    student_id INT NOT NULL,
    class_id INT NOT NULL,
    join_date DATE DEFAULT GETDATE(),
    status NVARCHAR(30)
        CHECK (status IN ('studying','completed','dropped'))
        DEFAULT 'studying',

    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (class_id) REFERENCES Class(class_id)
);

-- 9. Exam
CREATE TABLE Exam (
    exam_id INT IDENTITY(1,1) PRIMARY KEY,
    class_id INT NOT NULL,
    exam_type NVARCHAR(50),
    exam_date DATE,
    description NVARCHAR(MAX),

    FOREIGN KEY (class_id) REFERENCES Class(class_id)
);

-- 10. Exam_Result
CREATE TABLE Exam_Result (
    exam_result_id INT IDENTITY(1,1) PRIMARY KEY,
    exam_id INT NOT NULL,
    class_enrollment_id INT NOT NULL,
    overall_score DECIMAL(5,2),
    result_status NVARCHAR(10)
        CHECK (result_status IN ('pass','fail')),

    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id),
    FOREIGN KEY (class_enrollment_id) REFERENCES Class_Enrollment(class_enrollment_id)
);

-- 11. Exam_Result_Detailed
CREATE TABLE Exam_Result_Detailed (
    exam_result_detailed_id INT IDENTITY(1,1) PRIMARY KEY,
    exam_result_id INT NOT NULL,
    skill_id INT NOT NULL,
    score DECIMAL(5,2),

    FOREIGN KEY (exam_result_id) REFERENCES Exam_Result(exam_result_id),
    FOREIGN KEY (skill_id) REFERENCES Skill(skill_id)
);

-- 12. Room
CREATE TABLE Room (
    room_id INT IDENTITY(1,1) PRIMARY KEY,
    room_name NVARCHAR(100),
    capacity INT,
    location NVARCHAR(150),
    status NVARCHAR(20)
        CHECK (status IN ('available','maintenance','unavailable'))
        DEFAULT 'available'
);

-- 13. Schedule
CREATE TABLE Schedule (
    schedule_id INT IDENTITY(1,1) PRIMARY KEY,
    class_id INT NOT NULL,
    room_id INT NOT NULL,
    study_date DATE,
    time_slot NVARCHAR(50),
    start_time TIME,
    end_time TIME,

    FOREIGN KEY (class_id) REFERENCES Class(class_id),
    FOREIGN KEY (room_id) REFERENCES Room(room_id)
);