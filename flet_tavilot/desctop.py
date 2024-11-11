import flet as ft
import os


def main(page):
    page.adaptive = True
    page.theme_mode = ft.ThemeMode.LIGHT
    TC = '#E9BE5F'

    # Function to validate phone number input
    def validate_phone_number():
        phone_number = phone_input.value
        if phone_number.isdigit() and len(phone_number) == 9:  # Basic validation
            page.update()
            open_next_page()
        else:
            result.value = "Invalid phone number. Please enter Uzbek number."
            result.color = ft.colors.RED
        page.update()

    # Event handler for submit event in the phone input field
    def on_submit(e):
        validate_phone_number()

    # Function to open the next page after validation
    def open_next_page():
        # Define the content for the next page (for example, another TextField or layout)
        next_page_content = ft.Column(
            controls=[
                ft.Text("Welcome to the next page!", style="titleLarge", color=TC),
                ft.Text("You successfully entered a valid phone number.", style="bodyMedium"),
                ft.OutlinedButton(
                    text="Go Back",
                    on_click=lambda e: go_back(),
                    width=200,
                    height=50,
                    style=ft.ButtonStyle(color='white', bgcolor=TC, shape=ft.RoundedRectangleBorder(radius=8)),
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
        page.controls.clear()  # Clear the current page content
        page.add(next_page_content)  # Add the next page content
        page.update()

    # Function to navigate back to the original page
    def go_back():
        # Reset the content column to the original state with phone input
        content_column.controls = [
            ft.Text(value="  TA'VILOT \nAL-QURON \n", color=TC, style="displayLarge"),
            ft.Text(value="Assalomu alaykum! \nDavom etish uchun ro'yxatdan o'ting\n", width=400, weight='bold', style="titleLarge"),
            phone_input,
            ft.OutlinedButton(
                text="Davom etish",
                on_click=lambda e: validate_phone_number(),  # Link the button to validation
                width=400,
                height=60,
                style=ft.ButtonStyle(
                    color='white',
                    bgcolor=TC,
                    shape=ft.RoundedRectangleBorder(radius=8),
                )
            ),
            result  # Display validation result here
        ]
        page.update()

    # Phone number input field
    phone_input = ft.TextField(
        prefix_text="+998 ",
        keyboard_type=ft.KeyboardType.NUMBER,
        width=400,
        on_submit=on_submit,
        on_change=lambda e: limit_length(e),
        border_color=TC,
        border_width=2,
        border_radius=10,
        text_style=ft.TextStyle(weight="bold")
    )

    # Function to limit input length to 9 digits
    def limit_length(e):
        if len(phone_input.value) > 9:
            phone_input.value = phone_input.value[:9]
            page.update()

    result = ft.Text()

    # Create a Column for all the fields on the left side
    content_column = ft.Column(
        controls=[
            ft.Text(value="  TA'VILOT \nAL-QURON \n", color=TC, style="displayLarge"),
            ft.Text(value="Assalomu alaykum! \nDavom etish uchun ro'yxatdan o'ting\n", width=400, weight='bold', style="titleLarge"),
            phone_input,
            ft.OutlinedButton(
                text="Davom etish",
                on_click=lambda e: validate_phone_number(),  # Link the button to validation
                width=400,
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
                    width=700,
                    height=900,
                    fit=ft.ImageFit.COVER,
                    border_radius=100
                ),
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
