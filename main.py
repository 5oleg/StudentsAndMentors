class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return f"Имя: {self.name}\n" \
               f"Фамилия: {self.surname}\n" \
               f"Средняя оценка за домашние задания: {self.hw_avg_grade()}\n" \
               f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n" \
               f"Завершенные курсы: {', '.join(self.finished_courses)}"

    def __lt__(self, other):
        return self.hw_avg_grade() < other.hw_avg_grade()

    def __le__(self, other):
        return self.hw_avg_grade() <= other.hw_avg_grade()

    def __gt__(self, other):
        return self.hw_avg_grade() > other.hw_avg_grade()

    def __ge__(self, other):
        return self.hw_avg_grade() >= other.hw_avg_grade()

    def __eq__(self, other):
        return self.hw_avg_grade() == other.hw_avg_grade()

    def __ne__(self, other):
        return self.hw_avg_grade() != other.hw_avg_grade()

    def hw_avg_grade(self):
        grades_count = 0
        grades_sum = 0
        for grades in self.grades.values():
            grades_count += len(grades)
            grades_sum += sum(grades)
        if grades_count:
            return grades_sum / grades_count
        else:
            return 0

    def rate_lecturer(self, lecturer, course, rate):
        if not isinstance(rate, int) or rate not in range(1, 11):
            return "Некорректная оценка (необходимо число от 1 до 10)"
        elif not isinstance(lecturer, Lecturer):
            return "Некорректный тип аргумента"
        elif course not in self.courses_in_progress + self.finished_courses:
            return f"Студент {self.name} {self.surname} не записывался на курс {course}"
        elif course not in lecturer.courses_attached:
            return f"Преподаватель {self.name} {self.surname} не читает лекции по предмету {course}"
        else:
            if course in lecturer.rates_by_studs:
                lecturer.rates_by_studs[course].append(rate)
            else:
                lecturer.rates_by_studs[course] = [rate]
            return f"Лектору {lecturer.surname} выставлена оценка {rate} за лекцию по предмету {course}!"


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.rates_by_studs = {}

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}\nСредняя оценка за лекции: {self.stud_avg_rate()}"

    def __lt__(self, other):
        return self.stud_avg_rate() < other.stud_avg_rate()

    def __le__(self, other):
        return self.stud_avg_rate() <= other.stud_avg_rate()

    def __gt__(self, other):
        return self.stud_avg_rate() > other.stud_avg_rate()

    def __ge__(self, other):
        return self.stud_avg_rate() >= other.stud_avg_rate()

    def __eq__(self, other):
        return self.stud_avg_rate() == other.stud_avg_rate()

    def __ne__(self, other):
        return self.stud_avg_rate() != other.stud_avg_rate()

    def stud_avg_rate(self):
        rates_count = 0
        rates_sum = 0
        for rates in self.rates_by_studs.values():
            rates_count += len(rates)
            rates_sum += sum(rates)
        if rates_count:
            return rates_sum / rates_count
        else:
            return 0


class Reviewer(Mentor):

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def calc_avg_stud_grade(students_list, course):
    grades_count = 0
    grades_sum = 0
    for student in students_list:
        if course in student.grades:
            grades_count += len(student.grades[course])
            grades_sum += sum(student.grades[course])
    if grades_count:
        return grades_sum / grades_count
    else:
        return 0


def calc_avg_lect_rate(lecturers_list, course):
    rates_count = 0
    rates_sum = 0
    for lecturer in lecturers_list:
        if course in lecturer.rates_by_studs:
            rates_count += len(lecturer.rates_by_studs[course])
            rates_sum += sum(lecturer.rates_by_studs[course])
    if rates_count:
        return rates_sum / rates_count
    else:
        return 0

def main():
    students = [
        Student("Артур", "Пирожков", "м"),
        Student("Мария", "Ватрушкина", "ж")
    ]

    print("Наши студенты (пока никуда не записаны):\n")
    for student in students:
        print(student, '\n')

    lecturers = [
        Lecturer("Макар", "Чердаков"),
        Lecturer("Василий", "Преображенский")
    ]

    print("Наши лекторы:\n")
    for lect in lecturers:
        print(lect, '\n')

    reviewers = [
        Reviewer("Максим", "Экспертин"),
        Reviewer("Геннадий", "Ревизин")
    ]

    print("Наши проверяющие:\n")
    for reviewer in reviewers:
        print(reviewer, '\n')

    courses = ["Питон для новичков", "Выгорание у программистов"]

    for student in students:
        student.courses_in_progress.append(courses[0])

    students[1].courses_in_progress.append(courses[1])

    lecturers[0].courses_attached.append(courses[0])
    lecturers[1].courses_attached.append(courses[1])

    for reviewer in reviewers:
        reviewer.courses_attached.extend(courses)

    reviewers[0].rate_hw(students[0], courses[0], 2)
    reviewers[0].rate_hw(students[1], courses[0], 3)
    reviewers[0].rate_hw(students[1], courses[1], 4)

    print(students[0].rate_lecturer(lecturers[0], courses[0], 5))
    print(students[1].rate_lecturer(lecturers[0], courses[0], 6))
    print(students[1].rate_lecturer(lecturers[1], courses[1], 6))

    print("\nРЕЗУЛЬТАТЫ ОБУЧЕНИЯ:\n")

    for student in students:
        print(student, '\n')

    for lect in lecturers:
        print(lect, '\n')

    print(f"Рейтинг лектора {lecturers[0].surname} ниже рейтинга лектора {lecturers[1].surname}? Результат:")
    print(lecturers[0] < lecturers[1], '\n')

    print(f"Средняя оценка по всем студентам в рамках курса {courses[0]}:\n{calc_avg_stud_grade(students, courses[0])}")
    print(f"Средний рейтинг по всем лекторам в рамках курса {courses[0]}:\n{calc_avg_lect_rate(lecturers, courses[0])}")


if __name__ == '__main__':
    main()
