import allure
import random
import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


@allure.suite("Страница Dashboard после логина")
class DashboardPage(BasePage):

    MENU_CATALOG = (By.CSS_SELECTOR, "#menu-catalog")
    PRODUCTS_SECTION = (By.PARTIAL_LINK_TEXT, "Products")
    ADD_BUTTON = (By.CSS_SELECTOR, ".fa.fa-plus")
    TRASH_BUTTON = (By.CSS_SELECTOR, ".fa.fa-trash-o")
    TABLE_CHECKBOX = (By.CSS_SELECTOR, "table.table-bordered.table-hover [type='checkbox']")
    WARNING_MSG = (By.CSS_SELECTOR, ".alert.alert-danger.alert-dismissible")
    SAVE_BUTTON = (By.CSS_SELECTOR, ".fa.fa-save")
    INPUT_NAME = (By.CSS_SELECTOR, "#input-name1")
    DESCRIPTION_TEXT_AREA = (By.CSS_SELECTOR, ".note-editable.panel-body")
    META_TAG_TITLE_INPUT = (By.CSS_SELECTOR, "#input-meta-title1")

    # навигация к странице с продуктами
    @allure.step("Навигация на страницу продуктов")
    def nav_to_products_page(self):
        logging.info("Navigate to products page")
        self.browser.find_element(*self.MENU_CATALOG).click()
        self.wait_element(self.PRODUCTS_SECTION)
        self.browser.find_element(*self.PRODUCTS_SECTION).click()

    # выбор случайного чекбокса (кроме общего) и удаление продукта
    @allure.step("Удалить случайный продукт")
    def delete_random_product(self):
        checkboxes = len(self.browser.find_elements(*self.TABLE_CHECKBOX))
        logging.info("Click on random checkbox and deleting relative product")
        self.browser.find_elements(*self.TABLE_CHECKBOX)[random.randint(1, checkboxes-1)].click()
        self.browser.find_element(*self.TRASH_BUTTON).click()
        self.browser.switch_to.alert.accept()
        assert self.browser.find_element(*self.WARNING_MSG)
        logging.info("Product successfully deleted!")

    # добавление нового продукта
    @allure.step("Добавить новый продукт")
    def add_new_product(self):
        new_product = 'Test product'
        logging.info("Starting to add new product")
        self.browser.find_element(*self.ADD_BUTTON).click()
        self.wait_element(self.SAVE_BUTTON)
        self.clear_n_paste(self.INPUT_NAME, new_product)
        self.browser.find_element(*self.DESCRIPTION_TEXT_AREA).send_keys('Test text')
        self.browser.find_element(*self.META_TAG_TITLE_INPUT).send_keys('test-tag')
        self.browser.find_element(*self.SAVE_BUTTON).click()
        with allure.step(f"Успешно добавлен новый продукт: {new_product}"):
            self.wait_element(self.WARNING_MSG)
