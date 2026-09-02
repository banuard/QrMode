import flet as ft
import qrcode
import base64
from io import BytesIO
import webbrowser

# Функция для генерации QR-кода и преобразования его в изображение для Flet
def generate_qr_image(data: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Конвертируем изображение в байты, чтобы показать его в Flet
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return ft.Image(src_base64=img_str, width=200, height=200)

def main(page: ft.Page):
    page.title = "QR Scanner & Generator"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.Colors.GREY_900

    # Поле для вывода отсканированного текста
    result_text = ft.Text("Здесь будет результат сканирования", size=16, color=ft.Colors.WHITE70)
    qr_image_display = ft.Container(content=ft.Text("Здесь будет QR-код"), padding=10)

    def handle_scanned_data(e):
        """Обработчик данных, полученных после сканирования QR-кода"""
        scanned_data = e.data
        result_text.value = f"Отсканировано: {scanned_data}"
        # Генерируем новый QR-код из отсканированных данных
        qr_image_display.content = generate_qr_image(scanned_data)
        page.update()

    def scan_qr_code(e):
        """Открывает веб-страницу для сканирования QR-кода"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>QR Scanner</title>
            <script src="https://unpkg.com/html5-qrcode"></script>
        </head>
        <body>
            <div id="reader" style="width: 300px;"></div>
            <script>
                function onScanSuccess(decodedText, decodedResult) {
                    window.location.href = "flet://scan?data=" + encodeURIComponent(decodedText);
                }
                var html5QrcodeScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 });
                html5QrcodeScanner.render(onScanSuccess);
            </script>
        </body>
        </html>
        """
        webbrowser.open("data:text/html;charset=utf-8," + html_content)

    scan_button = ft.ElevatedButton(
        "📷 Открыть сканер",
        on_click=scan_qr_code,
        icon=ft.Icons.CAMERA_ALT,
        bgcolor=ft.Colors.BLUE_400,
        color=ft.Colors.WHITE
    )

    # Добавляем элементы на страницу
    page.add(
        ft.Text("QR Scanner & Generator", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_300),
        scan_button,
        ft.Divider(height=20),
        result_text,
        ft.Divider(height=20),
        ft.Text("Сгенерированный QR-код:", size=16, color=ft.Colors.WHITE70),
        qr_image_display,
    )

# ========== ИСПРАВЛЕННЫЙ ЗАПУСК ==========
ft.run(main)  # ← БЕЗ target=
