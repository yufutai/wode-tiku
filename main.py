import os
import re
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.clock import Clock

# --- 1. 数据加载模块 ---
def load_questions():
    # 优先尝试读取外部文件
    file_path = '/sdcard/Download/题目.txt' # 安卓路径
    # file_path = '题目.txt' # 电脑调试路径
    
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except:
            return "❌ 文件读取失败，请检查文件路径和权限。"
    else:
        return "⚠️ 未找到 '题目.txt'，请将其放入手机的 Download 文件夹。"

# --- 2. 搜索逻辑模块 ---
def search_in_text(text, keyword):
    if not keyword:
        return ["请输入关键词..."]
    
    results = []
    # 简单的按行搜索，你可以根据文档结构调整正则
    lines = text.split('\n')
    for line in lines:
        if keyword.lower() in line.lower():
            results.append(f"🔍 {line}")
    return results if results else ["未找到相关结果。"]

# --- 3. 界面构建 ---
class SearchWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.width = dp(350)
        self.height = dp(500)
        
        # --- 顶部栏 (含时空信息) ---
        top_bar = BoxLayout(size_hint_y=None, height=dp(40), padding=5, spacing=10)
        top_bar.add_widget(Label(text='📅 2026-04-25 | 📍 黑龙江省大庆市', 
                                color=(0, 1, 1, 1), bold=True))
        self.add_widget(top_bar)

        # --- 搜索框 ---
        self.search_input = TextInput(
            hint_text='输入题目关键词...',
            multiline=False,
            size_hint_y=None,
            height=dp(40),
            padding=[10, 10]
        )
        self.search_input.bind(on_text_validate=self.do_search) # 绑定回车键
        self.add_widget(self.search_input)

        # --- 搜索按钮 ---
        btn = Button(text='开始搜索', size_hint_y=None, height=dp(50))
        btn.bind(on_press=self.do_search)
        self.add_widget(btn)

        # --- 结果显示区 (带滚动) ---
        scroll = ScrollView(size_hint=(1, 1))
        self.result_label = Label(
            text='等待搜索...\n\n(请确保题目.txt在Download文件夹)',
            size_hint_y=None,
            padding=[10, 10],
            text_size=(self.width - 20, None),
            valign='top'
        )
        scroll.add_widget(self.result_label)
        self.add_widget(scroll)

        # --- 加载题目 ---
        self.question_db = load_questions()
        self.result_label.text = f"✅ 题库加载成功\n共 {len(self.question_db.split('【第'))-1} 道题目"

    def do_search(self, instance):
        keyword = self.search_input.text
        results = search_in_text(self.question_db, keyword)
        self.result_label.text = '\n\n'.join(results)
        self.result_label.height = len(results) * 25 # 动态调整高度

# --- 4. App 主程序 ---
class SearchApp(App):
    def build(self):
        # --- 关键设置：悬浮与置顶 ---
        Window.size = (350, 500)
        Window.top = 100 # 距离顶部距离
        Window.left = Window.width - 360 # 默认停靠在右下角
        Window.borderless = True # 无边框
        Window.clearcolor = (0.1, 0.1, 0.1, 0.9) # 背景色+透明度
        
        # 允许窗口拖动
        self.root = SearchWidget()
        self._offset_x = 0
        self._offset_y = 0
        
        # 绑定鼠标/触摸事件实现拖拽
        self.root.bind(on_touch_down=self.start_drag)
        self.root.bind(on_touch_move=self.do_drag)
        
        return self.root

    def start_drag(self, instance, touch):
        if self.root.collide_point(*touch.pos):
            self._offset_x = touch.x - Window.left
            self._offset_y = touch.y - Window.top

    def do_drag(self, instance, touch):
        if touch.button == 'left' and touch.x > self._offset_x:
            Window.left = touch.x - self._offset_x
            Window.top = touch.y - self._offset_y

if __name__ == '__main__':
    SearchApp().run()