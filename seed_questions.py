import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from accounts.models import User
from subjects.models import Subject, Topic
from questions.models import Question


subject = Subject.objects.get(name="QA")
topic = Topic.objects.get(subject=subject, name="Average")
admin = User.objects.get(username="admin")


questions = [
    {
        "question_text": "The average of five numbers is 24. What is their total?",
        "option_a": "100",
        "option_b": "110",
        "option_c": "120",
        "option_d": "125",
        "correct_option": "C",
        "explanation": "Total = Average × Number of values = 24 × 5 = 120.",
    },
    {
        "question_text": "The average of 8 numbers is 15. If one number is removed, the average of the remaining 7 numbers becomes 14. What is the removed number?",
        "option_a": "20",
        "option_b": "22",
        "option_c": "24",
        "option_d": "26",
        "correct_option": "B",
        "explanation": "Total of 8 numbers = 120 and total of remaining 7 = 98. Removed number = 22.",
    },
    {
        "question_text": "The average age of 4 students is 18 years. If a teacher aged 28 years joins them, what is the new average age?",
        "option_a": "19 years",
        "option_b": "20 years",
        "option_c": "21 years",
        "option_d": "22 years",
        "correct_option": "B",
        "explanation": "Total = 4 × 18 + 28 = 100. New average = 100 / 5 = 20 years.",
    },
    {
        "question_text": "The average of three consecutive even numbers is 24. What is the largest number?",
        "option_a": "24",
        "option_b": "26",
        "option_c": "28",
        "option_d": "30",
        "correct_option": "B",
        "explanation": "The numbers are 22, 24 and 26. Largest = 26.",
    },
    {
        "question_text": "The average marks of 6 students is 70. If one student scored 90 marks, what is the average of the remaining 5 students?",
        "option_a": "64",
        "option_b": "65",
        "option_c": "66",
        "option_d": "68",
        "correct_option": "C",
        "explanation": "Total = 420. Remaining total = 420 - 90 = 330. Average = 330 / 5 = 66.",
    },
    {
        "question_text": "The average of 12, 18, 24 and x is 21. Find x.",
        "option_a": "28",
        "option_b": "30",
        "option_c": "32",
        "option_d": "34",
        "correct_option": "B",
        "explanation": "Required total = 84. Known total = 54. Therefore x = 30.",
    },
    {
        "question_text": "The average of 7 numbers is 18. If each number is increased by 3, what will be the new average?",
        "option_a": "18",
        "option_b": "19",
        "option_c": "20",
        "option_d": "21",
        "correct_option": "D",
        "explanation": "The average also increases by 3. New average = 21.",
    },
    {
        "question_text": "The average salary of 5 employees is ₹30,000. If a new employee with salary ₹36,000 joins, what is the new average salary?",
        "option_a": "₹30,500",
        "option_b": "₹31,000",
        "option_c": "₹31,500",
        "option_d": "₹32,000",
        "correct_option": "B",
        "explanation": "New total = ₹186,000. Average = ₹186,000 / 6 = ₹31,000.",
    },
    {
        "question_text": "The average of 10 numbers is 25. If each number is multiplied by 2, what will be the new average?",
        "option_a": "25",
        "option_b": "40",
        "option_c": "50",
        "option_d": "60",
        "correct_option": "C",
        "explanation": "The average is also multiplied by 2. New average = 50.",
    },
    {
        "question_text": "The average of 5 consecutive integers is 32. What is the smallest integer?",
        "option_a": "28",
        "option_b": "29",
        "option_c": "30",
        "option_d": "31",
        "correct_option": "C",
        "explanation": "The integers are 30, 31, 32, 33 and 34. Smallest = 30.",
    },
    {
        "question_text": "The average of 9 numbers is 20. If one number 28 is replaced by 37, what is the new average?",
        "option_a": "20",
        "option_b": "21",
        "option_c": "22",
        "option_d": "23",
        "correct_option": "B",
        "explanation": "Total increases by 9. Average increases by 9 / 9 = 1. New average = 21.",
    },
    {
        "question_text": "The average of 6 numbers is 16. If every number is decreased by 4, what is the new average?",
        "option_a": "10",
        "option_b": "11",
        "option_c": "12",
        "option_d": "13",
        "correct_option": "C",
        "explanation": "The average also decreases by 4. New average = 12.",
    },
    {
        "question_text": "The average age of 5 children is 12 years. If the age of their father is included, the average becomes 17 years. What is the father's age?",
        "option_a": "40 years",
        "option_b": "42 years",
        "option_c": "44 years",
        "option_d": "46 years",
        "correct_option": "B",
        "explanation": "Children total = 60. Total with father = 102. Father's age = 42 years.",
    },
    {
        "question_text": "The average of 15 numbers is 40. What is their total?",
        "option_a": "500",
        "option_b": "550",
        "option_c": "600",
        "option_d": "650",
        "correct_option": "C",
        "explanation": "Total = 40 × 15 = 600.",
    },
    {
        "question_text": "The average of two numbers is 45. If one number is 38, what is the other number?",
        "option_a": "48",
        "option_b": "50",
        "option_c": "52",
        "option_d": "54",
        "correct_option": "C",
        "explanation": "Total = 90. Other number = 90 - 38 = 52.",
    },
    {
        "question_text": "The average score of a student in 4 tests is 72. What score is needed in the fifth test to make the average 76?",
        "option_a": "88",
        "option_b": "90",
        "option_c": "92",
        "option_d": "94",
        "correct_option": "C",
        "explanation": "Current total = 288. Required total = 380. Required score = 92.",
    },
    {
        "question_text": "The average of 20, 30, 40, 50 and x is 38. Find x.",
        "option_a": "45",
        "option_b": "48",
        "option_c": "50",
        "option_d": "55",
        "correct_option": "C",
        "explanation": "Required total = 190. Known total = 140. Therefore x = 50.",
    },
    {
        "question_text": "The average weight of 8 persons is 60 kg. If one person weighing 67 kg leaves, what is the average weight of the remaining 7 persons?",
        "option_a": "57 kg",
        "option_b": "58 kg",
        "option_c": "59 kg",
        "option_d": "60 kg",
        "correct_option": "C",
        "explanation": "Total = 480 kg. Remaining = 413 kg. Average = 413 / 7 = 59 kg.",
    },
    {
        "question_text": "The average of 11, 13, 15, 17 and 19 is?",
        "option_a": "14",
        "option_b": "15",
        "option_c": "16",
        "option_d": "17",
        "correct_option": "B",
        "explanation": "Average = 75 / 5 = 15.",
    },
    {
        "question_text": "The average monthly income of 4 people is ₹25,000. If a fifth person joins, the average becomes ₹26,000. What is the fifth person's income?",
        "option_a": "₹28,000",
        "option_b": "₹30,000",
        "option_c": "₹32,000",
        "option_d": "₹34,000",
        "correct_option": "B",
        "explanation": "Old total = ₹100,000. New total = ₹130,000. Fifth income = ₹30,000.",
    },
    {
        "question_text": "The average of 6 numbers is 20. What is the sum of those numbers?",
        "option_a": "100",
        "option_b": "110",
        "option_c": "120",
        "option_d": "130",
        "correct_option": "C",
        "explanation": "Sum = Average × Number of values = 20 × 6 = 120.",
    },
    {
        "question_text": "The average of 4 numbers is 35. Three of the numbers are 20, 30 and 40. Find the fourth number.",
        "option_a": "45",
        "option_b": "50",
        "option_c": "55",
        "option_d": "60",
        "correct_option": "B",
        "explanation": "Required total = 140. Known total = 90. Fourth number = 50.",
    },
    {
        "question_text": "The average age of 10 students is 16 years. If a student aged 18 years is replaced by another student aged 20 years, what is the new average?",
        "option_a": "16.0 years",
        "option_b": "16.2 years",
        "option_c": "16.5 years",
        "option_d": "17.0 years",
        "correct_option": "B",
        "explanation": "Total increases by 2. Average increases by 2 / 10 = 0.2. New average = 16.2 years.",
    },
    {
        "question_text": "The average of 5 numbers is 28. If the average of the first 4 numbers is 25, what is the fifth number?",
        "option_a": "36",
        "option_b": "38",
        "option_c": "40",
        "option_d": "42",
        "correct_option": "C",
        "explanation": "Total of 5 = 140. Total of first 4 = 100. Fifth number = 40.",
    },
    {
        "question_text": "The average of 7 numbers is 30. If one more number 38 is added, what is the new average?",
        "option_a": "30",
        "option_b": "31",
        "option_c": "32",
        "option_d": "33",
        "correct_option": "B",
        "explanation": "Old total = 210. New total = 248. Average = 248 / 8 = 31.",
    },
]


created = 0
skipped = 0

