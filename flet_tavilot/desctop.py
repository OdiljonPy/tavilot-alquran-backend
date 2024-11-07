import flet as ft

import os
print(os.path.abspath("assets/tavilot_book.png/"))

def main(page):
    page.adaptive = True
    page.theme_mode = ft.ThemeMode.LIGHT
    TC = '#E9BE5F'

    # Function to validate phone number input
    def on_submit(e):
        phone_number = phone_input.value
        if phone_number.isdigit() and len(phone_number) >= 14:  # Basic validation
            result.value = f"Phone Number Entered: {phone_number}"
            result.color = ft.colors.GREEN
        else:
            result.value = "Invalid phone number. Please enter uzbek number."
            result.color = ft.colors.RED
        page.update()

    # Phone number input field
    phone_input = ft.TextField(
        hint_text="+998",
        keyboard_type=ft.KeyboardType.NUMBER,  # Show numeric keyboard on mobile
        on_submit=on_submit,
    )

    phone_input = ft.TextField(hint_text="+998", keyboard_type=ft.KeyboardType.NUMBER, width=298, on_submit=on_submit,
                               border_color=TC, border_width=2, border_radius=10)

    result = ft.Text()

    first_text = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(value="  TA'VILOT \nAL-QURON \n\n", color=TC, style="headlineMedium"),
                ft.Text(value="Assalomu alaykum! \nDavom etish uchun ro'yxatdan o'ting", weight='bold',
                        style="bodyLarge"),
                phone_input,
                ft.OutlinedButton(
                    text="Davom etish",
                    on_click=lambda e: print("Outlined Button clicked!"),
                    width=298,
                    height=60,
                    style=ft.ButtonStyle(
                        color='white',
                        bgcolor=TC,
                        shape=ft.RoundedRectangleBorder(radius=8),  # Rounded corners
                    )
                ),
                ft.Text(value='Abbos'),
                ft.Image(src=f"/assets/tavilot_book.png", width=100, height=100, fit=ft.ImageFit.CONTAIN),
                ft.Text(value='Abbos')
        ],
        alignment = ft.MainAxisAlignment.CENTER,
        horizontal_alignment = ft.CrossAxisAlignment.CENTER,
        ),
        expand = True,  # Expand to fill the page
        padding = 20,
        alignment = ft.alignment.center,

    )

    page.add(first_text)
    page.update()

ft.app(target=main)
