import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

from models.category import Category
from models.order import Order, OrderProduct
from models.product import Product
from ui.MainWindow import Ui_MainWindow
from widgets.CategoryDialog import CategoryDialog
from widgets.ChoicePile import ChoicePile
from widgets.ProductDialog import ProductDialog


def init_db():
    # Инициализация БД
    for table in [Category, Product, Order, OrderProduct]:
        table._create_table()
    pass


class MyWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        init_db()
        self.show()
        self.setup_categories()
        self.exitMenu.triggered.connect(self.close)
        self.addCategoryMenu.triggered.connect(self.open_category_dialog)
        self.addProductMenu.triggered.connect(self.open_product_dialog)
        self.toCategoriesButton.clicked.connect(self.setup_categories)

    def open_category_dialog(self):
        dlg = CategoryDialog(self)
        dlg.setWindowTitle('Добавить новую категорию')
        dlg.accepted.connect(self.setup_categories)
        dlg.exec()

    def open_product_dialog(self):
        dlg = ProductDialog(self)
        dlg.setWindowTitle('Добавить блюдо')
        dlg.accepted.connect(self.setup_categories)
        dlg.exec()

    def setup_categories(self):
        piles = self.pilesGrid
        for i in reversed(range(piles.count())):
            piles.itemAt(i).widget().setParent(None)
        categories = Category.fetch_all()
        for i, category in {i: categories[i] for i in range(len(categories))}.items():
            row = i // 3
            col = i % 3
            pile = ChoicePile(category.label, category.image, category)
            piles.addWidget(pile, row, col)
            pile.show()
            pile.clicked.connect(self.setup_products)
        self.toCategoriesButton.setEnabled(False)

    def setup_products(self):
        piles = self.pilesGrid
        for i in reversed(range(piles.count())):
            piles.itemAt(i).widget().setParent(None)
        for widget in piles.children():
            piles.removeWidget(widget)
        products = Product.fetch_all()
        for i, product in {i: products[i] for i in range(len(products)) if
                           products[i].category.id == self.sender().obj.id}.items():
            row = i // 3
            col = i % 3
            pile = ChoicePile(product.name, product.image, product)
            piles.addWidget(pile, row, col)
            pile.show()
        self.toCategoriesButton.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = MyWindow()
    sys.exit(app.exec_())
