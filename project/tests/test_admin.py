from unittest.mock import Mock
from flask import url_for
from project.admin.utils import EntryList
from project.admin.views import (
    SECTIONS, mainpage, vacancy_detail,
    user_list, user_detail,
)
from project.tests.utils import ProjectTestCase
from project.models import Vacancy
from werkzeug.exceptions import NotFound, Forbidden



expected_sections = dict([
    ('Пользователи', '/admin/users/'),
    ('Вакансии', '/admin/vacancies/'),
    ('Категории', '/admin/categories/'),
    ('Города', '/admin/cities/'),
    ('Блоки страниц', '/admin/blocks/'),
    ('Страницы', '/admin/pages/'),
    ('Элементы страниц', '/admin/pagechunks/'),
    ('Шаблоны писем', '/admin/mail_templates/'),
    ('Галерея', '/admin/gallery_images/'),
])


class EntryListTests(ProjectTestCase):

    render_templates = False
    template = "404.html"  # who cares what template we use?
    model = Mock()

    def setUp(self):
        self.view = EntryList.as_view(
            name="whatever",
            model=self.model,
            template=self.template,
        )
        self.view()

    def test_view_uses_correct_template(self):
        self.assert_template_used(self.template)

    def test_view_uses_all_model_objects(self):
        self.model.query.all.assert_called_once_with()


class EntryDetailTest(ProjectTestCase):
    pass


class MainPageTest(ProjectTestCase):
    render_templates = False

    def setUp(self):
        self.view = mainpage
        self.view()
        # self.response = self.client.get("/admin/")

    def test_view_uses_correct_template(self):
        self.assertTemplateUsed("admin/main.html")

    def test_view_generates_correct_context(self):
        self.assert_context("sections", expected_sections.items())


class SectionsTest(ProjectTestCase):
    def test_all_endpoints_can_be_resolved(self):
        for name in expected_sections:
            self.assertEqual(
                expected_sections[name],
                url_for("admin." + SECTIONS[name])
            )

class VacancyAdminDeletionTest(ProjectTestCase):
    def test_deleted_raises_404(self):
        pk = Vacancy.query.filter(Vacancy.condition_is_deleted).first().id
        self.assertRaises(NotFound, vacancy_detail, pk)

class PermissionsTest(ProjectTestCase):
    def test_userlist_returns_403(self):
        self.log_in('dipperpines')
        resp = self.client.get(url_for('admin.user_list'))
        self.assert403(resp)

    def test_userlist_returns_200_superuser(self):
        self.log_in('cthulhu')
        resp = self.client.get(url_for('admin.user_list'))
        self.assert200(resp)

    def test_userdetail_returns_403(self):
        self.log_in('dipperpines')
        resp = self.client.get(url_for('admin.user_detail') + '1/')
        self.assert403(resp)

    def test_userdetail_returns_200_superuser(self):
        self.log_in('cthulhu')
        resp = self.client.get(url_for('admin.user_detail') + '1/')
        self.assert200(resp)

    def test_correct_sections_staff(self):
        expected = expected_sections.copy()
        del expected['Пользователи']
        self.log_in('dipperpines')
        self.client.get(url_for('admin.mainpage'))
        self.assert_context("sections", expected.items())

    def test_correct_sections_superuser(self):
        self.log_in('cthulhu')
        self.client.get(url_for('admin.mainpage'))
        self.assert_context("sections", expected_sections.items())

