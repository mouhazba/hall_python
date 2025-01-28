# **hall_python**

This repository contains exercises and mini-projects implemented in Python. It is designed for learning and exploring Python programming through practical examples.

---

## **Task Mini Project**

This project simplifies task management by offering an intuitive user interface. It is ideal for students, professionals, and anyone looking to stay organized.

### **Key Features**
- Add, modify, and delete tasks.
- Set reminders for deadlines.
- Collaborative mode for sharing task lists.
- User-friendly interface.

---

### **Project Subdirectories**

#### 1. **`pyTask_with_function`**
   - **Logic**: The core logic remains intact and is implemented using functions.
   - **Description**: Tasks are stored in a list of dictionaries.

#### 2. **`pyTask_with_decorator`**
   - **Logic**: The core project logic remains intact but focuses on decorators.
   - **Description**: Certain tasks in this version are exclusively reserved for admins.

#### 3. **`pyTask_with_class`**
   - **Logic**: Uses a class-based approach for the same project.
   - **Description**:
     - Implements methods within a class to manage the project.
     - Uses decorators for certain methods as needed.

---

## **Check Password Project**

This project allows users to check if their passwords have been exposed in known data breaches by using the Pwned Passwords API.

### **Key Features**
- Validates password security against a database of leaked passwords.
- Uses SHA-1 hashing to maintain password confidentiality.
- Efficiently queries the API using the first 5 characters of the hashed password.
- Simple command-line interface for quick checks.

### **Quick Start**

To use the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/mouhazba/hall_python.git
   cd hall_python
   ```

2. Navigate to the `ztm/check_password` directory:
   ```bash
   cd ztm/check_password
   ```

3. Run the script with a password to check:
   ```bash
   python check_password.py your_password_here
   ```

4. Alternatively, check multiple passwords by providing them as command-line arguments:
   ```bash
   python check_password.py password1 password2 password3
   ```

---

## **Image Converter Project**

This project converts image files in a source directory to PNG format and saves them in a specified output directory.

### **Key Features**
- Converts images from their original format to PNG.
- Allows specifying input and output directories via command-line arguments.
- Automatically creates the output directory if it doesn't exist.

### **Quick Start**

To use the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/mouhazba/hall_python.git
   cd hall_python
   ```

2. Navigate to the `ztm/image_converter` directory:
   ```bash
   cd ztm/image_converter
   ```

3. Run the script with the source directory and output directory as arguments:
   ```bash
   python image_converter.py /path/to/source /path/to/output
   ```

---

## **Goal 100_000 lines of code**

This project lists projects and files written in Python and sets a goal of reaching 100,000 lines of code to inspire beginners and enthusiasts to enjoy the coding journey.

### **Key Features**
- Accepts file or directory paths as command-line inputs.
- Counts lines of code for each path.
- Saves data in a JSON file.
- Updates line counts efficiently.

### **Quick Start**

To use the project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/mouhazba/hall_python.git
   cd hall_python
   ```

2. Navigate to the desired subdirectory (e.g., `pyTask_with_function`).

3. Run the Python script:
   ```bash
   python script_name.py
   ```

---

### **Folder Structure**

```
hall_python/
│
├── pyTask/                      # Task projects directory
|   ├── pyTask_with_function/    # Task project using functions
|   ├── pyTask_with_decorator/   # Task project using decorators
|   ├── pyTask_with_class/       # Task project using classes
├── ztm/                         # ZTM projects directory
|   ├── check_password/          # Check password security project
|   ├── image_converter/         # Image conversion project
├── goal_lines/                  # Contains additional code or tools
|   ├── save_lines_vo/           # Contains version v0
|   ├── save_lines_v1/           # Contains version v1
└── README.md                    # Documentation for the repository
```

---

### **Contributing**

Contributions are welcome! If you'd like to improve the project or add new features:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push:
   ```bash
   git commit -m "Add feature-name"
   git push origin feature-name
   ```
4. Submit a pull request.

---

### **License**

This project is licensed under the MIT License. See the `LICENSE` file for details.

---
