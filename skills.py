skills = ["Атлетика", "Драка", "Фехтование", "Стрельба", "Запугивание", "Оккультизм", "Шестое", "Бдительность", "Обращение", "Расследование", "Красноречие", "Исполнение", "Хитрость", "Эмпатия", "Этикет", "Законы", "Политика", "Финансы", "Лидерство", "Уличное", "Воровство", "Скрытность", "Выживание", "Ремесло", "Вождение", "Гуманитарные", "Естественные", "Медицина", "Информатика", "Электроника"]
lower_skills = [string.lower() for string in skills]
categories = ["Грубая сила", "Восприятие", "Обаяние", "Социология", "Ловкость рук", "Ученость"]

skills_by_cats = {}
skills_by_cats["Грубая сила"] = ["Атлетика", "Драка", "Фехтование", "Стрельба", "Запугивание"]
skills_by_cats["Восприятие"] = ["Оккультизм", "Шестое чувство", "Бдительность", "Обращение с животными", "Расследование"]
skills_by_cats["Обаяние"] = ["Красноречие", "Исполнение", "Хитрость", "Эмпатия", "Этикет"]
skills_by_cats["Социология"] = ["Законы", "Политика", "Финансы", "Лидерство", "Уличное чутье"]
skills_by_cats["Ловкость рук"] = ["Воровство", "Скрытность", "Выживание", "Ремесло", "Вождение"]
skills_by_cats["Ученость"] = ["Гуманитарные науки", "Естественные науки", "Медицина", "Информатика", "Электроника"]
