"""Internship project suite.

Contains beginner-friendly implementations for:
1) Student Management System
2) Marks Prediction (simple ML with optional scikit-learn)
3) Cloud File Backup Simulation
4) Linux File Management (safe sandbox in local folder)
5) Zero Client model explanation
6) Cybersecurity Login System
Bonus) Smart School System (integrated menu)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# -----------------------------
# 1) Student Management System
# -----------------------------
@dataclass
class Student:
    name: str
    marks: float

    @property
    def status(self) -> str:
        return "Pass" if self.marks >= 40 else "Fail"


class StudentManagementSystem:
    def __init__(self) -> None:
        self.students: List[Student] = []

    def add_student(self, name: str, marks: float) -> None:
        self.students.append(Student(name=name, marks=marks))

    def list_results(self) -> List[Tuple[str, float, str]]:
        return [(student.name, student.marks, student.status) for student in self.students]


# -----------------------------
# 2) Marks Prediction Project
# -----------------------------
class MarksPrediction:
    """Predict marks from study hours.

    Uses scikit-learn LinearRegression if available.
    Falls back to manual simple linear regression.
    """

    def __init__(self) -> None:
        self._model = None
        self._coef = None
        self._intercept = None

    def train(self, hours: List[float], marks: List[float]) -> None:
        if len(hours) != len(marks) or not hours:
            raise ValueError("Hours and marks must be non-empty and of same length.")

        try:
            from sklearn.linear_model import LinearRegression  # type: ignore
            import numpy as np

            x = np.array(hours).reshape(-1, 1)
            y = np.array(marks)
            model = LinearRegression()
            model.fit(x, y)
            self._model = model
        except Exception:
            # Manual least-squares fit for y = m*x + b
            n = len(hours)
            mean_x = sum(hours) / n
            mean_y = sum(marks) / n
            numerator = sum((hours[i] - mean_x) * (marks[i] - mean_y) for i in range(n))
            denominator = sum((hours[i] - mean_x) ** 2 for i in range(n))
            if denominator == 0:
                raise ValueError("Cannot train with identical hour values.")
            self._coef = numerator / denominator
            self._intercept = mean_y - self._coef * mean_x

    def predict(self, hours: float) -> float:
        if self._model is not None:
            import numpy as np

            return float(self._model.predict(np.array([[hours]]))[0])

        if self._coef is None or self._intercept is None:
            raise RuntimeError("Model is not trained yet.")

        return self._coef * hours + self._intercept


# -----------------------------
# 3) Cloud Backup Simulation
# -----------------------------
class FileBackupSimulation:
    def __init__(self) -> None:
        self.backup_files: List[str] = []

    def backup_file(self, filename: str) -> None:
        if filename and filename not in self.backup_files:
            self.backup_files.append(filename)

    def list_backups(self) -> List[str]:
        return list(self.backup_files)


# -----------------------------
# 4) Linux File Management
# -----------------------------
class LinuxFileManagement:
    """Simple file/folder operations within a safe base directory."""

    def __init__(self, base_dir: str = "linux_lab") -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, relative_path: str) -> Path:
        target = (self.base_path / relative_path).resolve()
        if self.base_path.resolve() not in target.parents and target != self.base_path.resolve():
            raise ValueError("Path is outside base directory.")
        return target

    def create_folder(self, folder_name: str) -> Path:
        folder = self._safe_path(folder_name)
        folder.mkdir(parents=True, exist_ok=True)
        return folder

    def create_file(self, file_name: str, content: str = "") -> Path:
        file_path = self._safe_path(file_name)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path

    def delete_path(self, target_name: str) -> bool:
        target = self._safe_path(target_name)
        if not target.exists():
            return False
        if target.is_file():
            target.unlink()
            return True
        if target.is_dir():
            try:
                target.rmdir()  # Removes empty directories
                return True
            except OSError:
                # Directory not empty
                return False
        return False

    def list_paths(self) -> List[str]:
        result: List[str] = []
        for path in sorted(self.base_path.rglob("*")):
            kind = "DIR" if path.is_dir() else "FILE"
            result.append(f"{kind}: {path.relative_to(self.base_path)}")
        return result


# -----------------------------
# 5) Zero Client explanation
# -----------------------------
def explain_zero_client_model() -> str:
    return (
        "Zero Client Model: The client device has minimal processing and storage. "
        "Applications and data run on a central server (or cloud VDI). "
        "Client devices connect to the server over a network, display remote sessions, "
        "and send keyboard/mouse input back to the server. "
        "Benefits: central management, stronger data control, easier updates. "
        "Limitations: requires stable network and capable server infrastructure."
    )


# -----------------------------
# 6) Cybersecurity login system
# -----------------------------
class LoginSystem:
    def __init__(self, users: Optional[Dict[str, str]] = None, max_attempts: int = 3) -> None:
        self.users = users or {"admin": "Admin@123", "student": "study123"}
        self.max_attempts = max_attempts

    def authenticate(self, username: str, password: str) -> bool:
        return self.users.get(username) == password

    def login_with_attempts(self) -> bool:
        attempts = 0
        while attempts < self.max_attempts:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            if self.authenticate(username, password):
                print("Login successful.")
                return True
            attempts += 1
            print(f"Invalid credentials. Attempts left: {self.max_attempts - attempts}")
        print("Account locked (simulation): max attempts reached.")
        return False


# -----------------------------
# BONUS: Smart School System
# -----------------------------
class SmartSchoolSystem:
    def __init__(self) -> None:
        self.sms = StudentManagementSystem()
        self.predictor = MarksPrediction()
        self.backup = FileBackupSimulation()
        self.linux_manager = LinuxFileManagement()
        self.login = LoginSystem()

    def run_demo(self) -> None:
        print("=== SMART SCHOOL SYSTEM ===")
        print("1. Login")
        if not self.login.login_with_attempts():
            return

        # Student management demo
        self.sms.add_student("Asha", 78)
        self.sms.add_student("Rahul", 34)
        print("\nStudent Results:")
        for name, marks, status in self.sms.list_results():
            print(f"- {name}: {marks} -> {status}")

        # ML demo
        train_hours = [1, 2, 3, 4, 5, 6]
        train_marks = [35, 40, 50, 60, 70, 78]
        self.predictor.train(train_hours, train_marks)
        predicted = self.predictor.predict(4.5)
        print(f"\nPredicted marks for 4.5 study hours: {predicted:.2f}")

        # Backup demo
        self.backup.backup_file("report_card.pdf")
        self.backup.backup_file("attendance.xlsx")
        print("\nBacked-up files:")
        for filename in self.backup.list_backups():
            print(f"- {filename}")

        # Linux management demo
        self.linux_manager.create_folder("students")
        self.linux_manager.create_file("students/info.txt", "Student data sample")
        print("\nLinux lab contents:")
        for item in self.linux_manager.list_paths():
            print(f"- {item}")

        # Zero client model
        print("\nZero Client Model Explanation:")
        print(explain_zero_client_model())


def main() -> None:
    print("Project suite created for internship tasks.")
    print("Run SmartSchoolSystem().run_demo() from Python for an interactive demonstration.")


if __name__ == "__main__":
    main()
