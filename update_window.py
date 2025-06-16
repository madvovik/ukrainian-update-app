import tkinter as tk
from tkinter import ttk
import random


class InteractiveUpdateWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Оновлення")

        # Получаем размеры экрана
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Устанавливаем размеры окна
        window_width = 500
        window_height = 300

        # Вычисляем координаты для центрирования окна
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        # Устанавливаем позицию окна по центру экрана
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.configure(bg='white')

        # Состояние программы
        self.mouse_move_count = 0
        self.is_flashing = False
        self.flash_job = None
        self.move_job = None
        self.original_pos = (x, y)
        self.last_move_time = 0
        self.can_advance = True
        self.advance_job = None
        self.is_running_away = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.run_away_job = None

        # Создаем основной текст
        self.main_label = ttk.Label(
            self.root,
            text="ОНОВЛЕННЯ ПРОГРАМИ!\nОЧІКУЙТЕ!",
            font=("Arial", 16, "bold"),
            justify="center"
        )
        self.main_label.pack(pady=20)

        # Создаем предупреждающий текст
        self.warning_label = tk.Label(
            self.root,
            text="НЕ ЧІПАЙ МИШКУ!",
            font=("Arial", 12, "bold"),
            fg="red",
            bg="white"
        )
        self.warning_label.pack(pady=10)

        # Прогресс бар (для красоты)
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(pady=20)
        self.progress.start(10)

        # Привязываем события мыши
        self.root.bind('<Motion>', self.on_mouse_move)
        self.root.bind('<Button-1>', self.on_mouse_click)

        # Делаем окно всегда поверх других
        self.root.attributes('-topmost', True)

    def on_mouse_move(self, event):
        """Обработчик движения мыши"""
        import time

        # Если окно убегает, не обрабатываем обычную логику
        if self.is_running_away:
            return

        # Проверяем, можем ли мы продвинуться на следующий этап
        if not self.can_advance:
            return

        current_time = time.time()

        # Если прошло меньше 5 секунд с последнего движения, игнорируем
        if current_time - self.last_move_time < 5.0 and self.mouse_move_count > 0:
            return

        self.last_move_time = current_time
        self.mouse_move_count += 1
        self.can_advance = False  # Блокируем продвижение

        if self.mouse_move_count == 1:
            self.first_warning()
        elif self.mouse_move_count == 2:
            self.second_warning()
        elif self.mouse_move_count == 3:
            self.third_warning()
        elif self.mouse_move_count == 4:
            self.fourth_warning()
        elif self.mouse_move_count == 5:
            self.fifth_warning()
        elif self.mouse_move_count >= 6:
            self.final_chaos()

        # Разблокируем продвижение через 5 секунд
        self.advance_job = self.root.after(5000, self.enable_advance)

    def enable_advance(self):
        """Разрешает переход на следующий этап"""
        self.can_advance = True

    def on_mouse_click(self, event):
        """Обработчик клика мыши"""
        # Если окно убегает, блокируем все клики
        if self.is_running_away:
            return
        # Клик тоже считается как движение, но не ускоряет процесс
        self.on_mouse_move(event)

    def first_warning(self):
        """Первое предупреждение"""
        self.warning_label.config(
            text="Я СКАЗАВ МИШКУ ПОКЛАДИ!\n(Почекай 5 секунд перед наступним рухом)",
            fg="red",
            font=("Arial", 12, "bold")
        )
        self.root.configure(bg='#ffeeee')

    def second_warning(self):
        """Второе предупреждение с морганием"""
        self.warning_label.config(
            text="ЯКЩО ЩЕ РАЗ ДОТОРКНЕШСЯ, Я ОБРАЗЖУСЯ!\n(Серйозно, почекай 5 секунд!)",
            font=("Arial", 14, "bold")
        )
        self.start_flashing()

    def third_warning(self):
        """Третье предупреждение"""
        self.stop_flashing()
        self.warning_label.config(
            text="ВСЕ! Я ОБРАЗИВСЯ! 😠",
            fg="darkred",
            font=("Arial", 18, "bold")
        )
        self.root.configure(bg='#ffcccc')

    def fourth_warning(self):
        """Четвертое предупреждение с тряской"""
        self.warning_label.config(
            text="ДОСИТЬ МЕНЕ ЗЛИТИ! 😡💢",
            font=("Arial", 20, "bold")
        )
        self.start_shaking()

    def fifth_warning(self):
        """Пятое предупреждение"""
        self.stop_shaking()
        self.warning_label.config(
            text="ОСТАННЄ ПОПЕРЕДЖЕННЯ! ⚠️",
            fg="red",
            font=("Arial", 22, "bold")
        )
        self.root.configure(bg='red')
        self.main_label.config(background='red', foreground='white')

    def final_chaos(self):
        """Финальный хаос"""
        chaos_messages = [
            "ВСЕ! ТИ МЕНЕ ДОВІВ! 🤬",
            "ЗАРАЗ Я РОЗКАЖУ ТВОЇЙ МАМІ! 📞",
            "ВИДАЛЯЮ ВСІ ТВОЇ \nФАЙЛИ... І Я НЕ ЖАРТУЮ! 😈",
            "СЕРЙОЗНО, ЗУПИНИСЯ, \nМЕНІ ВЖЕ НЕМА ЧТОГО ВИДАЛЯТИ! 🛑",
            "ГАРАЗД, ТИ ПЕРЕМІГ... Я ЗДАЮСЯ 😭",
            "ДОБРЕ, ДАВАЙ ДРУЖИТИ? 🤝"
        ]

        message_index = min(self.mouse_move_count - 6, len(chaos_messages) - 1)
        self.warning_label.config(
            text=chaos_messages[message_index],
            font=("Arial", 16, "bold")
        )

        # На этапе "удаления файлов" - окно начинает убегать
        if self.mouse_move_count == 8:  # "ВИДАЛЯЮ ВСІ ТВОЇ ФАЙЛИ"
            self.start_running_away()

        # Случайный цвет фона
        colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
        self.root.configure(bg=random.choice(colors))

        # Если пользователь продолжает, показываем "примирение"
        if self.mouse_move_count >= 12:
            self.reconciliation()

    def reconciliation(self):
        """Примирение с пользователем"""
        self.stop_all_effects()
        self.root.configure(bg='lightgreen')
        self.main_label.config(
            text="ОНОВЛЕННЯ ЗАВЕРШЕНО! ✅\nДЯКУЮ ЗА ТЕРПІННЯ! 😊",
            background='lightgreen'
        )
        self.warning_label.config(
            text="Ми тепер друзі! 🤗",
            fg="green",
            bg="lightgreen",
            font=("Arial", 14, "bold")
        )

        # Безопасно останавливаем и удаляем прогресс-бар
        try:
            if self.progress and self.progress.winfo_exists():
                self.progress.stop()
                self.progress.destroy()
        except:
            pass

        # Кнопка закрытия
        close_btn = tk.Button(
            self.root,
            text="Закрити",
            command=self.root.destroy,
            font=("Arial", 12),
            bg="white"
        )
        close_btn.pack(pady=20)

    def start_flashing(self):
        """Запуск эффекта мигания"""
        if not self.is_flashing:
            self.is_flashing = True
            self.flash()

    def flash(self):
        """Эффект мигания экрана"""
        if self.is_flashing:
            current_color = self.root.cget('bg')
            new_color = 'red' if current_color != 'red' else 'white'
            self.root.configure(bg=new_color)
            self.flash_job = self.root.after(200, self.flash)

    def stop_flashing(self):
        """Остановка мигания"""
        self.is_flashing = False
        if self.flash_job:
            self.root.after_cancel(self.flash_job)

    def start_shaking(self):
        """Запуск эффекта тряски окна"""
        self.shake_window()

    def shake_window(self):
        """Эффект тряски окна"""
        if self.mouse_move_count == 4:  # Трясти только на 4-м этапе
            x_offset = random.randint(-10, 10)
            y_offset = random.randint(-10, 10)
            new_x = self.original_pos[0] + x_offset
            new_y = self.original_pos[1] + y_offset
            self.root.geometry(f"500x300+{new_x}+{new_y}")
            self.move_job = self.root.after(50, self.shake_window)

    def stop_shaking(self):
        """Остановка тряски"""
        if self.move_job:
            self.root.after_cancel(self.move_job)
        # Возвращаем окно в центр
        self.root.geometry(f"500x300+{self.original_pos[0]}+{self.original_pos[1]}")

    def start_running_away(self):
        """Запуск режима убегания от мыши"""
        self.is_running_away = True
        self.warning_label.config(
            text="СПРОБУЙ МЕНЕ ПІЙМАТИ! 🏃‍♂️💨\n(Я ВТІКАЮ ВІД ТВОЄЇ МИШКИ!)",
            fg="yellow",
            bg="darkred",
            font=("Arial", 14, "bold")
        )
        self.root.configure(bg='darkred')
        self.run_away_from_mouse()

        # Останавливаем убегание через 10 секунд
        self.root.after(10000, self.stop_running_away_and_continue)

    def run_away_from_mouse(self):
        """Убегание от мыши"""
        if not self.is_running_away:
            return

        try:
            # Получаем позицию мыши относительно экрана
            mouse_x = self.root.winfo_pointerx()
            mouse_y = self.root.winfo_pointery()

            # Получаем текущую позицию окна
            window_x = self.root.winfo_x()
            window_y = self.root.winfo_y()
            window_center_x = window_x + 250  # центр окна по X
            window_center_y = window_y + 150  # центр окна по Y

            # Вычисляем расстояние от мыши до центра окна
            distance_x = window_center_x - mouse_x
            distance_y = window_center_y - mouse_y
            distance = (distance_x ** 2 + distance_y ** 2) ** 0.5

            # Если мышь близко (меньше 200 пикселей), убегаем
            if distance < 200:
                # Определяем направление убегания (в противоположную сторону от мыши)
                if distance_x >= 0:
                    new_x = window_x + 80  # Убегаем вправо
                else:
                    new_x = window_x - 80  # Убегаем влево

                if distance_y >= 0:
                    new_y = window_y + 80  # Убегаем вниз
                else:
                    new_y = window_y - 80  # Убегаем вверх

                # Проверяем границы экрана и телепортируемся на противоположную сторону
                if new_x < 0:
                    new_x = self.screen_width - 520
                elif new_x > self.screen_width - 500:
                    new_x = 20

                if new_y < 0:
                    new_y = self.screen_height - 320
                elif new_y > self.screen_height - 300:
                    new_y = 20

                # Перемещаем окно
                self.root.geometry(f"500x300+{new_x}+{new_y}")

            # Продолжаем отслеживание мыши
            if self.is_running_away:
                self.run_away_job = self.root.after(30, self.run_away_from_mouse)

        except Exception:
            # Если произошла ошибка, останавливаем убегание
            self.stop_running_away()

    def stop_running_away(self):
        """Остановка убегания"""
        self.is_running_away = False
        if self.run_away_job:
            self.root.after_cancel(self.run_away_job)

    def stop_running_away_and_continue(self):
        """Остановка убегания и переход к следующему этапу"""
        self.stop_running_away()
        # Возвращаем окно в центр
        self.root.geometry(f"500x300+{self.original_pos[0]}+{self.original_pos[1]}")

        # Увеличиваем счетчик и показываем следующее сообщение
        self.mouse_move_count += 1
        self.can_advance = True

        # Показываем следующее сообщение из chaos_messages
        if self.mouse_move_count < 12:
            self.final_chaos()
        else:
            self.reconciliation()

    def stop_all_effects(self):
        """Остановка всех эффектов"""
        self.stop_flashing()
        self.stop_shaking()
        self.stop_running_away()
        if self.advance_job:
            self.root.after_cancel(self.advance_job)

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()


# Запуск программы
if __name__ == "__main__":
    app = InteractiveUpdateWindow()
    app.run()