for data in questions:
    exists = Question.objects.filter(
        subject=subject,
        topic=topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        skipped += 1
        print("Skipped duplicate:", data["question_text"][:50])
        continue

    Question.objects.create(
        subject=subject,
        topic=topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=2,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    created += 1


print(f"\nCreated: {created}")
print(f"Skipped: {skipped}")
print("QA -> Average -> Level 2 seeding complete.")

level3_questions = [
    {
        "question_text": "The average of 12 numbers is 36. If the average of the first 7 numbers is 32 and the average of the last 4 numbers is 41, find the eighth number.",
        "option_a": "42",
        "option_b": "44",
        "option_c": "46",
        "option_d": "48",
        "correct_option": "B",
        "explanation": "Total of 12 = 432. First 7 total = 224. Last 4 total = 164. Eighth number = 432 - 224 - 164 = 44.",
    },
    {
        "question_text": "The average age of 20 students is 18 years. If the teacher's age is included, the average increases by 1 year. What is the teacher's age?",
        "option_a": "36 years",
        "option_b": "38 years",
        "option_c": "39 years",
        "option_d": "40 years",
        "correct_option": "C",
        "explanation": "Students total = 20 × 18 = 360. New total = 21 × 19 = 399. Teacher's age = 39 years.",
    },
    {
        "question_text": "The average of 25 numbers is 48. Later it was found that 36 was wrongly entered as 63. What is the correct average?",
        "option_a": "46.72",
        "option_b": "46.92",
        "option_c": "47.12",
        "option_d": "47.28",
        "correct_option": "B",
        "explanation": "Wrong total = 1200. Correct total = 1200 - 63 + 36 = 1173. Correct average = 1173 / 25 = 46.92.",
    },
    {
        "question_text": "The average marks of 15 students is 64. The average of the first 5 students is 60. What is the average of the remaining 10 students?",
        "option_a": "64",
        "option_b": "65",
        "option_c": "66",
        "option_d": "68",
        "correct_option": "C",
        "explanation": "Total = 15 × 64 = 960. First 5 total = 300. Remaining total = 660. Average = 660 / 10 = 66.",
    },
    {
        "question_text": "The average of 10 numbers is 50. If the largest number, 80, is replaced by 60, what is the new average?",
        "option_a": "46",
        "option_b": "47",
        "option_c": "48",
        "option_d": "49",
        "correct_option": "C",
        "explanation": "Total decreases by 20. Average decreases by 20 / 10 = 2. New average = 48.",
    },
    {
        "question_text": "The average of 5 consecutive multiples of 6 is 42. What is the largest number?",
        "option_a": "48",
        "option_b": "54",
        "option_c": "60",
        "option_d": "66",
        "correct_option": "B",
        "explanation": "The numbers are 30, 36, 42, 48 and 54. Largest = 54.",
    },
    {
        "question_text": "The average of 8 numbers is 28. If each of the first 4 numbers is increased by 2 and each of the remaining 4 numbers is decreased by 1, what is the new average?",
        "option_a": "28",
        "option_b": "28.5",
        "option_c": "29",
        "option_d": "29.5",
        "correct_option": "B",
        "explanation": "Total change = (4 × 2) - (4 × 1) = 4. Average increases by 4 / 8 = 0.5. New average = 28.5.",
    },
    {
        "question_text": "The average of A and B is 35, the average of B and C is 40, and the average of A and C is 45. What is the average of A, B and C?",
        "option_a": "38",
        "option_b": "40",
        "option_c": "42",
        "option_d": "45",
        "correct_option": "B",
        "explanation": "A+B=70, B+C=80, A+C=90. Adding gives 2(A+B+C)=240, so total=120 and average=40.",
    },
    {
        "question_text": "The average of 30 numbers is 72. If two numbers 50 and 70 are removed, what is the average of the remaining 28 numbers?",
        "option_a": "72",
        "option_b": "72.5",
        "option_c": "72.86",
        "option_d": "73",
        "correct_option": "C",
        "explanation": "Total = 2160. Remaining total = 2040. Average = 2040 / 28 ≈ 72.86.",
    },
    {
        "question_text": "The average monthly salary of 12 employees is ₹40,000. If the manager's salary is included, the average becomes ₹45,000. What is the manager's salary?",
        "option_a": "₹95,000",
        "option_b": "₹100,000",
        "option_c": "₹105,000",
        "option_d": "₹110,000",
        "correct_option": "C",
        "explanation": "Employees total = ₹480,000. New total = 13 × ₹45,000 = ₹585,000. Manager salary = ₹105,000.",
    },
    {
        "question_text": "The average of 9 consecutive integers is 37. What is the sum of the smallest and largest integers?",
        "option_a": "72",
        "option_b": "74",
        "option_c": "76",
        "option_d": "78",
        "correct_option": "B",
        "explanation": "Numbers range from 33 to 41. Smallest + largest = 33 + 41 = 74.",
    },
    {
        "question_text": "The average of 6 numbers is 25. If one number is excluded, the average becomes 22. The excluded number is?",
        "option_a": "35",
        "option_b": "38",
        "option_c": "40",
        "option_d": "42",
        "correct_option": "C",
        "explanation": "Original total = 150. Remaining total = 5 × 22 = 110. Excluded number = 40.",
    },
    {
        "question_text": "The average age of a family of 6 members is 24 years. If the youngest member aged 4 years is excluded, what is the average age of the remaining members?",
        "option_a": "26 years",
        "option_b": "27 years",
        "option_c": "28 years",
        "option_d": "29 years",
        "correct_option": "C",
        "explanation": "Total age = 144. Remaining total = 140. Average = 140 / 5 = 28 years.",
    },
    {
        "question_text": "The average of 40 observations is 35. If an observation 25 is replaced by 65, what will be the new average?",
        "option_a": "35.5",
        "option_b": "36",
        "option_c": "36.5",
        "option_d": "37",
        "correct_option": "B",
        "explanation": "Total increases by 40. Average increases by 40 / 40 = 1. New average = 36.",
    },
    {
        "question_text": "The average of three numbers is 52. The first number is twice the second and the third is 12 more than the second. Find the second number.",
        "option_a": "32",
        "option_b": "34",
        "option_c": "36",
        "option_d": "38",
        "correct_option": "C",
        "explanation": "Let second = x. Then 2x + x + (x+12) = 156. So 4x = 144 and x = 36.",
    },
    {
        "question_text": "The average of 11 results is 50. If the average of the first 6 results is 49 and that of the last 6 results is 52, find the sixth result.",
        "option_a": "54",
        "option_b": "55",
        "option_c": "56",
        "option_d": "57",
        "correct_option": "C",
        "explanation": "First 6 total = 294, last 6 total = 312, all 11 total = 550. Sixth result = 294 + 312 - 550 = 56.",
    },
    {
        "question_text": "The average of 20 numbers is 30. If every number is increased by 10% of its value, what is the new average?",
        "option_a": "31",
        "option_b": "32",
        "option_c": "33",
        "option_d": "34",
        "correct_option": "C",
        "explanation": "Increasing every value by 10% increases the average by 10%. New average = 30 × 1.10 = 33.",
    },
    {
        "question_text": "A batsman has an average of 48 runs after 25 innings. How many runs must he score in the next innings to increase his average to 50?",
        "option_a": "90",
        "option_b": "95",
        "option_c": "100",
        "option_d": "105",
        "correct_option": "C",
        "explanation": "Current runs = 25 × 48 = 1200. Required total = 26 × 50 = 1300. Required runs = 100.",
    },
    {
        "question_text": "The average temperature from Monday to Wednesday is 30°C and from Tuesday to Thursday is 32°C. If Monday's temperature is 28°C, what is Thursday's temperature?",
        "option_a": "32°C",
        "option_b": "33°C",
        "option_c": "34°C",
        "option_d": "35°C",
        "correct_option": "C",
        "explanation": "M+T+W=90 and T+W+Th=96. Therefore Th - M = 6. Thursday = 28 + 6 = 34°C.",
    },
    {
        "question_text": "The average of 7 numbers is 45. The average of the first 3 numbers is 40 and that of the last 3 numbers is 50. What is the fourth number?",
        "option_a": "40",
        "option_b": "42",
        "option_c": "45",
        "option_d": "48",
        "correct_option": "C",
        "explanation": "Total = 315. First 3 total = 120 and last 3 total = 150. Fourth number = 315 - 270 = 45.",
    },
    {
        "question_text": "The average of 18 numbers is 44. If the average of 8 of them is 40, what is the average of the remaining 10 numbers?",
        "option_a": "46",
        "option_b": "46.8",
        "option_c": "47.2",
        "option_d": "48",
        "correct_option": "C",
        "explanation": "Total = 792. First group total = 320. Remaining total = 472. Average = 472 / 10 = 47.2.",
    },
    {
        "question_text": "The average weight of 10 boys is 45 kg and the average weight of 15 girls is 40 kg. What is the average weight of all 25 students?",
        "option_a": "41 kg",
        "option_b": "42 kg",
        "option_c": "42.5 kg",
        "option_d": "43 kg",
        "correct_option": "B",
        "explanation": "Total weight = 10×45 + 15×40 = 1050 kg. Average = 1050 / 25 = 42 kg.",
    },
    {
        "question_text": "The average of five numbers is 60. If one number is 20 more than the average and another is 10 less than the average, what is the average of the remaining three numbers?",
        "option_a": "55",
        "option_b": "56.67",
        "option_c": "58",
        "option_d": "60",
        "correct_option": "B",
        "explanation": "Total = 300. Two numbers are 80 and 50, total 130. Remaining total = 170. Average = 170 / 3 ≈ 56.67.",
    },
    {
        "question_text": "The average of 50 numbers is 38. If two numbers 45 and 55 are replaced by 35 and 40 respectively, what is the new average?",
        "option_a": "37",
        "option_b": "37.5",
        "option_c": "38",
        "option_d": "38.5",
        "correct_option": "B",
        "explanation": "Original total = 1900. Total decreases by 25. New total = 1875. New average = 1875 / 50 = 37.5.",
    },
    {
        "question_text": "The average age of 8 persons increases by 2 years when a person aged 24 years is replaced by another person. What is the age of the new person?",
        "option_a": "36 years",
        "option_b": "38 years",
        "option_c": "40 years",
        "option_d": "42 years",
        "correct_option": "C",
        "explanation": "Total age increases by 8 × 2 = 16 years. New person's age = 24 + 16 = 40 years.",
    },
]

created_l3 = 0
skipped_l3 = 0

for data in level3_questions:
    exists = Question.objects.filter(
        subject=subject,
        topic=topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        skipped_l3 += 1
        print("Skipped duplicate:", data["question_text"][:50])
        continue

    Question.objects.create(
        subject=subject,
        topic=topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=3,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    created_l3 += 1

print(f"\nLevel 3 Created: {created_l3}")
print(f"Level 3 Skipped: {skipped_l3}")
print("QA -> Average -> Level 3 seeding complete.")

# =========================================================
# QA -> Ratio & Proportion -> Level 1
# =========================================================

ratio_subject = Subject.objects.get(name="QA")
ratio_topic = Topic.objects.get(
    subject=ratio_subject,
    name="Ratio & Proportion"
)

ratio_level1_questions = [
    {
        "question_text": "What is the ratio of 20 to 30 in simplest form?",
        "option_a": "1:2",
        "option_b": "2:3",
        "option_c": "3:2",
        "option_d": "4:5",
        "correct_option": "B",
        "explanation": "20:30 = 2:3 after dividing both terms by 10.",
    },
    {
        "question_text": "Simplify the ratio 24:36.",
        "option_a": "2:3",
        "option_b": "3:4",
        "option_c": "4:5",
        "option_d": "1:2",
        "correct_option": "A",
        "explanation": "24:36 = 2:3 after dividing by 12.",
    },
    {
        "question_text": "If A:B = 3:5 and A = 15, what is B?",
        "option_a": "20",
        "option_b": "25",
        "option_c": "30",
        "option_d": "35",
        "correct_option": "B",
        "explanation": "3 parts = 15, so 1 part = 5. B = 5 × 5 = 25.",
    },
    {
        "question_text": "If the ratio of boys to girls is 2:3 and there are 20 boys, how many girls are there?",
        "option_a": "25",
        "option_b": "30",
        "option_c": "35",
        "option_d": "40",
        "correct_option": "B",
        "explanation": "2 parts = 20, so 1 part = 10. Girls = 3 × 10 = 30.",
    },
    {
        "question_text": "Divide 60 in the ratio 2:3. What is the larger part?",
        "option_a": "24",
        "option_b": "30",
        "option_c": "36",
        "option_d": "40",
        "correct_option": "C",
        "explanation": "Total parts = 5. Larger part = 60 × 3/5 = 36.",
    },
    {
        "question_text": "The ratio of two numbers is 4:7. If the smaller number is 20, what is the larger number?",
        "option_a": "30",
        "option_b": "35",
        "option_c": "40",
        "option_d": "45",
        "correct_option": "B",
        "explanation": "4 parts = 20, so 1 part = 5. Larger number = 7 × 5 = 35.",
    },
    {
        "question_text": "What is the ratio of 45 minutes to 1 hour?",
        "option_a": "3:4",
        "option_b": "4:3",
        "option_c": "2:3",
        "option_d": "1:2",
        "correct_option": "A",
        "explanation": "1 hour = 60 minutes. Ratio = 45:60 = 3:4.",
    },
    {
        "question_text": "What is the ratio of 2 kg to 500 g?",
        "option_a": "2:1",
        "option_b": "3:1",
        "option_c": "4:1",
        "option_d": "5:1",
        "correct_option": "C",
        "explanation": "2 kg = 2000 g. Ratio = 2000:500 = 4:1.",
    },
    {
        "question_text": "If x:y = 5:8 and y = 40, find x.",
        "option_a": "20",
        "option_b": "25",
        "option_c": "30",
        "option_d": "35",
        "correct_option": "B",
        "explanation": "8 parts = 40, so 1 part = 5. x = 5 × 5 = 25.",
    },
    {
        "question_text": "If 3:4 = 12:x, find x.",
        "option_a": "14",
        "option_b": "15",
        "option_c": "16",
        "option_d": "18",
        "correct_option": "C",
        "explanation": "3/4 = 12/x. Therefore 3x = 48 and x = 16.",
    },
    {
        "question_text": "The ratio of red balls to blue balls is 3:2. If there are 15 red balls, how many blue balls are there?",
        "option_a": "8",
        "option_b": "10",
        "option_c": "12",
        "option_d": "15",
        "correct_option": "B",
        "explanation": "3 parts = 15, so 1 part = 5. Blue balls = 2 × 5 = 10.",
    },
    {
        "question_text": "Two numbers are in the ratio 5:6 and their sum is 55. Find the smaller number.",
        "option_a": "20",
        "option_b": "25",
        "option_c": "30",
        "option_d": "35",
        "correct_option": "B",
        "explanation": "Total parts = 11. One part = 55/11 = 5. Smaller number = 5 × 5 = 25.",
    },
    {
        "question_text": "Two numbers are in the ratio 3:7 and their sum is 50. Find the larger number.",
        "option_a": "30",
        "option_b": "35",
        "option_c": "40",
        "option_d": "45",
        "correct_option": "B",
        "explanation": "Total parts = 10. One part = 5. Larger number = 7 × 5 = 35.",
    },
    {
        "question_text": "If A:B = 2:5, what fraction of the total is A?",
        "option_a": "2/5",
        "option_b": "2/7",
        "option_c": "5/7",
        "option_d": "3/7",
        "correct_option": "B",
        "explanation": "Total parts = 2 + 5 = 7. A represents 2/7 of the total.",
    },
    {
        "question_text": "If A:B = 4:3, what fraction of the total is B?",
        "option_a": "3/4",
        "option_b": "4/7",
        "option_c": "3/7",
        "option_d": "1/3",
        "correct_option": "C",
        "explanation": "Total parts = 7. B represents 3/7 of the total.",
    },
    {
        "question_text": "The ratio of ₹40 to ₹100 is?",
        "option_a": "1:2",
        "option_b": "2:5",
        "option_c": "3:5",
        "option_d": "4:5",
        "correct_option": "B",
        "explanation": "40:100 = 2:5 after dividing by 20.",
    },
    {
        "question_text": "Simplify the ratio 18:27.",
        "option_a": "2:3",
        "option_b": "3:4",
        "option_c": "4:5",
        "option_d": "5:6",
        "correct_option": "A",
        "explanation": "18:27 = 2:3 after dividing by 9.",
    },
    {
        "question_text": "If 5 pens cost ₹50 and 8 pens cost ₹x at the same rate, find x.",
        "option_a": "₹70",
        "option_b": "₹75",
        "option_c": "₹80",
        "option_d": "₹85",
        "correct_option": "C",
        "explanation": "Cost per pen = ₹10. Cost of 8 pens = ₹80.",
    },
    {
        "question_text": "If 4 books cost ₹200, what will 6 books cost at the same rate?",
        "option_a": "₹250",
        "option_b": "₹280",
        "option_c": "₹300",
        "option_d": "₹320",
        "correct_option": "C",
        "explanation": "Cost per book = ₹50. Cost of 6 books = ₹300.",
    },
    {
        "question_text": "If 6 workers complete a task in 10 days, how many worker-days are required?",
        "option_a": "50",
        "option_b": "60",
        "option_c": "70",
        "option_d": "80",
        "correct_option": "B",
        "explanation": "Worker-days = 6 × 10 = 60.",
    },
    {
        "question_text": "The ratio of 75 cm to 1.5 m is?",
        "option_a": "1:2",
        "option_b": "2:3",
        "option_c": "3:4",
        "option_d": "1:3",
        "correct_option": "A",
        "explanation": "1.5 m = 150 cm. Ratio = 75:150 = 1:2.",
    },
    {
        "question_text": "The ratio of 250 ml to 1 litre is?",
        "option_a": "1:2",
        "option_b": "1:3",
        "option_c": "1:4",
        "option_d": "2:5",
        "correct_option": "C",
        "explanation": "1 litre = 1000 ml. Ratio = 250:1000 = 1:4.",
    },
    {
        "question_text": "If a:b = 7:9 and a = 35, find b.",
        "option_a": "40",
        "option_b": "45",
        "option_c": "50",
        "option_d": "55",
        "correct_option": "B",
        "explanation": "7 parts = 35, so 1 part = 5. b = 9 × 5 = 45.",
    },
    {
        "question_text": "If 8:x = 4:7, find x.",
        "option_a": "12",
        "option_b": "14",
        "option_c": "16",
        "option_d": "18",
        "correct_option": "B",
        "explanation": "8/x = 4/7. Therefore 4x = 56 and x = 14.",
    },
    {
        "question_text": "A sum of ₹90 is divided between A and B in the ratio 4:5. How much does B receive?",
        "option_a": "₹40",
        "option_b": "₹45",
        "option_c": "₹50",
        "option_d": "₹55",
        "correct_option": "C",
        "explanation": "Total parts = 9. One part = ₹10. B receives 5 × ₹10 = ₹50.",
    },
]

ratio_l1_created = 0
ratio_l1_skipped = 0

for data in ratio_level1_questions:
    exists = Question.objects.filter(
        subject=ratio_subject,
        topic=ratio_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        ratio_l1_skipped += 1
        print("Skipped duplicate:", data["question_text"][:50])
        continue

    Question.objects.create(
        subject=ratio_subject,
        topic=ratio_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=1,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    ratio_l1_created += 1


print(f"\nRatio Level 1 Created: {ratio_l1_created}")
print(f"Ratio Level 1 Skipped: {ratio_l1_skipped}")
print("QA -> Ratio & Proportion -> Level 1 seeding complete.")

# =========================================================
# QA -> Ratio & Proportion -> Level 2
# =========================================================

ratio_level2_questions = [
    {
        "question_text": "Two numbers are in the ratio 4:7. If their difference is 24, find the larger number.",
        "option_a": "48",
        "option_b": "56",
        "option_c": "64",
        "option_d": "72",
        "correct_option": "B",
        "explanation": "Difference = 3 parts = 24, so 1 part = 8. Larger number = 7 × 8 = 56.",
    },
    {
        "question_text": "The ratio of boys to girls in a class is 5:4. If the total number of students is 45, how many girls are there?",
        "option_a": "18",
        "option_b": "20",
        "option_c": "22",
        "option_d": "25",
        "correct_option": "B",
        "explanation": "Total parts = 9. One part = 45/9 = 5. Girls = 4 × 5 = 20.",
    },
    {
        "question_text": "If A:B = 3:4 and B:C = 2:5, find A:B:C.",
        "option_a": "3:4:10",
        "option_b": "3:8:20",
        "option_c": "6:8:20",
        "option_d": "6:4:10",
        "correct_option": "C",
        "explanation": "Make B equal: A:B = 6:8 and B:C = 8:20. Therefore A:B:C = 6:8:20.",
    },
    {
        "question_text": "A sum of ₹840 is divided among A, B and C in the ratio 2:3:5. How much does C receive?",
        "option_a": "₹360",
        "option_b": "₹400",
        "option_c": "₹420",
        "option_d": "₹440",
        "correct_option": "C",
        "explanation": "Total parts = 10. C receives 5/10 × 840 = ₹420.",
    },
    {
        "question_text": "If 12 men can complete a work in 15 days, how many days will 20 men take, assuming the same efficiency?",
        "option_a": "8 days",
        "option_b": "9 days",
        "option_c": "10 days",
        "option_d": "12 days",
        "correct_option": "B",
        "explanation": "Men × days is constant. 12 × 15 = 20 × x, so x = 9 days.",
    },
    {
        "question_text": "If 8 machines produce 400 units in a day, how many units will 12 machines produce at the same rate?",
        "option_a": "500",
        "option_b": "550",
        "option_c": "600",
        "option_d": "650",
        "correct_option": "C",
        "explanation": "Units per machine = 400/8 = 50. For 12 machines = 12 × 50 = 600.",
    },
    {
        "question_text": "Two numbers are in the ratio 7:9. If their sum is 128, find the smaller number.",
        "option_a": "52",
        "option_b": "56",
        "option_c": "60",
        "option_d": "63",
        "correct_option": "B",
        "explanation": "Total parts = 16. One part = 128/16 = 8. Smaller number = 7 × 8 = 56.",
    },
    {
        "question_text": "If x:y = 4:5 and y:z = 10:3, find x:z.",
        "option_a": "4:3",
        "option_b": "8:3",
        "option_c": "5:3",
        "option_d": "10:3",
        "correct_option": "B",
        "explanation": "x:y = 8:10 and y:z = 10:3. Therefore x:z = 8:3.",
    },
    {
        "question_text": "The ratio of income to expenditure of a person is 5:4. If the income is ₹25,000, find the savings.",
        "option_a": "₹4,000",
        "option_b": "₹5,000",
        "option_c": "₹6,000",
        "option_d": "₹7,000",
        "correct_option": "B",
        "explanation": "5 parts = ₹25,000, so 1 part = ₹5,000. Expenditure = ₹20,000. Savings = ₹5,000.",
    },
    {
        "question_text": "A mixture contains milk and water in the ratio 7:3. If the total mixture is 50 litres, how much water is present?",
        "option_a": "10 litres",
        "option_b": "15 litres",
        "option_c": "20 litres",
        "option_d": "25 litres",
        "correct_option": "B",
        "explanation": "Total parts = 10. Water = 3/10 × 50 = 15 litres.",
    },
    {
        "question_text": "If 5 notebooks cost ₹120, what will 8 notebooks cost at the same rate?",
        "option_a": "₹180",
        "option_b": "₹192",
        "option_c": "₹200",
        "option_d": "₹210",
        "correct_option": "B",
        "explanation": "Cost per notebook = ₹24. Cost of 8 = 8 × 24 = ₹192.",
    },
    {
        "question_text": "Two quantities are in the ratio 3:5. If both are increased by 10, the ratio becomes 5:7. Find the smaller quantity.",
        "option_a": "10",
        "option_b": "15",
        "option_c": "20",
        "option_d": "25",
        "correct_option": "B",
        "explanation": "Let quantities be 3x and 5x. (3x+10)/(5x+10)=5/7 gives x=5. Smaller quantity = 15.",
    },
    {
        "question_text": "The ratio of present ages of A and B is 4:5. If A is 24 years old, what is B's age?",
        "option_a": "28 years",
        "option_b": "30 years",
        "option_c": "32 years",
        "option_d": "35 years",
        "correct_option": "B",
        "explanation": "4 parts = 24, so 1 part = 6. B = 5 × 6 = 30 years.",
    },
    {
        "question_text": "The ratio of two numbers is 5:8. If 6 is added to each number, the ratio becomes 2:3. Find the smaller number.",
        "option_a": "15",
        "option_b": "18",
        "option_c": "20",
        "option_d": "25",
        "correct_option": "B",
        "explanation": "Let numbers be 5x and 8x. (5x+6)/(8x+6)=2/3 gives x=3.6, so smaller = 18.",
    },
    {
        "question_text": "A and B invest money in the ratio 3:5. If the total investment is ₹64,000, what is B's investment?",
        "option_a": "₹24,000",
        "option_b": "₹32,000",
        "option_c": "₹40,000",
        "option_d": "₹48,000",
        "correct_option": "C",
        "explanation": "Total parts = 8. B = 5/8 × 64,000 = ₹40,000.",
    },
    {
        "question_text": "If 16 workers complete a task in 12 days, how many workers are required to complete it in 8 days?",
        "option_a": "20",
        "option_b": "22",
        "option_c": "24",
        "option_d": "26",
        "correct_option": "C",
        "explanation": "Workers × days is constant. 16 × 12 = x × 8, so x = 24.",
    },
    {
        "question_text": "The ratio of two numbers is 9:11. If the larger number is 55, find the smaller number.",
        "option_a": "40",
        "option_b": "45",
        "option_c": "50",
        "option_d": "54",
        "correct_option": "B",
        "explanation": "11 parts = 55, so 1 part = 5. Smaller number = 9 × 5 = 45.",
    },
    {
        "question_text": "If A:B = 2:3, B:C = 4:5 and C:D = 10:7, find A:D.",
        "option_a": "8:7",
        "option_b": "16:21",
        "option_c": "8:21",
        "option_d": "16:7",
        "correct_option": "B",
        "explanation": "Combining ratios gives A:B:C:D = 16:24:30:21. Therefore A:D = 16:21.",
    },
    {
        "question_text": "The ratio of speed of A to B is 3:4. If A travels at 45 km/h, what is B's speed?",
        "option_a": "50 km/h",
        "option_b": "55 km/h",
        "option_c": "60 km/h",
        "option_d": "65 km/h",
        "correct_option": "C",
        "explanation": "3 parts = 45, so 1 part = 15. B = 4 × 15 = 60 km/h.",
    },
    {
        "question_text": "A recipe requires flour and sugar in the ratio 5:2. If 750 g of flour is used, how much sugar is needed?",
        "option_a": "250 g",
        "option_b": "300 g",
        "option_c": "350 g",
        "option_d": "400 g",
        "correct_option": "B",
        "explanation": "5 parts = 750 g, so 1 part = 150 g. Sugar = 2 × 150 = 300 g.",
    },
    {
        "question_text": "If 3 kg of apples cost ₹180, how much will 7 kg cost at the same rate?",
        "option_a": "₹360",
        "option_b": "₹400",
        "option_c": "₹420",
        "option_d": "₹450",
        "correct_option": "C",
        "explanation": "Cost per kg = ₹60. Cost of 7 kg = ₹420.",
    },
    {
        "question_text": "The ratio of two numbers is 6:11. If the difference between them is 35, find their sum.",
        "option_a": "105",
        "option_b": "112",
        "option_c": "119",
        "option_d": "126",
        "correct_option": "C",
        "explanation": "Difference = 5 parts = 35, so 1 part = 7. Sum = 17 × 7 = 119.",
    },
    {
        "question_text": "If a:b = 4:7 and b:c = 14:15, find a:b:c.",
        "option_a": "8:14:15",
        "option_b": "4:14:15",
        "option_c": "8:7:15",
        "option_d": "4:7:15",
        "correct_option": "A",
        "explanation": "a:b = 8:14 and b:c = 14:15. Therefore a:b:c = 8:14:15.",
    },
    {
        "question_text": "A bag contains red, blue and green balls in the ratio 2:3:5. If there are 50 balls in total, how many blue balls are there?",
        "option_a": "10",
        "option_b": "15",
        "option_c": "20",
        "option_d": "25",
        "correct_option": "B",
        "explanation": "Total parts = 10. Blue balls = 3/10 × 50 = 15.",
    },
    {
        "question_text": "If 15 litres of fuel are required to travel 180 km, how much fuel is required to travel 300 km at the same rate?",
        "option_a": "20 litres",
        "option_b": "22 litres",
        "option_c": "25 litres",
        "option_d": "28 litres",
        "correct_option": "C",
        "explanation": "Fuel required = 15 × 300 / 180 = 25 litres.",
    },
]

ratio_l2_created = 0
ratio_l2_skipped = 0

for data in ratio_level2_questions:
    exists = Question.objects.filter(
        subject=ratio_subject,
        topic=ratio_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        ratio_l2_skipped += 1
        continue

    Question.objects.create(
        subject=ratio_subject,
        topic=ratio_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=2,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    ratio_l2_created += 1

print(f"\nRatio Level 2 Created: {ratio_l2_created}")
print(f"Ratio Level 2 Skipped: {ratio_l2_skipped}")
print("QA -> Ratio & Proportion -> Level 2 seeding complete.")

# =========================================================
# QA -> Profit & Loss -> Level 1
# =========================================================

profit_subject = Subject.objects.get(name="QA")
profit_topic = Topic.objects.get(
    subject=profit_subject,
    name="Profit & Loss"
)

profit_level1_questions = [
    {
        "question_text": "A shopkeeper buys an item for ₹100 and sells it for ₹120. What is the profit?",
        "option_a": "₹10",
        "option_b": "₹20",
        "option_c": "₹25",
        "option_d": "₹30",
        "correct_option": "B",
        "explanation": "Profit = Selling Price - Cost Price = 120 - 100 = ₹20.",
    },
    {
        "question_text": "An item is bought for ₹250 and sold for ₹225. What is the loss?",
        "option_a": "₹20",
        "option_b": "₹25",
        "option_c": "₹30",
        "option_d": "₹35",
        "correct_option": "B",
        "explanation": "Loss = Cost Price - Selling Price = 250 - 225 = ₹25.",
    },
    {
        "question_text": "A product costs ₹500 and is sold for ₹600. Find the profit percentage.",
        "option_a": "10%",
        "option_b": "15%",
        "option_c": "20%",
        "option_d": "25%",
        "correct_option": "C",
        "explanation": "Profit = ₹100. Profit% = 100/500 × 100 = 20%.",
    },
    {
        "question_text": "An article is purchased for ₹400 and sold for ₹360. Find the loss percentage.",
        "option_a": "5%",
        "option_b": "10%",
        "option_c": "15%",
        "option_d": "20%",
        "correct_option": "B",
        "explanation": "Loss = ₹40. Loss% = 40/400 × 100 = 10%.",
    },
    {
        "question_text": "If the cost price of an item is ₹800 and profit is ₹200, what is the selling price?",
        "option_a": "₹900",
        "option_b": "₹950",
        "option_c": "₹1000",
        "option_d": "₹1100",
        "correct_option": "C",
        "explanation": "Selling Price = Cost Price + Profit = 800 + 200 = ₹1000.",
    },
    {
        "question_text": "If the cost price is ₹750 and the loss is ₹50, what is the selling price?",
        "option_a": "₹650",
        "option_b": "₹700",
        "option_c": "₹725",
        "option_d": "₹800",
        "correct_option": "B",
        "explanation": "Selling Price = Cost Price - Loss = 750 - 50 = ₹700.",
    },
    {
        "question_text": "A book is sold for ₹330 at a profit of ₹30. What is its cost price?",
        "option_a": "₹280",
        "option_b": "₹290",
        "option_c": "₹300",
        "option_d": "₹310",
        "correct_option": "C",
        "explanation": "Cost Price = Selling Price - Profit = 330 - 30 = ₹300.",
    },
    {
        "question_text": "An item is sold for ₹450 at a loss of ₹50. Find its cost price.",
        "option_a": "₹450",
        "option_b": "₹475",
        "option_c": "₹500",
        "option_d": "₹550",
        "correct_option": "C",
        "explanation": "Cost Price = Selling Price + Loss = 450 + 50 = ₹500.",
    },
    {
        "question_text": "A pen is bought for ₹20 and sold for ₹25. What is the profit percentage?",
        "option_a": "20%",
        "option_b": "25%",
        "option_c": "30%",
        "option_d": "35%",
        "correct_option": "B",
        "explanation": "Profit = ₹5. Profit% = 5/20 × 100 = 25%.",
    },
    {
        "question_text": "A toy is bought for ₹200 and sold for ₹180. What is the loss percentage?",
        "option_a": "5%",
        "option_b": "10%",
        "option_c": "15%",
        "option_d": "20%",
        "correct_option": "B",
        "explanation": "Loss = ₹20. Loss% = 20/200 × 100 = 10%.",
    },
    {
        "question_text": "If an article costs ₹600 and is sold at a profit of 10%, what is the selling price?",
        "option_a": "₹620",
        "option_b": "₹640",
        "option_c": "₹660",
        "option_d": "₹680",
        "correct_option": "C",
        "explanation": "Profit = 10% of ₹600 = ₹60. Selling price = ₹660.",
    },
    {
        "question_text": "An item costs ₹500 and is sold at a loss of 20%. Find the selling price.",
        "option_a": "₹350",
        "option_b": "₹400",
        "option_c": "₹425",
        "option_d": "₹450",
        "correct_option": "B",
        "explanation": "Loss = 20% of ₹500 = ₹100. Selling price = ₹400.",
    },
    {
        "question_text": "A bicycle costs ₹4000 and is sold for ₹4400. What is the profit percentage?",
        "option_a": "5%",
        "option_b": "10%",
        "option_c": "15%",
        "option_d": "20%",
        "correct_option": "B",
        "explanation": "Profit = ₹400. Profit% = 400/4000 × 100 = 10%.",
    },
    {
        "question_text": "A mobile phone is bought for ₹10,000 and sold for ₹9,000. Find the loss percentage.",
        "option_a": "5%",
        "option_b": "10%",
        "option_c": "15%",
        "option_d": "20%",
        "correct_option": "B",
        "explanation": "Loss = ₹1000. Loss% = 1000/10000 × 100 = 10%.",
    },
    {
        "question_text": "A shirt is bought for ₹800 and sold at 25% profit. What is the selling price?",
        "option_a": "₹900",
        "option_b": "₹950",
        "option_c": "₹1000",
        "option_d": "₹1050",
        "correct_option": "C",
        "explanation": "Profit = 25% of ₹800 = ₹200. Selling price = ₹1000.",
    },
    {
        "question_text": "A table is bought for ₹2000 and sold at 15% loss. What is the selling price?",
        "option_a": "₹1600",
        "option_b": "₹1700",
        "option_c": "₹1800",
        "option_d": "₹1900",
        "correct_option": "B",
        "explanation": "Loss = 15% of ₹2000 = ₹300. Selling price = ₹1700.",
    },
    {
        "question_text": "A trader earns ₹150 profit on an item costing ₹750. What is the profit percentage?",
        "option_a": "10%",
        "option_b": "15%",
        "option_c": "20%",
        "option_d": "25%",
        "correct_option": "C",
        "explanation": "Profit% = 150/750 × 100 = 20%.",
    },
    {
        "question_text": "A seller loses ₹120 on an article costing ₹600. What is the loss percentage?",
        "option_a": "10%",
        "option_b": "15%",
        "option_c": "20%",
        "option_d": "25%",
        "correct_option": "C",
        "explanation": "Loss% = 120/600 × 100 = 20%.",
    },
    {
        "question_text": "If an item is sold for ₹960 at 20% profit, what is its cost price?",
        "option_a": "₹750",
        "option_b": "₹800",
        "option_c": "₹850",
        "option_d": "₹900",
        "correct_option": "B",
        "explanation": "Selling price = 120% of cost price. Cost price = 960/1.2 = ₹800.",
    },
    {
        "question_text": "An article is sold for ₹720 at a loss of 10%. Find its cost price.",
        "option_a": "₹750",
        "option_b": "₹800",
        "option_c": "₹820",
        "option_d": "₹850",
        "correct_option": "B",
        "explanation": "Selling price = 90% of cost price. Cost price = 720/0.9 = ₹800.",
    },
    {
        "question_text": "A fruit seller buys oranges for ₹300 and sells them for ₹360. What is the profit?",
        "option_a": "₹40",
        "option_b": "₹50",
        "option_c": "₹60",
        "option_d": "₹70",
        "correct_option": "C",
        "explanation": "Profit = ₹360 - ₹300 = ₹60.",
    },
    {
        "question_text": "A watch bought for ₹1500 is sold for ₹1350. What is the loss?",
        "option_a": "₹100",
        "option_b": "₹150",
        "option_c": "₹200",
        "option_d": "₹250",
        "correct_option": "B",
        "explanation": "Loss = ₹1500 - ₹1350 = ₹150.",
    },
    {
        "question_text": "A product bought for ₹1200 is sold at 5% profit. Find the selling price.",
        "option_a": "₹1240",
        "option_b": "₹1260",
        "option_c": "₹1280",
        "option_d": "₹1300",
        "correct_option": "B",
        "explanation": "Profit = 5% of ₹1200 = ₹60. Selling price = ₹1260.",
    },
    {
        "question_text": "A product costing ₹1600 is sold at 25% loss. Find the selling price.",
        "option_a": "₹1000",
        "option_b": "₹1100",
        "option_c": "₹1200",
        "option_d": "₹1300",
        "correct_option": "C",
        "explanation": "Loss = 25% of ₹1600 = ₹400. Selling price = ₹1200.",
    },
    {
        "question_text": "A shopkeeper buys an item for ₹900 and wants a profit of 20%. At what price should he sell it?",
        "option_a": "₹1000",
        "option_b": "₹1050",
        "option_c": "₹1080",
        "option_d": "₹1100",
        "correct_option": "C",
        "explanation": "Profit = 20% of ₹900 = ₹180. Selling price = ₹1080.",
    },
]

profit_l1_created = 0
profit_l1_skipped = 0

for data in profit_level1_questions:
    exists = Question.objects.filter(
        subject=profit_subject,
        topic=profit_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        profit_l1_skipped += 1
        continue

    Question.objects.create(
        subject=profit_subject,
        topic=profit_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=1,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    profit_l1_created += 1

print(f"\nProfit & Loss Level 1 Created: {profit_l1_created}")
print(f"Profit & Loss Level 1 Skipped: {profit_l1_skipped}")
print("QA -> Profit & Loss -> Level 1 seeding complete.")

# =========================================================
# QA -> Profit & Loss -> Level 2
# =========================================================

profit_level2_questions = [
    {
        "question_text": "An article is sold for ₹960 at a profit of 20%. What is its cost price?",
        "option_a": "₹750",
        "option_b": "₹800",
        "option_c": "₹820",
        "option_d": "₹850",
        "correct_option": "B",
        "explanation": "SP = 120% of CP. CP = 960 / 1.2 = ₹800.",
    },
    {
        "question_text": "A product is sold for ₹765 at a loss of 15%. Find its cost price.",
        "option_a": "₹850",
        "option_b": "₹875",
        "option_c": "₹900",
        "option_d": "₹925",
        "correct_option": "C",
        "explanation": "SP = 85% of CP. CP = 765 / 0.85 = ₹900.",
    },
    {
        "question_text": "A shopkeeper gains 25% by selling an item for ₹1500. Find the cost price.",
        "option_a": "₹1100",
        "option_b": "₹1200",
        "option_c": "₹1250",
        "option_d": "₹1300",
        "correct_option": "B",
        "explanation": "CP = 1500 / 1.25 = ₹1200.",
    },
    {
        "question_text": "A trader sells an article at 10% loss for ₹1080. What was the cost price?",
        "option_a": "₹1150",
        "option_b": "₹1200",
        "option_c": "₹1250",
        "option_d": "₹1300",
        "correct_option": "B",
        "explanation": "SP = 90% of CP. CP = 1080 / 0.9 = ₹1200.",
    },
    {
        "question_text": "An article is bought for ₹800 and sold for ₹920. Find the profit percentage.",
        "option_a": "10%",
        "option_b": "12%",
        "option_c": "15%",
        "option_d": "20%",
        "correct_option": "C",
        "explanation": "Profit = ₹120. Profit% = 120/800 × 100 = 15%.",
    },
    {
        "question_text": "A product is purchased for ₹1250 and sold for ₹1125. Find the loss percentage.",
        "option_a": "5%",
        "option_b": "8%",
        "option_c": "10%",
        "option_d": "12%",
        "correct_option": "C",
        "explanation": "Loss = ₹125. Loss% = 125/1250 × 100 = 10%.",
    },
    {
        "question_text": "A shopkeeper sells an item for ₹1800 and earns 20% profit. What profit amount does he earn?",
        "option_a": "₹250",
        "option_b": "₹300",
        "option_c": "₹350",
        "option_d": "₹400",
        "correct_option": "B",
        "explanation": "CP = 1800/1.2 = ₹1500. Profit = ₹300.",
    },
    {
        "question_text": "A man sells a bicycle for ₹3400 at a loss of 15%. Find the loss amount.",
        "option_a": "₹500",
        "option_b": "₹600",
        "option_c": "₹650",
        "option_d": "₹700",
        "correct_option": "B",
        "explanation": "CP = 3400/0.85 = ₹4000. Loss = ₹600.",
    },
    {
        "question_text": "A shopkeeper buys an article for ₹1500 and wants a profit of 12%. What should be the selling price?",
        "option_a": "₹1620",
        "option_b": "₹1650",
        "option_c": "₹1680",
        "option_d": "₹1700",
        "correct_option": "C",
        "explanation": "SP = 1500 × 1.12 = ₹1680.",
    },
    {
        "question_text": "An article costing ₹2400 is sold at a loss of 12.5%. Find the selling price.",
        "option_a": "₹2000",
        "option_b": "₹2100",
        "option_c": "₹2150",
        "option_d": "₹2200",
        "correct_option": "B",
        "explanation": "12.5% of ₹2400 = ₹300. SP = ₹2100.",
    },
    {
        "question_text": "A seller gains 20% on an article. If the cost price increases from ₹500 to ₹600 and the same profit rate is maintained, what is the new selling price?",
        "option_a": "₹680",
        "option_b": "₹700",
        "option_c": "₹720",
        "option_d": "₹750",
        "correct_option": "C",
        "explanation": "New SP = 600 × 1.20 = ₹720.",
    },
    {
        "question_text": "A product is sold for ₹990 after a 10% loss. At what price should it be sold to earn 10% profit?",
        "option_a": "₹1100",
        "option_b": "₹1150",
        "option_c": "₹1200",
        "option_d": "₹1210",
        "correct_option": "D",
        "explanation": "CP = 990/0.9 = ₹1100. Required SP = 1100 × 1.1 = ₹1210.",
    },
    {
        "question_text": "A shopkeeper sells an article at 25% profit. If the cost price is ₹640, find the selling price.",
        "option_a": "₹760",
        "option_b": "₹780",
        "option_c": "₹800",
        "option_d": "₹820",
        "correct_option": "C",
        "explanation": "SP = 640 × 1.25 = ₹800.",
    },
    {
        "question_text": "An item is sold for ₹1440 at 20% loss. Find the cost price.",
        "option_a": "₹1600",
        "option_b": "₹1700",
        "option_c": "₹1800",
        "option_d": "₹1900",
        "correct_option": "C",
        "explanation": "SP = 80% of CP. CP = 1440/0.8 = ₹1800.",
    },
    {
        "question_text": "A trader buys 10 items for ₹2000 and sells each item for ₹240. What is his total profit?",
        "option_a": "₹300",
        "option_b": "₹350",
        "option_c": "₹400",
        "option_d": "₹450",
        "correct_option": "C",
        "explanation": "Total SP = 10 × 240 = ₹2400. Profit = 2400 - 2000 = ₹400.",
    },
    {
        "question_text": "A trader buys 20 pens for ₹500 and sells each pen for ₹22. What is the total loss?",
        "option_a": "₹40",
        "option_b": "₹50",
        "option_c": "₹60",
        "option_d": "₹70",
        "correct_option": "C",
        "explanation": "Total SP = 20 × 22 = ₹440. Loss = 500 - 440 = ₹60.",
    },
    {
        "question_text": "A man bought an item for ₹1600 and spent ₹200 on repairs. If he sold it for ₹2160, what was his profit percentage?",
        "option_a": "15%",
        "option_b": "20%",
        "option_c": "25%",
        "option_d": "30%",
        "correct_option": "B",
        "explanation": "Total CP = 1600 + 200 = ₹1800. Profit = ₹360. Profit% = 20%.",
    },
    {
        "question_text": "A shopkeeper purchases an item for ₹900 and spends ₹100 on transport. He sells it for ₹900. What is his loss percentage?",
        "option_a": "5%",
        "option_b": "10%",
        "option_c": "12%",
        "option_d": "15%",
        "correct_option": "B",
        "explanation": "Total CP = ₹1000. Loss = ₹100. Loss% = 10%.",
    },
    {
        "question_text": "An article is sold at 15% profit for ₹2300. Find its cost price.",
        "option_a": "₹1900",
        "option_b": "₹2000",
        "option_c": "₹2100",
        "option_d": "₹2200",
        "correct_option": "B",
        "explanation": "CP = 2300/1.15 = ₹2000.",
    },
    {
        "question_text": "An article is sold at 25% loss for ₹1500. Find the cost price.",
        "option_a": "₹1800",
        "option_b": "₹1900",
        "option_c": "₹2000",
        "option_d": "₹2100",
        "correct_option": "C",
        "explanation": "SP = 75% of CP. CP = 1500/0.75 = ₹2000.",
    },
    {
        "question_text": "A trader wants to earn ₹500 profit on an article costing ₹2500. What profit percentage should he earn?",
        "option_a": "15%",
        "option_b": "18%",
        "option_c": "20%",
        "option_d": "25%",
        "correct_option": "C",
        "explanation": "Profit% = 500/2500 × 100 = 20%.",
    },
    {
        "question_text": "A seller suffers a loss of ₹360 on an article costing ₹2400. Find the loss percentage.",
        "option_a": "10%",
        "option_b": "12%",
        "option_c": "15%",
        "option_d": "18%",
        "correct_option": "C",
        "explanation": "Loss% = 360/2400 × 100 = 15%.",
    },
    {
        "question_text": "A product is sold for ₹1320 at a profit of 10%. If it were sold for ₹1080, what would be the loss percentage?",
        "option_a": "5%",
        "option_b": "10%",
        "option_c": "12%",
        "option_d": "15%",
        "correct_option": "B",
        "explanation": "CP = 1320/1.1 = ₹1200. Loss at ₹1080 = ₹120, which is 10%.",
    },
    {
        "question_text": "An item is sold for ₹800 at a loss of 20%. If sold for ₹1200 instead, what would be the profit percentage?",
        "option_a": "10%",
        "option_b": "15%",
        "option_c": "20%",
        "option_d": "25%",
        "correct_option": "C",
        "explanation": "CP = 800/0.8 = ₹1000. Profit at ₹1200 = ₹200 = 20%.",
    },
    {
        "question_text": "A shopkeeper buys an item for ₹1800. At what price should it be sold to gain 25%?",
        "option_a": "₹2150",
        "option_b": "₹2200",
        "option_c": "₹2250",
        "option_d": "₹2300",
        "correct_option": "C",
        "explanation": "SP = 1800 × 1.25 = ₹2250.",
    },
]

profit_l2_created = 0
profit_l2_skipped = 0

for data in profit_level2_questions:
    exists = Question.objects.filter(
        subject=profit_subject,
        topic=profit_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        profit_l2_skipped += 1
        continue

    Question.objects.create(
        subject=profit_subject,
        topic=profit_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=2,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    profit_l2_created += 1

print(f"\nProfit & Loss Level 2 Created: {profit_l2_created}")
print(f"Profit & Loss Level 2 Skipped: {profit_l2_skipped}")
print("QA -> Profit & Loss -> Level 2 seeding complete.")

# =========================================================
# LR -> Blood Relations -> Level 1
# =========================================================

lr_subject = Subject.objects.get(name="LR")
blood_topic = Topic.objects.get(
    subject=lr_subject,
    name="Blood Relations"
)

blood_level1_questions = [
    {
        "question_text": "A is the father of B. B is the sister of C. How is A related to C?",
        "option_a": "Brother",
        "option_b": "Father",
        "option_c": "Uncle",
        "option_d": "Grandfather",
        "correct_option": "B",
        "explanation": "B and C are siblings, so A is also the father of C.",
    },
    {
        "question_text": "P is the mother of Q. Q is the brother of R. How is P related to R?",
        "option_a": "Mother",
        "option_b": "Sister",
        "option_c": "Aunt",
        "option_d": "Grandmother",
        "correct_option": "A",
        "explanation": "Q and R are siblings, so P is the mother of R.",
    },
    {
        "question_text": "A is the brother of B. B is the daughter of C. How is A related to C?",
        "option_a": "Son",
        "option_b": "Brother",
        "option_c": "Father",
        "option_d": "Uncle",
        "correct_option": "A",
        "explanation": "B is C's daughter and A is B's brother, so A is C's son.",
    },
    {
        "question_text": "R is the father of S. S is the father of T. How is R related to T?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "R is the father of T's father, so R is T's grandfather.",
    },
    {
        "question_text": "M is the sister of N. N is the father of O. How is M related to O?",
        "option_a": "Mother",
        "option_b": "Sister",
        "option_c": "Aunt",
        "option_d": "Grandmother",
        "correct_option": "C",
        "explanation": "M is the sister of O's father, so M is O's aunt.",
    },
    {
        "question_text": "A is the son of B. B is the daughter of C. How is C related to A?",
        "option_a": "Parent",
        "option_b": "Grandparent",
        "option_c": "Sibling",
        "option_d": "Uncle",
        "correct_option": "B",
        "explanation": "B is A's parent and C is B's parent, so C is A's grandparent.",
    },
    {
        "question_text": "K is the brother of L. L is the mother of M. How is K related to M?",
        "option_a": "Father",
        "option_b": "Brother",
        "option_c": "Uncle",
        "option_d": "Grandfather",
        "correct_option": "C",
        "explanation": "K is the brother of M's mother, so K is M's uncle.",
    },
    {
        "question_text": "X is the daughter of Y. Y is the son of Z. How is X related to Z?",
        "option_a": "Daughter",
        "option_b": "Granddaughter",
        "option_c": "Sister",
        "option_d": "Niece",
        "correct_option": "B",
        "explanation": "Y is Z's son and X is Y's daughter, so X is Z's granddaughter.",
    },
    {
        "question_text": "P is the father of Q. R is the mother of Q. How is P related to R?",
        "option_a": "Brother",
        "option_b": "Husband",
        "option_c": "Father",
        "option_d": "Son",
        "correct_option": "B",
        "explanation": "P and R are the father and mother of the same child, so P is R's husband.",
    },
    {
        "question_text": "A is the mother of B. C is the father of A. How is C related to B?",
        "option_a": "Father",
        "option_b": "Uncle",
        "option_c": "Grandfather",
        "option_d": "Brother",
        "correct_option": "C",
        "explanation": "C is the father of B's mother, so C is B's grandfather.",
    },
    {
        "question_text": "S is the sister of T. T is the son of U. How is S related to U?",
        "option_a": "Daughter",
        "option_b": "Sister",
        "option_c": "Mother",
        "option_d": "Aunt",
        "correct_option": "A",
        "explanation": "T is U's son and S is T's sister, so S is U's daughter.",
    },
    {
        "question_text": "B is the brother of C. C is the sister of D. How is B related to D?",
        "option_a": "Brother",
        "option_b": "Father",
        "option_c": "Uncle",
        "option_d": "Son",
        "correct_option": "A",
        "explanation": "B, C and D are siblings, so B is D's brother.",
    },
    {
        "question_text": "R is the daughter of S. S is the mother of T. How is R related to T?",
        "option_a": "Mother",
        "option_b": "Sister",
        "option_c": "Aunt",
        "option_d": "Daughter",
        "correct_option": "B",
        "explanation": "R and T have the same mother, so R is T's sister.",
    },
    {
        "question_text": "P is the son of Q. Q is the sister of R. How is P related to R?",
        "option_a": "Son",
        "option_b": "Nephew",
        "option_c": "Brother",
        "option_d": "Father",
        "correct_option": "B",
        "explanation": "Q is R's sister and P is Q's son, so P is R's nephew.",
    },
    {
        "question_text": "A is the father of B. B is the father of C. C is the son of D. How is A related to C?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "A is the father of C's father, so A is C's grandfather.",
    },
    {
        "question_text": "M is the mother of N. N is the mother of O. How is M related to O?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "M is the mother of O's mother, so M is O's grandmother.",
    },
    {
        "question_text": "K is the son of L. L is the brother of M. How is K related to M?",
        "option_a": "Nephew",
        "option_b": "Brother",
        "option_c": "Uncle",
        "option_d": "Son",
        "correct_option": "A",
        "explanation": "L is M's brother and K is L's son, so K is M's nephew.",
    },
    {
        "question_text": "C is the daughter of D. D is the sister of E. How is C related to E?",
        "option_a": "Sister",
        "option_b": "Daughter",
        "option_c": "Niece",
        "option_d": "Mother",
        "correct_option": "C",
        "explanation": "D is E's sister and C is D's daughter, so C is E's niece.",
    },
    {
        "question_text": "A is the brother of B. B is the mother of C. How is A related to C?",
        "option_a": "Brother",
        "option_b": "Father",
        "option_c": "Uncle",
        "option_d": "Grandfather",
        "correct_option": "C",
        "explanation": "A is the brother of C's mother, so A is C's uncle.",
    },
    {
        "question_text": "T is the father of U. U is the sister of V. How is T related to V?",
        "option_a": "Father",
        "option_b": "Uncle",
        "option_c": "Brother",
        "option_d": "Grandfather",
        "correct_option": "A",
        "explanation": "U and V are siblings, so T is also the father of V.",
    },
    {
        "question_text": "R is the mother of S. S is the brother of T. How is R related to T?",
        "option_a": "Mother",
        "option_b": "Aunt",
        "option_c": "Grandmother",
        "option_d": "Sister",
        "correct_option": "A",
        "explanation": "S and T are siblings, so R is also the mother of T.",
    },
    {
        "question_text": "X is the son of Y. Y is the sister of Z. How is X related to Z?",
        "option_a": "Brother",
        "option_b": "Nephew",
        "option_c": "Son",
        "option_d": "Uncle",
        "correct_option": "B",
        "explanation": "Y is Z's sister and X is Y's son, so X is Z's nephew.",
    },
    {
        "question_text": "A is the daughter of B. B is the son of C. How is A related to C?",
        "option_a": "Granddaughter",
        "option_b": "Daughter",
        "option_c": "Sister",
        "option_d": "Niece",
        "correct_option": "A",
        "explanation": "B is C's son and A is B's daughter, so A is C's granddaughter.",
    },
    {
        "question_text": "P is the sister of Q. Q is the father of R. How is P related to R?",
        "option_a": "Mother",
        "option_b": "Aunt",
        "option_c": "Sister",
        "option_d": "Grandmother",
        "correct_option": "B",
        "explanation": "P is the sister of R's father, so P is R's aunt.",
    },
    {
        "question_text": "M is the father of N. N is the daughter of O. How is M related to O?",
        "option_a": "Brother",
        "option_b": "Husband",
        "option_c": "Father",
        "option_d": "Son",
        "correct_option": "B",
        "explanation": "M and O are the parents of N, so M is O's husband.",
    },
]

blood_l1_created = 0
blood_l1_skipped = 0

for data in blood_level1_questions:
    exists = Question.objects.filter(
        subject=lr_subject,
        topic=blood_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        blood_l1_skipped += 1
        continue

    Question.objects.create(
        subject=lr_subject,
        topic=blood_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=1,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    blood_l1_created += 1

print(f"\nBlood Relations Level 1 Created: {blood_l1_created}")
print(f"Blood Relations Level 1 Skipped: {blood_l1_skipped}")
print("LR -> Blood Relations -> Level 1 seeding complete.")

# =========================================================
# LR -> Blood Relations -> Level 2
# =========================================================

blood_level2_questions = [
    {
        "question_text": "A is the brother of B. B is the mother of C. C is the sister of D. How is A related to D?",
        "option_a": "Father",
        "option_b": "Uncle",
        "option_c": "Brother",
        "option_d": "Grandfather",
        "correct_option": "B",
        "explanation": "A is the brother of D's mother, so A is D's uncle.",
    },
    {
        "question_text": "P is the father of Q. Q is the sister of R. R is the father of S. How is P related to S?",
        "option_a": "Father",
        "option_b": "Uncle",
        "option_c": "Grandfather",
        "option_d": "Brother",
        "correct_option": "C",
        "explanation": "P is the father of R, and R is the father of S. Therefore P is S's grandfather.",
    },
    {
        "question_text": "M is the daughter of N. N is the brother of O. O is the mother of P. How is M related to P?",
        "option_a": "Sister",
        "option_b": "Cousin",
        "option_c": "Aunt",
        "option_d": "Niece",
        "correct_option": "B",
        "explanation": "N and O are siblings, so their children M and P are cousins.",
    },
    {
        "question_text": "A is the son of B. C is the father of B. D is the mother of C. How is D related to A?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Great-grandmother",
        "option_d": "Aunt",
        "correct_option": "C",
        "explanation": "D is C's mother, C is B's father, and B is A's parent. Therefore D is A's great-grandmother.",
    },
    {
        "question_text": "R is the sister of S. S is the son of T. T is the daughter of U. How is R related to U?",
        "option_a": "Daughter",
        "option_b": "Granddaughter",
        "option_c": "Niece",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "R is T's daughter and T is U's daughter, so R is U's granddaughter.",
    },
    {
        "question_text": "K is the father of L. L is the brother of M. M is the mother of N. How is K related to N?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "K is the father of M, and M is the mother of N. So K is N's grandfather.",
    },
    {
        "question_text": "P is the daughter of Q. Q is the sister of R. R is the father of S. How is P related to S?",
        "option_a": "Sister",
        "option_b": "Cousin",
        "option_c": "Aunt",
        "option_d": "Niece",
        "correct_option": "B",
        "explanation": "Q and R are siblings, so their children P and S are cousins.",
    },
    {
        "question_text": "A is the mother of B. B is the father of C. C is the brother of D. How is A related to D?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "A is the mother of D's father, so A is D's grandmother.",
    },
    {
        "question_text": "X is the son of Y. Y is the daughter of Z. Z is the brother of W. How is X related to W?",
        "option_a": "Son",
        "option_b": "Nephew",
        "option_c": "Grandson",
        "option_d": "Grandnephew",
        "correct_option": "D",
        "explanation": "Y is W's niece, so Y's son X is W's grandnephew.",
    },
    {
        "question_text": "A is the brother of B. B is the sister of C. C is the father of D. How is A related to D?",
        "option_a": "Father",
        "option_b": "Uncle",
        "option_c": "Brother",
        "option_d": "Grandfather",
        "correct_option": "B",
        "explanation": "A is the brother of D's father, so A is D's uncle.",
    },
    {
        "question_text": "M is the mother of N. N is the sister of O. O is the father of P. How is M related to P?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "M is the mother of P's father, so M is P's grandmother.",
    },
    {
        "question_text": "R is the son of S. S is the sister of T. T is the father of U. How is R related to U?",
        "option_a": "Brother",
        "option_b": "Cousin",
        "option_c": "Uncle",
        "option_d": "Nephew",
        "correct_option": "B",
        "explanation": "S and T are siblings, so their children R and U are cousins.",
    },
    {
        "question_text": "P is the father of Q. Q is the mother of R. R is the sister of S. How is P related to S?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "P is the father of S's mother, so P is S's grandfather.",
    },
    {
        "question_text": "A is the daughter of B. B is the brother of C. C is the mother of D. How is A related to D?",
        "option_a": "Sister",
        "option_b": "Cousin",
        "option_c": "Aunt",
        "option_d": "Niece",
        "correct_option": "B",
        "explanation": "B and C are siblings, so their children A and D are cousins.",
    },
    {
        "question_text": "K is the brother of L. L is the daughter of M. M is the son of N. How is K related to N?",
        "option_a": "Son",
        "option_b": "Grandson",
        "option_c": "Nephew",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "K is M's son and M is N's son. Therefore K is N's grandson.",
    },
    {
        "question_text": "T is the mother of U. U is the father of V. V is the daughter of W. How is T related to V?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "T is the mother of V's father, so T is V's grandmother.",
    },
    {
        "question_text": "A is the father of B. B is the daughter of C. C is the sister of D. How is A related to C?",
        "option_a": "Brother",
        "option_b": "Husband",
        "option_c": "Father",
        "option_d": "Son",
        "correct_option": "B",
        "explanation": "A and C are the parents of B, so A is C's husband.",
    },
    {
        "question_text": "P is the son of Q. Q is the brother of R. R is the mother of S. How is P related to S?",
        "option_a": "Brother",
        "option_b": "Cousin",
        "option_c": "Uncle",
        "option_d": "Nephew",
        "correct_option": "B",
        "explanation": "Q and R are siblings, so P and S are cousins.",
    },
    {
        "question_text": "M is the sister of N. N is the father of O. O is the father of P. How is M related to P?",
        "option_a": "Mother",
        "option_b": "Aunt",
        "option_c": "Great-aunt",
        "option_d": "Grandmother",
        "correct_option": "C",
        "explanation": "M is the sister of P's grandfather N, so M is P's great-aunt.",
    },
    {
        "question_text": "X is the daughter of Y. Y is the brother of Z. Z is the father of A. How is X related to A?",
        "option_a": "Sister",
        "option_b": "Cousin",
        "option_c": "Niece",
        "option_d": "Aunt",
        "correct_option": "B",
        "explanation": "Y and Z are brothers, so their children X and A are cousins.",
    },
    {
        "question_text": "R is the mother of S. S is the brother of T. T is the mother of U. How is R related to U?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "R is the mother of U's mother T, so R is U's grandmother.",
    },
    {
        "question_text": "A is the son of B. B is the sister of C. C is the mother of D. How is A related to D?",
        "option_a": "Brother",
        "option_b": "Cousin",
        "option_c": "Nephew",
        "option_d": "Uncle",
        "correct_option": "B",
        "explanation": "B and C are sisters, so their children A and D are cousins.",
    },
    {
        "question_text": "K is the daughter of L. L is the brother of M. M is the father of N. How is K related to N?",
        "option_a": "Sister",
        "option_b": "Cousin",
        "option_c": "Aunt",
        "option_d": "Niece",
        "correct_option": "B",
        "explanation": "L and M are brothers, so K and N are cousins.",
    },
    {
        "question_text": "P is the father of Q. Q is the brother of R. R is the mother of S. How is P related to S?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "P is the father of S's mother R, so P is S's grandfather.",
    },
    {
        "question_text": "M is the daughter of N. N is the son of O. O is the mother of P. How is M related to P?",
        "option_a": "Daughter",
        "option_b": "Niece",
        "option_c": "Sister",
        "option_d": "Aunt",
        "correct_option": "B",
        "explanation": "N and P are siblings, and M is N's daughter. Therefore M is P's niece.",
    },
]

blood_l2_created = 0
blood_l2_skipped = 0

for data in blood_level2_questions:
    exists = Question.objects.filter(
        subject=lr_subject,
        topic=blood_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        blood_l2_skipped += 1
        continue

    Question.objects.create(
        subject=lr_subject,
        topic=blood_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=2,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    blood_l2_created += 1

print(f"\nBlood Relations Level 2 Created: {blood_l2_created}")
print(f"Blood Relations Level 2 Skipped: {blood_l2_skipped}")
print("LR -> Blood Relations -> Level 2 seeding complete.")

# =========================================================
# LR -> Blood Relations -> Level 3
# =========================================================

blood_level3_questions = [
    {
        "question_text": "Pointing to a woman, Raj said, 'She is the daughter of the only son of my grandfather.' How is the woman related to Raj?",
        "option_a": "Mother",
        "option_b": "Sister",
        "option_c": "Aunt",
        "option_d": "Cousin",
        "correct_option": "B",
        "explanation": "The only son of Raj's grandfather is Raj's father. His daughter is Raj's sister.",
    },
    {
        "question_text": "A woman says, 'The man in the photograph is the son of my mother's only son.' How is the man related to the woman?",
        "option_a": "Brother",
        "option_b": "Son",
        "option_c": "Nephew",
        "option_d": "Cousin",
        "correct_option": "C",
        "explanation": "The woman's mother's only son is her brother. His son is her nephew.",
    },
    {
        "question_text": "P is Q's brother. R is Q's mother. S is R's father. How is S related to P?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "R is P's mother and S is R's father. Therefore S is P's grandfather.",
    },
    {
        "question_text": "A is the sister of B. B is the father of C. C is the brother of D. How is A related to D?",
        "option_a": "Mother",
        "option_b": "Aunt",
        "option_c": "Sister",
        "option_d": "Grandmother",
        "correct_option": "B",
        "explanation": "A is the sister of D's father B, so A is D's aunt.",
    },
    {
        "question_text": "Pointing to a boy, Meena said, 'He is the son of the only daughter of my mother.' How is the boy related to Meena?",
        "option_a": "Brother",
        "option_b": "Nephew",
        "option_c": "Son",
        "option_d": "Cousin",
        "correct_option": "C",
        "explanation": "The only daughter of Meena's mother is Meena herself. Therefore the boy is Meena's son.",
    },
    {
        "question_text": "If A is B's father, C is A's mother, D is C's husband and E is D's son, how is E related to B?",
        "option_a": "Father",
        "option_b": "Uncle",
        "option_c": "Brother",
        "option_d": "Grandfather",
        "correct_option": "B",
        "explanation": "D and C are A's parents. E is D's son, so E is A's brother and therefore B's uncle.",
    },
    {
        "question_text": "Ravi said, 'She is the wife of the only son of my grandmother.' How is the woman related to Ravi?",
        "option_a": "Mother",
        "option_b": "Sister",
        "option_c": "Aunt",
        "option_d": "Grandmother",
        "correct_option": "A",
        "explanation": "The only son of Ravi's grandmother is Ravi's father. His wife is Ravi's mother.",
    },
    {
        "question_text": "A is the mother of B. C is the brother of A. D is the father of C. How is D related to B?",
        "option_a": "Father",
        "option_b": "Uncle",
        "option_c": "Grandfather",
        "option_d": "Brother",
        "correct_option": "C",
        "explanation": "D is the father of A, who is B's mother. Therefore D is B's grandfather.",
    },
    {
        "question_text": "P is the daughter of Q. R is the husband of Q. S is the mother of R. How is S related to P?",
        "option_a": "Mother",
        "option_b": "Aunt",
        "option_c": "Grandmother",
        "option_d": "Sister",
        "correct_option": "C",
        "explanation": "R is P's father and S is R's mother. So S is P's grandmother.",
    },
    {
        "question_text": "Pointing to a man, Neha said, 'His mother is the only daughter of my mother.' How is the man related to Neha?",
        "option_a": "Brother",
        "option_b": "Son",
        "option_c": "Nephew",
        "option_d": "Cousin",
        "correct_option": "B",
        "explanation": "The only daughter of Neha's mother is Neha herself, so the man is Neha's son.",
    },
    {
        "question_text": "A is B's sister. C is B's mother. D is C's father. E is D's wife. How is E related to A?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "D is A's maternal grandfather and E is D's wife, so E is A's grandmother.",
    },
    {
        "question_text": "If M is N's mother, N is O's sister, O is P's father and P is Q's brother, how is M related to Q?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "M is O's mother. O is Q's father, so M is Q's grandmother.",
    },
    {
        "question_text": "Pointing to a girl, Amit said, 'She is the daughter of the only daughter of my father.' How is the girl related to Amit?",
        "option_a": "Daughter",
        "option_b": "Sister",
        "option_c": "Niece",
        "option_d": "Cousin",
        "correct_option": "C",
        "explanation": "The only daughter of Amit's father is Amit's sister. Her daughter is Amit's niece.",
    },
    {
        "question_text": "A is the son of B. B is the sister of C. C is the father of D. D is the sister of E. How is A related to E?",
        "option_a": "Brother",
        "option_b": "Cousin",
        "option_c": "Uncle",
        "option_d": "Nephew",
        "correct_option": "B",
        "explanation": "B and C are siblings, so their children A and E are cousins.",
    },
    {
        "question_text": "P is the brother of Q. Q is the daughter of R. R is the wife of S. T is the father of S. How is T related to P?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "S is P's father and T is S's father. Therefore T is P's grandfather.",
    },
    {
        "question_text": "A woman introduced a man as 'the brother of the daughter of the wife of my husband.' How is the man related to the woman?",
        "option_a": "Brother",
        "option_b": "Son",
        "option_c": "Nephew",
        "option_d": "Husband",
        "correct_option": "B",
        "explanation": "The wife of her husband is the woman herself. Her daughter's brother is her son.",
    },
    {
        "question_text": "X is the father of Y. Z is the sister of X. A is the daughter of Z. How is A related to Y?",
        "option_a": "Sister",
        "option_b": "Cousin",
        "option_c": "Aunt",
        "option_d": "Niece",
        "correct_option": "B",
        "explanation": "X and Z are siblings, so their children Y and A are cousins.",
    },
    {
        "question_text": "P is the mother of Q. R is the brother of P. S is the son of R. How is S related to Q?",
        "option_a": "Brother",
        "option_b": "Cousin",
        "option_c": "Uncle",
        "option_d": "Nephew",
        "correct_option": "B",
        "explanation": "P and R are siblings, so their children Q and S are cousins.",
    },
    {
        "question_text": "A is the father of B. C is the daughter of B. D is the brother of C. How is A related to D?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "B is D's parent and A is B's father. Hence A is D's grandfather.",
    },
    {
        "question_text": "Pointing to a lady, Arun said, 'She is the mother of my father's only daughter.' How is the lady related to Arun?",
        "option_a": "Mother",
        "option_b": "Sister",
        "option_c": "Aunt",
        "option_d": "Grandmother",
        "correct_option": "A",
        "explanation": "Arun's father's only daughter is Arun's sister. Her mother is Arun's mother.",
    },
    {
        "question_text": "M is the brother of N. N is the daughter of O. P is the mother of O. How is P related to M?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Aunt",
        "option_d": "Sister",
        "correct_option": "B",
        "explanation": "O is M's parent and P is O's mother, so P is M's grandmother.",
    },
    {
        "question_text": "If A is B's mother, B is C's father, C is D's sister and D is E's father, how is A related to E?",
        "option_a": "Mother",
        "option_b": "Grandmother",
        "option_c": "Great-grandmother",
        "option_d": "Aunt",
        "correct_option": "C",
        "explanation": "A is the mother of B, B is the father of D, and D is E's father. So A is E's great-grandmother.",
    },
    {
        "question_text": "P is Q's son. Q is R's daughter. R is S's wife. How is S related to P?",
        "option_a": "Father",
        "option_b": "Grandfather",
        "option_c": "Uncle",
        "option_d": "Brother",
        "correct_option": "B",
        "explanation": "S is Q's father and Q is P's mother, so S is P's grandfather.",
    },
    {
        "question_text": "Pointing to a boy, Sita said, 'He is the son of the only brother of my father.' How is the boy related to Sita?",
        "option_a": "Brother",
        "option_b": "Cousin",
        "option_c": "Nephew",
        "option_d": "Uncle",
        "correct_option": "B",
        "explanation": "The only brother of Sita's father is her uncle. His son is Sita's cousin.",
    },
    {
        "question_text": "A is the daughter of B. B is the brother of C. C is the father of D. D is the mother of E. How is A related to E?",
        "option_a": "Aunt",
        "option_b": "Cousin",
        "option_c": "Niece",
        "option_d": "Sister",
        "correct_option": "A",
        "explanation": "A and D are cousins because B and C are brothers. Therefore A is the cousin of E's mother, commonly treated as an aunt relation.",
    },
]

blood_l3_created = 0
blood_l3_skipped = 0

for data in blood_level3_questions:
    exists = Question.objects.filter(
        subject=lr_subject,
        topic=blood_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        blood_l3_skipped += 1
        continue

    Question.objects.create(
        subject=lr_subject,
        topic=blood_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=3,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    blood_l3_created += 1

print(f"\nBlood Relations Level 3 Created: {blood_l3_created}")
print(f"Blood Relations Level 3 Skipped: {blood_l3_skipped}")
print("LR -> Blood Relations -> Level 3 seeding complete.")

# =========================================================
# LR -> Number/Letter Series -> Level 1
# =========================================================

series_topic = Topic.objects.get(
    subject=lr_subject,
    name="Number/Letter Series"
)

series_level1_questions = [
    {
        "question_text": "Find the next number in the series: 2, 4, 6, 8, ?",
        "option_a": "9",
        "option_b": "10",
        "option_c": "11",
        "option_d": "12",
        "correct_option": "B",
        "explanation": "The numbers increase by 2 each time. Next = 10.",
    },
    {
        "question_text": "Find the next number: 5, 10, 15, 20, ?",
        "option_a": "22",
        "option_b": "24",
        "option_c": "25",
        "option_d": "30",
        "correct_option": "C",
        "explanation": "Each term increases by 5. Next = 25.",
    },
    {
        "question_text": "Find the next number: 1, 3, 5, 7, ?",
        "option_a": "8",
        "option_b": "9",
        "option_c": "10",
        "option_d": "11",
        "correct_option": "B",
        "explanation": "The series contains consecutive odd numbers. Next = 9.",
    },
    {
        "question_text": "Find the next number: 10, 20, 30, 40, ?",
        "option_a": "45",
        "option_b": "50",
        "option_c": "55",
        "option_d": "60",
        "correct_option": "B",
        "explanation": "Each term increases by 10. Next = 50.",
    },
    {
        "question_text": "Find the next number: 3, 6, 9, 12, ?",
        "option_a": "14",
        "option_b": "15",
        "option_c": "16",
        "option_d": "18",
        "correct_option": "B",
        "explanation": "Each term increases by 3. Next = 15.",
    },
    {
        "question_text": "Find the next number: 2, 4, 8, 16, ?",
        "option_a": "24",
        "option_b": "28",
        "option_c": "32",
        "option_d": "36",
        "correct_option": "C",
        "explanation": "Each number is multiplied by 2. Next = 32.",
    },
    {
        "question_text": "Find the next number: 1, 2, 4, 8, ?",
        "option_a": "12",
        "option_b": "14",
        "option_c": "16",
        "option_d": "18",
        "correct_option": "C",
        "explanation": "Each number is doubled. Next = 16.",
    },
    {
        "question_text": "Find the missing number: 7, 14, 21, ?, 35",
        "option_a": "24",
        "option_b": "26",
        "option_c": "28",
        "option_d": "30",
        "correct_option": "C",
        "explanation": "The series increases by 7. Missing number = 28.",
    },
    {
        "question_text": "Find the next number: 50, 45, 40, 35, ?",
        "option_a": "25",
        "option_b": "30",
        "option_c": "32",
        "option_d": "34",
        "correct_option": "B",
        "explanation": "Each term decreases by 5. Next = 30.",
    },
    {
        "question_text": "Find the next number: 100, 90, 80, 70, ?",
        "option_a": "50",
        "option_b": "55",
        "option_c": "60",
        "option_d": "65",
        "correct_option": "C",
        "explanation": "Each term decreases by 10. Next = 60.",
    },
    {
        "question_text": "Find the next letter: A, B, C, D, ?",
        "option_a": "E",
        "option_b": "F",
        "option_c": "G",
        "option_d": "H",
        "correct_option": "A",
        "explanation": "Letters are in alphabetical order. Next = E.",
    },
    {
        "question_text": "Find the next letter: B, D, F, H, ?",
        "option_a": "I",
        "option_b": "J",
        "option_c": "K",
        "option_d": "L",
        "correct_option": "B",
        "explanation": "Every second letter is used: B, D, F, H, J.",
    },
    {
        "question_text": "Find the next letter: A, C, E, G, ?",
        "option_a": "H",
        "option_b": "I",
        "option_c": "J",
        "option_d": "K",
        "correct_option": "B",
        "explanation": "Every second alphabet letter is used. Next = I.",
    },
    {
        "question_text": "Find the next letter: Z, Y, X, W, ?",
        "option_a": "T",
        "option_b": "U",
        "option_c": "V",
        "option_d": "S",
        "correct_option": "C",
        "explanation": "Letters move backward one position each time. Next = V.",
    },
    {
        "question_text": "Find the missing letter: A, C, ?, G, I",
        "option_a": "D",
        "option_b": "E",
        "option_c": "F",
        "option_d": "H",
        "correct_option": "B",
        "explanation": "Series uses alternate letters: A, C, E, G, I.",
    },
    {
        "question_text": "Find the next number: 4, 8, 12, 16, ?",
        "option_a": "18",
        "option_b": "20",
        "option_c": "22",
        "option_d": "24",
        "correct_option": "B",
        "explanation": "Each term increases by 4. Next = 20.",
    },
    {
        "question_text": "Find the next number: 9, 18, 27, 36, ?",
        "option_a": "42",
        "option_b": "45",
        "option_c": "48",
        "option_d": "54",
        "correct_option": "B",
        "explanation": "Each term increases by 9. Next = 45.",
    },
    {
        "question_text": "Find the next number: 25, 20, 15, 10, ?",
        "option_a": "0",
        "option_b": "5",
        "option_c": "8",
        "option_d": "10",
        "correct_option": "B",
        "explanation": "Each term decreases by 5. Next = 5.",
    },
    {
        "question_text": "Find the next number: 1, 4, 7, 10, ?",
        "option_a": "11",
        "option_b": "12",
        "option_c": "13",
        "option_d": "14",
        "correct_option": "C",
        "explanation": "Each term increases by 3. Next = 13.",
    },
    {
        "question_text": "Find the next number: 6, 12, 18, 24, ?",
        "option_a": "28",
        "option_b": "30",
        "option_c": "32",
        "option_d": "36",
        "correct_option": "B",
        "explanation": "Each term increases by 6. Next = 30.",
    },
    {
        "question_text": "Find the next letter: C, E, G, I, ?",
        "option_a": "J",
        "option_b": "K",
        "option_c": "L",
        "option_d": "M",
        "correct_option": "B",
        "explanation": "Every second letter is used. Next = K.",
    },
    {
        "question_text": "Find the next letter: M, N, O, P, ?",
        "option_a": "Q",
        "option_b": "R",
        "option_c": "S",
        "option_d": "T",
        "correct_option": "A",
        "explanation": "Letters are consecutive. Next = Q.",
    },
    {
        "question_text": "Find the next number: 30, 25, 20, 15, ?",
        "option_a": "5",
        "option_b": "10",
        "option_c": "12",
        "option_d": "14",
        "correct_option": "B",
        "explanation": "Each term decreases by 5. Next = 10.",
    },
    {
        "question_text": "Find the missing number: 2, 6, 10, ?, 18",
        "option_a": "12",
        "option_b": "13",
        "option_c": "14",
        "option_d": "16",
        "correct_option": "C",
        "explanation": "Each term increases by 4. Missing number = 14.",
    },
    {
        "question_text": "Find the next letter: D, F, H, J, ?",
        "option_a": "K",
        "option_b": "L",
        "option_c": "M",
        "option_d": "N",
        "correct_option": "B",
        "explanation": "Every second letter is used. Next = L.",
    },
]

series_l1_created = 0
series_l1_skipped = 0

for data in series_level1_questions:
    exists = Question.objects.filter(
        subject=lr_subject,
        topic=series_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        series_l1_skipped += 1
        continue

    Question.objects.create(
        subject=lr_subject,
        topic=series_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=1,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    series_l1_created += 1

print(f"\nSeries Level 1 Created: {series_l1_created}")
print(f"Series Level 1 Skipped: {series_l1_skipped}")
print("LR -> Number/Letter Series -> Level 1 seeding complete.")

# =========================================================
# LR -> Number/Letter Series -> Level 2
# =========================================================

series_level2_questions = [
    {
        "question_text": "Find the next number: 3, 6, 12, 24, ?",
        "option_a": "36",
        "option_b": "42",
        "option_c": "48",
        "option_d": "52",
        "correct_option": "C",
        "explanation": "Each term is multiplied by 2. Next = 48.",
    },
    {
        "question_text": "Find the next number: 2, 5, 10, 17, 26, ?",
        "option_a": "35",
        "option_b": "37",
        "option_c": "39",
        "option_d": "41",
        "correct_option": "B",
        "explanation": "Differences are +3, +5, +7, +9. Next difference is +11. So next = 37.",
    },
    {
        "question_text": "Find the next number: 1, 4, 9, 16, ?",
        "option_a": "20",
        "option_b": "24",
        "option_c": "25",
        "option_d": "27",
        "correct_option": "C",
        "explanation": "These are squares: 1², 2², 3², 4². Next = 5² = 25.",
    },
    {
        "question_text": "Find the next number: 2, 6, 12, 20, 30, ?",
        "option_a": "36",
        "option_b": "40",
        "option_c": "42",
        "option_d": "44",
        "correct_option": "C",
        "explanation": "Pattern is n(n+1): 1×2, 2×3, 3×4, 4×5, 5×6. Next = 6×7 = 42.",
    },
    {
        "question_text": "Find the next number: 81, 27, 9, 3, ?",
        "option_a": "1",
        "option_b": "2",
        "option_c": "0",
        "option_d": "3",
        "correct_option": "A",
        "explanation": "Each term is divided by 3. Next = 1.",
    },
    {
        "question_text": "Find the next number: 5, 11, 23, 47, ?",
        "option_a": "91",
        "option_b": "93",
        "option_c": "95",
        "option_d": "97",
        "correct_option": "C",
        "explanation": "Each term = previous × 2 + 1. Next = 47 × 2 + 1 = 95.",
    },
    {
        "question_text": "Find the next number: 100, 95, 85, 70, ?",
        "option_a": "45",
        "option_b": "50",
        "option_c": "55",
        "option_d": "60",
        "correct_option": "B",
        "explanation": "Subtract 5, 10, 15, then 20. Next = 70 - 20 = 50.",
    },
    {
        "question_text": "Find the missing number: 4, 9, 16, 25, ?, 49",
        "option_a": "30",
        "option_b": "32",
        "option_c": "36",
        "option_d": "40",
        "correct_option": "C",
        "explanation": "These are squares 2², 3², 4², 5², 6², 7². Missing = 36.",
    },
    {
        "question_text": "Find the next number: 7, 14, 28, 56, ?",
        "option_a": "84",
        "option_b": "98",
        "option_c": "112",
        "option_d": "120",
        "correct_option": "C",
        "explanation": "Each term is doubled. Next = 112.",
    },
    {
        "question_text": "Find the next number: 2, 3, 5, 8, 12, ?",
        "option_a": "15",
        "option_b": "16",
        "option_c": "17",
        "option_d": "18",
        "correct_option": "C",
        "explanation": "Differences are +1, +2, +3, +4. Next difference = +5. Next = 17.",
    },
    {
        "question_text": "Find the next letter: A, D, G, J, ?",
        "option_a": "K",
        "option_b": "L",
        "option_c": "M",
        "option_d": "N",
        "correct_option": "C",
        "explanation": "Each letter moves forward by 3 positions. Next = M.",
    },
    {
        "question_text": "Find the next letter: Z, W, T, Q, ?",
        "option_a": "M",
        "option_b": "N",
        "option_c": "O",
        "option_d": "P",
        "correct_option": "B",
        "explanation": "Each letter moves backward by 3 positions. Next = N.",
    },
    {
        "question_text": "Find the next letter: B, E, H, K, ?",
        "option_a": "L",
        "option_b": "M",
        "option_c": "N",
        "option_d": "O",
        "correct_option": "C",
        "explanation": "Each term advances by 3 letters. Next = N.",
    },
    {
        "question_text": "Find the next pair: AB, CD, EF, GH, ?",
        "option_a": "HI",
        "option_b": "IJ",
        "option_c": "JK",
        "option_d": "KL",
        "correct_option": "B",
        "explanation": "Pairs are consecutive alphabet groups. Next = IJ.",
    },
    {
        "question_text": "Find the next letter: A, C, F, J, ?",
        "option_a": "M",
        "option_b": "N",
        "option_c": "O",
        "option_d": "P",
        "correct_option": "C",
        "explanation": "Letter jumps are +2, +3, +4, so next is +5. J + 5 = O.",
    },
    {
        "question_text": "Find the next number: 11, 22, 44, 88, ?",
        "option_a": "132",
        "option_b": "154",
        "option_c": "166",
        "option_d": "176",
        "correct_option": "D",
        "explanation": "Each term is doubled. Next = 176.",
    },
    {
        "question_text": "Find the next number: 64, 32, 16, 8, ?",
        "option_a": "2",
        "option_b": "4",
        "option_c": "6",
        "option_d": "8",
        "correct_option": "B",
        "explanation": "Each term is divided by 2. Next = 4.",
    },
    {
        "question_text": "Find the next number: 1, 8, 27, 64, ?",
        "option_a": "100",
        "option_b": "120",
        "option_c": "125",
        "option_d": "144",
        "correct_option": "C",
        "explanation": "These are cubes: 1³, 2³, 3³, 4³. Next = 5³ = 125.",
    },
    {
        "question_text": "Find the next number: 13, 18, 24, 31, 39, ?",
        "option_a": "46",
        "option_b": "47",
        "option_c": "48",
        "option_d": "49",
        "correct_option": "C",
        "explanation": "Differences are +5, +6, +7, +8. Next difference = +9. Next = 48.",
    },
    {
        "question_text": "Find the next number: 90, 81, 73, 66, ?",
        "option_a": "58",
        "option_b": "60",
        "option_c": "61",
        "option_d": "62",
        "correct_option": "B",
        "explanation": "Differences are -9, -8, -7. Next is -6. So 66 - 6 = 60.",
    },
    {
        "question_text": "Find the next letter: C, F, J, O, ?",
        "option_a": "T",
        "option_b": "U",
        "option_c": "V",
        "option_d": "W",
        "correct_option": "B",
        "explanation": "Jumps are +3, +4, +5, then +6. O + 6 = U.",
    },
    {
        "question_text": "Find the next number: 4, 7, 13, 25, ?",
        "option_a": "37",
        "option_b": "43",
        "option_c": "49",
        "option_d": "51",
        "correct_option": "C",
        "explanation": "Each term = previous × 2 - 1. Next = 25 × 2 - 1 = 49.",
    },
    {
        "question_text": "Find the missing number: 3, 9, 27, ?, 243",
        "option_a": "54",
        "option_b": "72",
        "option_c": "81",
        "option_d": "90",
        "correct_option": "C",
        "explanation": "Each term is multiplied by 3. Missing number = 81.",
    },
    {
        "question_text": "Find the next number: 6, 10, 18, 34, ?",
        "option_a": "50",
        "option_b": "58",
        "option_c": "64",
        "option_d": "66",
        "correct_option": "D",
        "explanation": "Differences are +4, +8, +16. Next difference = +32. Next = 66.",
    },
    {
        "question_text": "Find the next letter: A, Z, B, Y, C, X, ?",
        "option_a": "D",
        "option_b": "W",
        "option_c": "E",
        "option_d": "V",
        "correct_option": "A",
        "explanation": "Letters alternate from the start and end of the alphabet: A, Z, B, Y, C, X, D.",
    },
]

series_l2_created = 0
series_l2_skipped = 0

for data in series_level2_questions:
    exists = Question.objects.filter(
        subject=lr_subject,
        topic=series_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        series_l2_skipped += 1
        continue

    Question.objects.create(
        subject=lr_subject,
        topic=series_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=2,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    series_l2_created += 1

print(f"\nSeries Level 2 Created: {series_l2_created}")
print(f"Series Level 2 Skipped: {series_l2_skipped}")
print("LR -> Number/Letter Series -> Level 2 seeding complete.")

# =========================================================
# LR -> Coding-Decoding -> Level 1
# =========================================================

coding_topic = Topic.objects.get(
    subject=lr_subject,
    name="Coding-Decoding"
)

coding_level1_questions = [
    {
        "question_text": "If CAT is coded as DBU, how is DOG coded?",
        "option_a": "EPH",
        "option_b": "EOH",
        "option_c": "FQI",
        "option_d": "DNG",
        "correct_option": "A",
        "explanation": "Each letter is moved one position forward: D→E, O→P, G→H.",
    },
    {
        "question_text": "If BOOK is coded as CPPL, how is PEN coded?",
        "option_a": "QFO",
        "option_b": "QEN",
        "option_c": "RFO",
        "option_d": "PFM",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by one position: P→Q, E→F, N→O.",
    },
    {
        "question_text": "If BAT is coded as AZS, how is DOG coded?",
        "option_a": "CNF",
        "option_b": "EPH",
        "option_c": "CMF",
        "option_d": "DNG",
        "correct_option": "A",
        "explanation": "Each letter is shifted one position backward: D→C, O→N, G→F.",
    },
    {
        "question_text": "If SUN is coded as TVO, how is MOON coded?",
        "option_a": "NPPO",
        "option_b": "NPPM",
        "option_c": "MPPO",
        "option_d": "OQQP",
        "correct_option": "A",
        "explanation": "Each letter is moved one position forward: M→N, O→P, O→P, N→O.",
    },
    {
        "question_text": "If APPLE is coded as BQQMF, how is MANGO coded?",
        "option_a": "NBOHP",
        "option_b": "NBMHP",
        "option_c": "OCPHQ",
        "option_d": "MANHP",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by one position.",
    },
    {
        "question_text": "If A=1, B=2, C=3 and so on, what is the code value of CAT?",
        "option_a": "22",
        "option_b": "24",
        "option_c": "26",
        "option_d": "28",
        "correct_option": "B",
        "explanation": "C=3, A=1, T=20. Total = 3+1+20 = 24.",
    },
    {
        "question_text": "If A=1, B=2, C=3 and so on, what is the value of DOG?",
        "option_a": "24",
        "option_b": "25",
        "option_c": "26",
        "option_d": "27",
        "correct_option": "C",
        "explanation": "D=4, O=15, G=7. Total = 4+15+7 = 26.",
    },
    {
        "question_text": "If PEN is written as 16-5-14, how is CAT written?",
        "option_a": "3-1-20",
        "option_b": "2-1-20",
        "option_c": "3-2-20",
        "option_d": "3-1-19",
        "correct_option": "A",
        "explanation": "Alphabet positions are C=3, A=1 and T=20.",
    },
    {
        "question_text": "If BAD is written as 2-1-4, how is FACE written?",
        "option_a": "6-1-3-5",
        "option_b": "5-1-3-6",
        "option_c": "6-2-3-5",
        "option_d": "6-1-4-5",
        "correct_option": "A",
        "explanation": "Alphabet positions: F=6, A=1, C=3, E=5.",
    },
    {
        "question_text": "If ROAD is coded as URDG, how is CAR coded using the same rule?",
        "option_a": "FDU",
        "option_b": "ECU",
        "option_c": "FDT",
        "option_d": "GBV",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 3 positions: C→F, A→D, R→U.",
    },
    {
        "question_text": "If MILK is coded as NJML, how is RICE coded?",
        "option_a": "SJDF",
        "option_b": "SICF",
        "option_c": "TKDG",
        "option_d": "RHBD",
        "correct_option": "A",
        "explanation": "Each letter moves one position forward: R→S, I→J, C→D, E→F.",
    },
    {
        "question_text": "If HOME is coded as IPNF, how is ROOM coded?",
        "option_a": "SPPN",
        "option_b": "RPPN",
        "option_c": "SQQN",
        "option_d": "SPPO",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by one position.",
    },
    {
        "question_text": "If FISH is coded as EHRG, how is GOAT coded?",
        "option_a": "FNZS",
        "option_b": "HPBU",
        "option_c": "FMZS",
        "option_d": "GNAT",
        "correct_option": "A",
        "explanation": "Each letter moves one position backward: G→F, O→N, A→Z, T→S.",
    },
    {
        "question_text": "If KING is coded as JHMF, how is QUEEN coded?",
        "option_a": "PTDDM",
        "option_b": "RVFFO",
        "option_c": "PTEDM",
        "option_d": "QTDDM",
        "correct_option": "A",
        "explanation": "Each letter is shifted one position backward.",
    },
    {
        "question_text": "If 1 represents A, 2 represents B and so on, what word is represented by 3-1-20?",
        "option_a": "CAT",
        "option_b": "BAT",
        "option_c": "CAR",
        "option_d": "CAN",
        "correct_option": "A",
        "explanation": "3=C, 1=A and 20=T, so the word is CAT.",
    },
    {
        "question_text": "Which word is represented by 4-15-7 using alphabet positions?",
        "option_a": "DIG",
        "option_b": "DOG",
        "option_c": "DOT",
        "option_d": "LOG",
        "correct_option": "B",
        "explanation": "4=D, 15=O and 7=G, so the word is DOG.",
    },
    {
        "question_text": "If TABLE is coded as UBCMF, how is CHAIR coded?",
        "option_a": "DIBJS",
        "option_b": "DHAIR",
        "option_c": "EJCJT",
        "option_d": "DIBJR",
        "correct_option": "A",
        "explanation": "Each letter is moved forward by one position.",
    },
    {
        "question_text": "If BLUE is coded as CMVF, how is RED coded?",
        "option_a": "SFE",
        "option_b": "RFE",
        "option_c": "TGF",
        "option_d": "QDC",
        "correct_option": "A",
        "explanation": "Each letter is shifted one position forward: R→S, E→F, D→E.",
    },
    {
        "question_text": "If GREEN is coded as HSFFO, how is BLACK coded?",
        "option_a": "CMBDL",
        "option_b": "CLBDL",
        "option_c": "CMBCK",
        "option_d": "DNCDM",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by one position.",
    },
    {
        "question_text": "If STAR is coded as TUBS, how is MOON coded?",
        "option_a": "NPPO",
        "option_b": "NQPO",
        "option_c": "MPPO",
        "option_d": "OQQP",
        "correct_option": "A",
        "explanation": "Every letter moves one position forward.",
    },
    {
        "question_text": "If COLD is coded as DPME, how is HEAT coded?",
        "option_a": "IFBU",
        "option_b": "HFBU",
        "option_c": "IGCV",
        "option_d": "IEAT",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by one position.",
    },
    {
        "question_text": "If LION is coded as KHNM, how is BEAR coded?",
        "option_a": "ADZQ",
        "option_b": "CFBS",
        "option_c": "AEZQ",
        "option_d": "BDAR",
        "correct_option": "A",
        "explanation": "Each letter is shifted one position backward: B→A, E→D, A→Z, R→Q.",
    },
    {
        "question_text": "If MAN is coded as 13-1-14, how is SUN coded?",
        "option_a": "19-21-14",
        "option_b": "18-21-14",
        "option_c": "19-20-14",
        "option_d": "19-21-13",
        "correct_option": "A",
        "explanation": "Alphabet positions: S=19, U=21 and N=14.",
    },
    {
        "question_text": "If CODE is written as 3-15-4-5, how is LOGIC written?",
        "option_a": "12-15-7-9-3",
        "option_b": "11-15-7-9-3",
        "option_c": "12-14-7-9-3",
        "option_d": "12-15-8-9-3",
        "correct_option": "A",
        "explanation": "Alphabet positions: L=12, O=15, G=7, I=9, C=3.",
    },
    {
        "question_text": "If ZOO is coded as APP, how is YAK coded?",
        "option_a": "ZBL",
        "option_b": "XAJ",
        "option_c": "ZBK",
        "option_d": "ABL",
        "correct_option": "A",
        "explanation": "Each letter moves one position forward, with Z wrapping to A.",
    },
]

coding_l1_created = 0
coding_l1_skipped = 0

for data in coding_level1_questions:
    exists = Question.objects.filter(
        subject=lr_subject,
        topic=coding_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        coding_l1_skipped += 1
        continue

    Question.objects.create(
        subject=lr_subject,
        topic=coding_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=1,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    coding_l1_created += 1

print(f"\nCoding-Decoding Level 1 Created: {coding_l1_created}")
print(f"Coding-Decoding Level 1 Skipped: {coding_l1_skipped}")
print("LR -> Coding-Decoding -> Level 1 seeding complete.")

# =========================================================
# LR -> Coding-Decoding -> Level 2
# =========================================================

coding_level2_questions = [
    {
        "question_text": "If CAT is coded as ECV, how is DOG coded?",
        "option_a": "FQI",
        "option_b": "EPH",
        "option_c": "GRJ",
        "option_d": "FQH",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 2 positions: D→F, O→Q, G→I.",
    },
    {
        "question_text": "If MANGO is coded as OCPIQ, how is APPLE coded?",
        "option_a": "CRRNG",
        "option_b": "BQQMF",
        "option_c": "CRQNG",
        "option_d": "DSSOH",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 2 positions.",
    },
    {
        "question_text": "If ROAD is coded as URDG, how is MILK coded?",
        "option_a": "PLON",
        "option_b": "PLOM",
        "option_c": "QMPN",
        "option_d": "NJML",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 3 positions.",
    },
    {
        "question_text": "If KING is coded as MKPI, how is QUEEN coded?",
        "option_a": "SWGGP",
        "option_b": "RVFFO",
        "option_c": "SWFFP",
        "option_d": "TXHHQ",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 2 positions.",
    },
    {
        "question_text": "If SOUTH is coded as TPVUI, how is NORTH coded?",
        "option_a": "OPSUI",
        "option_b": "OPSTI",
        "option_c": "NPSUI",
        "option_d": "PQTUJ",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 1 position.",
    },
    {
        "question_text": "If TRAIN is coded as WUDLQ, how is PLANE coded?",
        "option_a": "SODQH",
        "option_b": "SODPH",
        "option_c": "QMBOF",
        "option_d": "TPERI",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 3 positions.",
    },
    {
        "question_text": "If BLACK is coded as AKZBJ, how is WHITE coded?",
        "option_a": "VGHSD",
        "option_b": "XIJUF",
        "option_c": "VGHQD",
        "option_d": "WGITE",
        "correct_option": "A",
        "explanation": "Each letter is shifted backward by 1 position.",
    },
    {
        "question_text": "If MONDAY is coded as NPOEBZ, how is FRIDAY coded?",
        "option_a": "GSJEBZ",
        "option_b": "GSJECZ",
        "option_c": "FRJEBZ",
        "option_d": "HTKFCZ",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 1 position.",
    },
    {
        "question_text": "If ZERO is coded as AFSP, how is ONE coded?",
        "option_a": "POF",
        "option_b": "PNF",
        "option_c": "QPG",
        "option_d": "OND",
        "correct_option": "A",
        "explanation": "Each letter moves one position forward, with Z wrapping to A.",
    },
    {
        "question_text": "If MATH is coded as NZUI, how is CODE coded?",
        "option_a": "DPEF",
        "option_b": "DPFE",
        "option_c": "EQFG",
        "option_d": "CNCD",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 1 position.",
    },
    {
        "question_text": "If EARTH is coded as FBSUI, how is WORLD coded?",
        "option_a": "XPSME",
        "option_b": "XQSME",
        "option_c": "WPSME",
        "option_d": "YQTNF",
        "correct_option": "A",
        "explanation": "Each letter is shifted forward by 1 position.",
    },
    {
        "question_text": "If TIGER is coded as 20-9-7-5-18, how is LION coded?",
        "option_a": "12-9-15-14",
        "option_b": "11-9-15-14",
        "option_c": "12-8-15-14",
        "option_d": "12-9-14-15",
        "correct_option": "A",
        "explanation": "Using alphabet positions: L=12, I=9, O=15, N=14.",
    },
    {
        "question_text": "If PEN is coded as 35 and CAT is coded as 24 by adding alphabet positions, what is DOG coded as?",
        "option_a": "24",
        "option_b": "25",
        "option_c": "26",
        "option_d": "27",
        "correct_option": "C",
        "explanation": "D=4, O=15 and G=7. Total = 26.",
    },
    {
        "question_text": "If BAD is coded as 214 and FACE as 6135, how is BED coded?",
        "option_a": "254",
        "option_b": "245",
        "option_c": "2514",
        "option_d": "2541",
        "correct_option": "A",
        "explanation": "B=2, E=5 and D=4, so BED = 254.",
    },
    {
        "question_text": "If SCHOOL is coded as LOOHCS, how is MARKET coded?",
        "option_a": "TEKRAM",
        "option_b": "TEKRMA",
        "option_c": "MARKET",
        "option_d": "TAKREM",
        "correct_option": "A",
        "explanation": "The word is reversed. MARKET becomes TEKRAM.",
    },
    {
        "question_text": "If APPLE is coded as ELPPA, how is ORANGE coded?",
        "option_a": "EGNARO",
        "option_b": "EGNRAO",
        "option_c": "ORANGE",
        "option_d": "EGRANO",
        "correct_option": "A",
        "explanation": "The coding rule reverses the word.",
    },
    {
        "question_text": "If ABC is coded as BCD and XYZ is coded as YZA, how is PQR coded?",
        "option_a": "QRS",
        "option_b": "RSP",
        "option_c": "QRT",
        "option_d": "PRS",
        "correct_option": "A",
        "explanation": "Each letter moves one position forward.",
    },
    {
        "question_text": "If CAT is coded as 3×1×20, what is the product value of BAT?",
        "option_a": "20",
        "option_b": "40",
        "option_c": "60",
        "option_d": "80",
        "correct_option": "B",
        "explanation": "B=2, A=1, T=20. Product = 2×1×20 = 40.",
    },
    {
        "question_text": "If DOG is coded as 4+15+7, what is the code value of LION?",
        "option_a": "48",
        "option_b": "49",
        "option_c": "50",
        "option_d": "51",
        "correct_option": "C",
        "explanation": "L=12, I=9, O=15, N=14. Total = 50.",
    },
    {
        "question_text": "If A=26, B=25, C=24 and so on in reverse order, what is the value of CAT?",
        "option_a": "55",
        "option_b": "56",
        "option_c": "57",
        "option_d": "58",
        "correct_option": "C",
        "explanation": "C=24, A=26, T=7. Total = 24+26+7 = 57.",
    },
    {
        "question_text": "If DELHI is coded as 4-5-12-8-9, how is INDIA coded?",
        "option_a": "9-14-4-9-1",
        "option_b": "8-14-4-9-1",
        "option_c": "9-13-4-9-1",
        "option_d": "9-14-5-9-1",
        "correct_option": "A",
        "explanation": "Using alphabet positions: I=9, N=14, D=4, I=9, A=1.",
    },
    {
        "question_text": "If DELHI is coded as IHLED, how is MUMBAI coded?",
        "option_a": "IABMUM",
        "option_b": "IABUMM",
        "option_c": "MUMBAI",
        "option_d": "IAMBUM",
        "correct_option": "A",
        "explanation": "The word is reversed. MUMBAI becomes IABMUM.",
    },
    {
        "question_text": "If COMPUTER is coded by shifting every letter one place forward, what are the first four coded letters?",
        "option_a": "DPNQ",
        "option_b": "DPNT",
        "option_c": "CQNP",
        "option_d": "EPOQ",
        "correct_option": "A",
        "explanation": "C→D, O→P, M→N and P→Q, giving DPNQ.",
    },
    {
        "question_text": "If FLOWER is coded as HNQYGT by shifting each letter two places forward, how is GARDEN coded?",
        "option_a": "ICTFGP",
        "option_b": "HBSFEO",
        "option_c": "ICUEGP",
        "option_d": "JDUHGP",
        "correct_option": "A",
        "explanation": "G→I, A→C, R→T, D→F, E→G, N→P. Code = ICTFGP.",
    },
    {
        "question_text": "If ZEBRA is coded as AFCSB by moving every letter one step forward, how is TIGER coded?",
        "option_a": "UJHFS",
        "option_b": "TIGFS",
        "option_c": "VKIGT",
        "option_d": "UIHFR",
        "correct_option": "A",
        "explanation": "T→U, I→J, G→H, E→F, R→S. Code = UJHFS.",
    },
]

coding_l2_created = 0
coding_l2_skipped = 0

for data in coding_level2_questions:
    exists = Question.objects.filter(
        subject=lr_subject,
        topic=coding_topic,
        question_text=data["question_text"]
    ).exists()

    if exists:
        coding_l2_skipped += 1
        continue

    Question.objects.create(
        subject=lr_subject,
        topic=coding_topic,
        question_text=data["question_text"],
        option_a=data["option_a"],
        option_b=data["option_b"],
        option_c=data["option_c"],
        option_d=data["option_d"],
        correct_option=data["correct_option"],
        explanation=data["explanation"],
        difficulty_level=2,
        created_by=admin,
        is_global=True,
        status="approved",
    )

    coding_l2_created += 1

print(f"\nCoding-Decoding Level 2 Created: {coding_l2_created}")
print(f"Coding-Decoding Level 2 Skipped: {coding_l2_skipped}")
print("LR -> Coding-Decoding -> Level 2 seeding complete.")

