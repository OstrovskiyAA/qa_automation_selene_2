import allure
from allure_commons.types import Severity
from selene import be, have
from selene.core.command import js, select_all
import os

from data.user import Users
from pages.registration_form import RegistrationPage

registration_page = RegistrationPage()
user=Users('Alexey', "Ostrovskiy", "a.a.ostrovskiy@mail.ru", "Male", "8911277596", 30, "May",
           1992, "Computer Science", "Music", "me.jpg", "Дачный проспект", "NCR", "Gurgaon")
@allure.label("owner", "Ostrovskiy Alexey")
@allure.severity(Severity.CRITICAL)
@allure.story("Checking registration")
@allure.feature("new tasks")
@allure.link("https://demoqa.com", name="Testing")

#Если без селеноида:
# def test_student_registrate(open):

# Если нужен селеноид:
def test_student_registrate(setup_browser):
    browser = setup_browser
    browser.open('https://demoqa.com/automation-practice-form')
    with allure.step("registration"):
        browser.element("[id=firstName]").should(be.blank).type(user.first_name)
        browser.element("#lastName").should(be.blank).perform(
            command=js.set_value(user.last_name)
        )
        browser.element("[id=userEmail]").should(be.blank).type(
            user.email
        )
        browser.all("[name=gender]").element_by(have.value(user.gender)).element("..").click()
        browser.all("[id^=userNumb]")[2].should(be.blank).with_(
            set_value_by_js=True
        ).set_value(user.mobile_number)
        browser.element('[id="dateOfBirthInput"]').should(be.visible).perform(
            command=select_all
        ).type(f"{user.date_by_your_own_day} {user.date_by_your_own_month} {user.date_by_your_own_year}").press_enter()
        browser.element("#subjectsInput").type(user.subject).press_enter()
        music = browser.element('[id="hobbies-checkbox-3"]').should(be.present)
        music.perform(command=js.click)
        browser.element("#uploadPicture").set_value(
            os.path.abspath(
                os.path.join(os.path.dirname(qa_automation_selene_high_level_steps.__file__), f'resources/{user.name_of_file}')
            )
        )
        browser.element('[id="currentAddress"]').should(be.blank).type(user.address)
        browser.element("#state").perform(command=js.scroll_into_view).click()
        browser.all("[id^=react-select][id*=option]").element_by(
            have.exact_text(user.state)
        ).click()
        browser.element(".css-1wa3eu0-placeholder").should(be.present).should(
            have.text("Select City")
        ).click()
        browser.all("[id^=react-select][id*=option]").element_by(
            have.exact_text(user.city)
        ).click()
    with allure.step("submit"):
        browser.element('[id = "submit"]').should(be.present).perform(command=js.click)
    with allure.step("assertion"):
        date_of_birth = f"{user.date_by_your_own_day} {user.date_by_your_own_month},{user.date_by_your_own_year}"
        browser.element(".table").all("td").even.should(
            have.exact_texts(
                f"{user.first_name} {user.last_name}",
                user.email,
                user.gender,
                user.mobile_number,
                date_of_birth,
                user.subject,
                user.hobby,
                user.name_of_file,
                user.address,
                f"{user.state} {user.city}",
            )
        )
    # registration_page.fill_first_name()
    # registration_page.fill_last_name()
    # registration_page.fill_email()
    # registration_page.select_gender()
    # registration_page.fill_mobile_number()
    # # registration_page.fill_date()
    # registration_page.fill_date_by_your_own(30, "May", 1992)
    # registration_page.fill_subject()
    # registration_page.fill_hobby()
    # registration_page.download_file()
    # registration_page.fill_address()
    # registration_page.fill_state()
    # registration_page.fill_city()
    # with allure.step("registration"):
    #     registration_page.register(user)
    # with allure.step("submit"):
    #     registration_page.submit()
    # with allure.step("assertion"):
    #     registration_page.should_be_registered(user)