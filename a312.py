import flet as ft


def main(page: ft.Page):
    page.title = "烧伤补液量计算器"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 30
    page.scroll = ft.ScrollMode.AUTO

    current_type = "adult"

    type_display = ft.Text(
        "当前选择：成人",
        size=16,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
    )

    weight_input = ft.TextField(
        label="体重 w (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="请输入体重",
    )
    area_input = ft.TextField(
        label="烧伤面积 a (%)",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="请输入烧伤面积百分比",
    )

    result_text = ft.Text(
        "",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_700,
        selectable=True,
    )

    def select_type(e):
        nonlocal current_type
        current_type = e.control.data
        type_map = {"adult": "成人", "child": "儿童", "infant": "婴儿"}
        type_display.value = f"当前选择：{type_map[current_type]}"
        page.update()

    def make_button(label, value):
        return ft.Button(
            label,
            data=value,
            on_click=select_type,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=20,
            ),
            expand=True,
        )

    def calculate(e):
        try:
            w = float(weight_input.value)
            a = float(area_input.value)
        except (ValueError, TypeError):
            result_text.value = "❌ 请输入有效的数字"
            result_text.color = ft.Colors.RED_700
            page.update()
            return

        if w <= 0 or a <= 0:
            result_text.value = "❌ 体重和面积必须大于 0"
            result_text.color = ft.Colors.RED_700
            page.update()
            return

        if current_type == "adult":
            # 成人：w * a * 1.5 + 2000 mL
            result = w * a * 1.5 + 2000
        elif current_type == "child":
            # 儿童：w * a * 1.8 + 60~80*w mL，此处取中位值 70*w
            result = w * a * 1.8 + 70 * w
        else:
            # 婴儿：w * a * 2 + 100*w mL
            result = w * a * 2 + 100 * w

        result_text.value = f"预计补液总量：{result:.1f} mL"
        result_text.color = ft.Colors.GREEN_700
        page.update()

    page.add(
        ft.Text("烧伤补液量计算", size=26, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        type_display,
        ft.Row(
            [
                make_button("成人", "adult"),
                make_button("儿童", "child"),
                make_button("婴儿", "infant"),
            ],
            spacing=10,
        ),
        ft.Divider(height=20),
        weight_input,
        area_input,
        ft.Divider(height=10),
        ft.Button(
            "计算补液量",
            on_click=calculate,
            width=float("inf"),
            style=ft.ButtonStyle(padding=15),
        ),
        ft.Divider(height=10),
        result_text,
    )


ft.run(main)