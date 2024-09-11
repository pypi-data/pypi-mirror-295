import qrcode
from colorama import init, Fore
import uuid
import os

# Инициализация colorama
init(autoreset=True)

class PorkofQRCode():
    def __init__(self):
        self.qr = None

    def create_qr_code(self, data, filename=None, box_size=10, border=4):
        # Создание экземпляра QRCode
        self.qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=box_size,
            border=border,
        )
    
        # Добавление данных в QR-код
        self.qr.add_data(data)
        self.qr.make(fit=True)
    
        # Генерация изображения QR-кода с инвертированными цветами
        img = self.qr.make_image(fill_color="white", back_color="black")
    
        # Генерация случайного имени файла, если не указано
        if filename is None:
            filename = f".qr_code_{uuid.uuid4().hex[:6]}.png"
    
        # Сохранение QR-кода в файл
        img.save(filename)
        
        """Выводит QR-код в текстовом формате в терминал."""
        matrix = self.qr.get_matrix()
        for row in matrix:
            line = ''.join(['██' if not col else '  ' for col in row])
            print(Fore.WHITE + line)
        os.remove(filename)

if __name__ == "__main__":
    # Пример использования
    create_qr_code = PorkofQRCode()
    create_qr_code.create_qr_code("https://www.example.com")
