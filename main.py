from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineIconListItem, IconLeftWidget
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawer
from kivymd.uix.toolbar import MDTopAppBar


KV = """
<ContentNavigationDrawer>:
    MDBoxLayout:
        orientation: "vertical"
        padding: "8dp"
        spacing: "8dp"

        ScrollView:
            MDList:
                id: menu_list
"""

class ContentNavigationDrawer(MDBoxLayout):
    pass

class OrganizaUffApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.screen = MDScreen()

        self.top_bar = MDTopAppBar(
            title="OrganizaUff",
            left_action_items=[["menu", lambda x: self.nav_drawer.set_state("toggle")]],
            pos_hint={"top": 1}
        )
        self.screen.add_widget(self.top_bar)

        self.nav_drawer = MDNavigationDrawer()
        self.content_drawer = ContentNavigationDrawer()
        self.nav_drawer.add_widget(self.content_drawer)
        self.screen.add_widget(self.nav_drawer)

        self.conteudo = MDScreen()
        self.screen.add_widget(self.conteudo)

        icon = IconLeftWidget(icon="calendar")
        item = OneLineIconListItem(
            text="1º Período",
            on_press=lambda x: self.mostrar_periodo1()
        )
        item.add_widget(icon)
        self.content_drawer.ids.menu_list.add_widget(item)

        return self.screen

    def mostrar_periodo1(self):
        self.conteudo.clear_widgets()
        self.conteudo.add_widget()
        self.nav_drawer.set_state("close")

if __name__ == "__main__":
    Builder.load_string(KV)
    OrganizaUffApp().run()
