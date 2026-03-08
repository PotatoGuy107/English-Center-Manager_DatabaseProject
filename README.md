# English Center Manager

A comprehensive management system for English language learning centers, built with Python, PyQt6, and SQL Server.

## 🎯 Overview

English Center Manager is a desktop application designed to streamline the administration of English language learning centers. The system provides tools for managing students, teachers, courses, enrollments, and billing operations through an intuitive graphical user interface.

## ✨ Features

### Core Functionality
- **Student Management**: Register, update, and track student information
- **Teacher Management**: Maintain teacher profiles and assignments
- **Course Management**: Create and manage course offerings with descriptions and credits
- **Enrollment System**: Handle student course enrollments efficiently
- **Billing & Payments**: Track and manage financial transactions

### Technical Highlights
- **Desktop Application**: Built with PyQt6 for a responsive user experience
- **Database Integration**: SQL Server backend with pyodbc connectivity
- **Three-Tier Architecture**: Organized into Models, Data Access Layer (DAL), Business Logic Layer (BLL), and Views
- **Modular Design**: Clean separation of concerns for maintainability

## 🏗️ Architecture

The project follows a layered architecture pattern:

```
src/
├── models/          # Data models (Course, Teacher, etc.)
├── dal/             # Data Access Layer - database operations
├── bll/             # Business Logic Layer - business rules
├── views/           # User interface components
│   └── dialogs/     # Dialog windows
├── config/          # Database configuration
└── main.py          # Application entry point
```

## 🚀 Getting Started

### Prerequisites

- Python 3.7 or higher
- SQL Server (with ODBC Driver 17)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/PotatoGuy107/English-Center-Manager_DatabaseProject.git
   cd English-Center-Manager_DatabaseProject
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install the package:
   ```bash
   pip install -e .
   ```

3. **Configure database connection**
   
   Update the database credentials in your environment or modify `src/config/database.py`:
   ```python
   db = DatabaseConnection('your_server', 'your_database', 'your_uid', 'your_pwd')
   ```

4. **Initialize the database**
   ```bash
   python CSDL/init_db.py
   ```

5. **Run the application**
   ```bash
   python src/main.py
   ```

## 📦 Dependencies

### Core Dependencies
- **PyQt6** (>=6.4.0): Modern GUI framework
- **pyodbc** (>=4.0.39): Database connectivity for SQL Server
- **python-dotenv** (>=1.0.0): Environment variable management

## 💻 Technology Stack

- **Language**: Python 3.x
- **GUI Framework**: PyQt6
- **Database**: Microsoft SQL Server
- **Database Driver**: pyodbc (ODBC Driver 17 for SQL Server)
- **Architecture**: Three-tier (MVC-inspired)

## 📂 Project Structure

```
English-Center-Manager_DatabaseProject/
├── src/
│   ├── main.py                 # Application entry point
│   ├── models/                 # Data models
│   │   ├── course.py
│   │   └── teacher.py
│   ├── dal/                    # Data Access Layer
│   │   ├── base_dal.py
│   │   ├── course_dal.py
│   │   └── enrollment_dal.py
│   ├── bll/                    # Business Logic Layer
│   ├── views/                  # UI components
│   │   ├── student_view.py
│   │   └── dialogs/
│   └── config/                 # Configuration
│       └── database.py
├── CSDL/                       # Database scripts and utilities
│   ├── 02_seed_data.sql
│   ├── init_db.py
│   ├── DAL/
│   ├── MODELS/
│   └── CONTROLL/
├── tests/                      # Test suite
├── docs/                       # Documentation
├── scripts/                    # Utility scripts
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
└── README.md                   # This file
```

## 🗄️ Database Schema

The system uses SQL Server with the following main entities:

- **Students**: Student profiles and contact information
- **Teachers**: Teacher profiles and subjects
- **Courses**: Course catalog with descriptions and credits
- **Enrollments**: Student-course relationships
- **Bills**: Payment and financial records

## 🛠️ Development

### Setting Up Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install in development mode:
   ```bash
   pip install -e .
   ```

3. Run tests:
   ```bash
   python -m pytest tests/
   ```

### Code Organization

- **Models**: Define data structures and object representations
- **DAL (Data Access Layer)**: Handle all database operations (CRUD)
- **BLL (Business Logic Layer)**: Implement business rules and validation
- **Views**: PyQt6 UI components and dialogs
- **Controllers**: Coordinate between views and business logic

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is part of a database course project. Please check with the repository owner for licensing information.

## 👥 Authors

- **PotatoGuy107** - [GitHub Profile](https://github.com/PotatoGuy107)

## 🔗 Links

- [Repository](https://github.com/PotatoGuy107/English-Center-Manager_DatabaseProject)
- [Issues](https://github.com/PotatoGuy107/English-Center-Manager_DatabaseProject/issues)

## 📞 Support

For questions or support, please open an issue in the GitHub repository.

---

**Note**: This project is designed for educational purposes as part of a database management course.