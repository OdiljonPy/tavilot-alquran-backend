import flet as ft
import os

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
            result.value = "Invalid phone number. Please enter Uzbek number."
            result.color = ft.colors.RED
        page.update()

    # Phone number input field
    phone_input = ft.TextField(
        hint_text="+998",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=298,
        on_submit=on_submit,
        border_color=TC,
        border_width=2,
        border_radius=10
    )

    result = ft.Text()

    # Create a Column for all the fields on the left side
    content_column = ft.Column(
        controls=[
            ft.Text(value="  TA'VILOT \nAL-QURON \n\n", color=TC, style="headlineMedium"),
            ft.Text(value="Assalomu alaykum! \nDavom etish uchun ro'yxatdan o'ting", weight='bold', style="bodyLarge"),
            phone_input,
            ft.OutlinedButton(
                text="Davom etish",
                on_click=lambda e: print("Outlined Button clicked!"),
                width=298,
                height=60,
                style=ft.ButtonStyle(
                    color='white',
                    bgcolor=TC,
                    shape=ft.RoundedRectangleBorder(radius=8),
                )
            ),
            result  # Display validation result here
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Define a Row that contains the content column and the image with rounded borders
    layout_with_image = ft.Row(
        controls=[
            content_column,
            ft.Container(
                content=ft.Image(
                    src=os.path.abspath("assets/tavilot_book.png"),
                    width=400,
                    height=900,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=5
                ),
                # border_radius=ft.BorderRadius.top_right,  # Apply border radius to the container
                clip_behavior=ft.ClipBehavior.ANTI_ALIAS,  # Enable anti-aliasing for smoother edges
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,  # Spread content and image to left and right
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Wrap layout_with_image in a Container to center it on the page
    centered_container = ft.Container(
        content=layout_with_image,
        alignment=ft.alignment.center,  # Center the entire row in the middle of the page
        expand=True,  # Make the container expand to fill the page
    )

    # Add the centered container to the page
    page.add(centered_container)
    page.update()

ft.app(target=main)
