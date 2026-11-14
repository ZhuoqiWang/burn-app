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
            result0 = w * a * 1.5 + 2000
            result1 = w * a * 1
            result2 = w * a * 0.5
            result3 =2000
            result4 =result0/16
            result5 =result0/32
            result1_0 = w * a * 0.75 + 2000
            result1_1 =result1_0/24
            result1_2 = w * a * 0.5
            result1_3 = w * a * 0.25
            result1_4 =2000
        elif current_type == "child":
            # 儿童：w * a * 1.75 + 50~100*w mL，此处取最小 50*w
            result0 = w * a * 1.75 + 50 * w
            result1 = w * a * 0.875
            result2 = result1
            result3 =50 * w
            result4 =result0/16
            result5 =result0/32
            result1_0 = w * a * 1.75/2 + 50 * w
            result1_1 =result1_0/24
            result1_2 = w * a * 1.75/4
            result1_3 = result1_2
            result1_4 =50 * w
        else:
            # 婴儿：w * a * 2 + 100*w mL
            result0 = w * a * 2 + 100 * w
            result1 = w * a 
            result2 = result1
            result3 =100 * w
            result4 =result0/16
            result5 =result0/32
            result1_0 = w * a  + 100 * w
            result1_1 =result1_0/24
            result1_2 = w * a /2
            result1_3 = result1_2
            result1_4 =100 * w
        result_text.value = f"第一天\n        预计补液总量：{result0:.1f} mL\n                晶体：{result1:.1f} mL；胶体：{result2:.1f} mL；水：{result3:.1f} mL\n        补液速度：\n                前8 h：{result4:.1f} mL/h；后16 h：{result5:.1f} mL/h\n第二天\n        预计补液总量：{result1_0:.1f} mL\n                晶体：{result1_2:.1f} mL；胶体：{result1_3:.1f} mL；水：{result1_4:.1f} mL\n        补液速度：\n                {result1_1:.1f} mL/h"
        result_text.color = ft.Colors.GREEN_700
        page.update()

    page.add(
        ft.Text("烧伤补液计算", size=26, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        type_display,
        ft.Row(
            [
                make_button("成人", "adult"),
                make_button("儿童（大于2岁）", "child"),
                make_button("儿童（小于2岁）", "infant"),
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
