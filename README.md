# EnglishCenterManager Project

This project is designed to manage an English center, utilizing a PyQt6 GUI and SQL Server for data management. The application follows the Model-View-Controller (MVC) pattern and implements a 3-layer architecture, ensuring a clean separation of concerns.

## Project Structure

```
EnglishCenterManager
├── src
│   ├── main.py
│   ├── config
│   │   ├── __init__.py
│   │   └── database.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── student.py
│   │   ├── teacher.py
│   │   ├── course.py
│   │   └── enrollment.py
│   ├── views
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── student_view.py
│   │   ├── teacher_view.py
│   │   ├── course_view.py
│   │   └── dialogs
│   │       ├── __init__.py
│   │       ├── student_dialog.py
│   │       ├── teacher_dialog.py
│   │       └── course_dialog.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── student_controller.py
│   │   ├── teacher_controller.py
│   │   ├── course_controller.py
│   │   └── enrollment_controller.py
│   ├── dal
│   │   ├── __init__.py
│   │   ├── base_dal.py
│   │   ├── student_dal.py
│   │   ├── teacher_dal.py
│   │   ├── course_dal.py
│   │   └── enrollment_dal.py
│   ├── bll
│   │   ├── __init__.py
│   │   ├── student_bll.py
│   │   ├── teacher_bll.py
│   │   ├── course_bll.py
│   │   └── enrollment_bll.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── resources
│       ├── __init__.py
│       └── styles.qss
├── tests
│   ├── __init__.py
│   ├── test_student.py
│   ├── test_teacher.py
│   └── test_course.py
├── scripts
│   └── create_database.sql
├── requirements.txt
├── setup.py
└── README.md
```

## Dependencies

The project requires the following Python packages:

- PyQt6
- pyodbc

## Database Connection

The application connects to a SQL Server database using the `pyodbc` library. The connection details (server, database, user ID, and password) should be configured in the `src/data/db_connection.py` file.

## Entry Point

The application starts from the `src/main.py` file, which initializes the PyQt application, establishes a database connection, and displays the main window titled "English Center Manager".

## MVC Pattern

The project is structured according to the MVC pattern, where:

- **Models** represent the data structure (e.g., students, teachers, courses).
- **Views** handle the user interface (e.g., main window, dialogs).
- **Controllers** manage the interaction between models and views.

## Git Ignore

The `.gitignore` file ensures that unnecessary files and directories (like virtual environments and cache files) are not tracked by Git.

## Future Enhancements

Future versions of the application may include additional features such as user authentication, reporting capabilities, and enhanced UI components.

## License

This project is licensed under the MIT License.