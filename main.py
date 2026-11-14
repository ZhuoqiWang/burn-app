import flet as ft


def main(page: ft.Page):
    page.title = "烧伤补液、能量计算器"
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
        label="体重 (kg)",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="请输入体重",
    )
    area_input = ft.TextField(
        label="烧伤面积 (%)",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="请输入烧伤面积百分比",
    )
    area0_input = ft.TextField(
        label="烧伤体表面积 (m²)",
        keyboard_type=ft.KeyboardType.NUMBER,
        hint_text="请输入烧伤体表面积",
    )

    # 第一天结果（绿色）
    result_day1 = ft.Text(
        "",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.GREEN_700,
        selectable=True,
    )
    # 第二天结果（蓝色）
    result_day2 = ft.Text(
        "",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE_700,
        selectable=True,
    )
    # 热量结果（橙色）
    result_heat = ft.Text(
        "",
        size=18,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.ORANGE_700,
        selectable=True,
    )


    def select_type(e):
        nonlocal current_type
        current_type = e.control.data
        type_map = {"adult": "成人", "child": "儿童（大于2岁）", "infant": "儿童（小于2岁）"}
        type_display.value = f"当前选择：{type_map[current_type]}"
        page.update()

    def make_button(label, value):
        return ft.Button(
            content=ft.Text(label, text_align=ft.TextAlign.CENTER),
            data=value,
            on_click=select_type,
            expand=True,
        )


    def calculate(e):
        try:
            w = float(weight_input.value)
            a = float(area_input.value)
            a0 = float(area0_input.value)
        except (ValueError, TypeError):
            result_day1.value = "❌ 请输入有效的数字"
            result_day1.color = ft.Colors.RED_700
            result_day2.value = ""
            result_heat.value = ""
            page.update()
            return


        if w <= 0 or a <= 0 or a0 <= 0:
            result_day1.value = "❌ 体重和面积必须大于 0"
            result_day1.color = ft.Colors.RED_700
            result_day2.value = ""
            result_heat.value = ""
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

        # 热量计算
        heat = (4184 * a0 + 104.6 * a) / 4.184

        # 第一天：绿色
        result_day1.value = (
            f"【第一天】\n"
            f"预计补液总量：{result0:.1f} mL\n"
            f"晶体：{result1:.1f} mL；\n"
            f"胶体：{result2:.1f} mL；\n"
            f"水：{result3:.1f} mL\n"
            f"补液速度：\n"
            f"前8 h：{result4:.1f} mL/h；\n"
            f"后16 h：{result5:.1f} mL/h"
        )
        result_day1.color = ft.Colors.GREEN_700

        # 第二天：蓝色
        result_day2.value = (
            f"【第二天】\n"
            f"预计补液总量：{result1_0:.1f} mL\n"
            f"晶体：{result1_2:.1f} mL；\n"
            f"胶体：{result1_3:.1f} mL；\n"
            f"水：{result1_4:.1f} mL\n"
            f"补液速度：\n"
            f"{result1_1:.1f} mL/h"
        )
        result_day2.color = ft.Colors.BLUE_700

        # 热量：橙色
        result_heat.value = f"热量：{heat:.1f} kcal/天"
        result_heat.color = ft.Colors.ORANGE_700

        page.update()

    page.add(
        ft.Container(height=60),   # 顶部占位，控制下移距离
        ft.Text("烧伤补液、能量计算", size=26, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        type_display,
        ft.Row(
            [
                make_button("成人", "adult"),
                make_button("儿童\n>2岁", "child"),
                make_button("儿童\n<2岁", "infant"),
            ],
            spacing=10,
        ),
        ft.Divider(height=20),
        weight_input,
        area_input, 
        area0_input,
        ft.Divider(height=10),
        ft.Button(
            "计算补液量",
            on_click=calculate,
            width=float("inf"),
            style=ft.ButtonStyle(padding=15),
        ),
        ft.Divider(height=10),
        result_day1,
        ft.Divider(height=10),
        result_day2,
        ft.Divider(height=10),
        result_heat,
    )


ft.run(main)
