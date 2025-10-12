import datetime
from django.urls import reverse
from django.test import TestCase, Client
from django.contrib.auth.models import User
from users_details.models import ProfileDetails


# Create your tests here.

class UserDetailsTestCase(TestCase):
    """Db tests"""
    def setUp(self):
        self.user = User.objects.create_user(id=1, username="testusername", email="testemail@gmail.com", password="Testing321")
        self.test_user_two = User.objects.create_user(id=2, username="testusername2", email="testemail2@gmail.com", password="Testing321")
        self.client = Client()


    def test_user_objects(self):
        # get_username = User.objects.get(username="testusername")
        self.assertEqual(self.user.username, "testusername")
        print(self.user.password)

    def test_profile_signals_created(self):
        # get_profile = User.objects.get(username="testusername")
        self.assertEqual(self.user.profiledetails.full_name, "enter_your_full_name")
        self.assertEqual(self.user.profiledetails.birthday, datetime.date.today())

    def test_register_get_route(self):
        response = self.client.get(reverse("register_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, b"Register Now</h2>")

    def test_register_post_route(self):
        response = self.client.post(reverse("register_page"), {"username": "Testuser",
                                                               "email": "testuser@gmail.com",
                                                               "password1": "Testing321",
                                                               "password2": "Testing321",

                                                               }, follow=True
                                    )
        # self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("login_page"))
        self.assertContains(response, b"Login</h2>")

    def test_login_get_route(self):
        response = self.client.get(reverse("login_page"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, b"Login</h2>")

    def test_login_logout_post(self):
        response = self.client.post(reverse("login_page"), {"email": "testusername",
                                                            "password": "Testing321"}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("home_page"))
        self.assertContains(response, b"Latest Posts</h1>")
        # python manage.py test users_details.tests.UserDetailsTestCase.test_login_post

        response2 = self.client.get(reverse("logout_page"), follow=True)
        self.assertContains(response2, b"Login</h2>")


    def test_profile_page(self):
        self.client.login(username=self.user.username, password="Testing321")
        response = self.client.get(reverse("profile_page",kwargs={"user_id": self.user.id}))
        self.assertContains(response, f"<h4>{self.user.username}</h4>")
        self.assertContains(response, f">{self.user.email}</p>")
        self.assertContains(response, f'> Name: "{self.user.profiledetails.full_name}"</p>')

        # this process was too long, simply cos i used default birthday for new acct as a datetime object
        # this means i now need to get current day date with datetime, and format it to byte, each time i
        # want to check it's displaying properly. should've just used a simple textfield honestly.
        # this shit took my time, plus un-necessary long code
        # current = datetime.date.today()
        # current_edit = current.strftime("%b. %d, %Y")
        # format_today_date = current.strftime("%b. %d, %Y").split("7")
        # format_today_date2 = format_today_date[0].replace("0", "7")
        # format_today_date3 = f"{format_today_date2}{format_today_date[1]}"
        # format_today_date4_to_byte = format_today_date3.encode("utf-8")
        # self.assertIn(format_today_date4_to_byte, response.content)

    def test_unauth_view_of_profile_page(self):
        response = self.client.get(reverse("profile_page", kwargs={"user_id": 1}), follow=True)
        self.assertContains(response, f"Login</h2>")
        print(response.status_code)


    def test_edit_profile_page(self):
        self.client.login(username=self.user.username, password="Testing321")
        response = self.client.get( reverse("edit_profile_page", kwargs={"user_id":self.user.id}) )
        self.assertContains(response, f">Update Details</h2>")


        response2 = self.client.post( reverse("edit_profile_page", kwargs= {"user_id": self.user.id}),
                                      data={
            "full_name": "test name changed",
            "birthday": "october 5, 2025",
            "username": "testusernamechanged",
            "email": "testemailchanged@gmail.com",
        }, follow=True)
        self.assertContains(response2, f"<h4>testusernamechanged</h4>")
        self.assertContains(response2, f">testemailchanged@gmail.com</p>")
        self.assertIn(b"Oct. 5, 2025", response2.content)
        # self.assertIn(b"5", response2.content)
        # self.assertIn(b"Oct.", response2.content)
        self.assertContains(response2, f'> Name: "test name changed"</p>')
        self.assertContains(response2, b">Edit Profile</a>")

    def test_unauth_user_edit_of_profile(self):
        response = self.client.get(reverse("edit_profile_page", kwargs={"user_id":1}), follow=True)
        self.assertNotEqual(200, response.status_code)

        self.assertContains(response, "<h1>YOU DO NOT HAVE PERMISSION<", status_code=404)


    def test_auth_user_trying_to_edit_a_profile_not_his(self):
        self.client.login(username=self.test_user_two.username, password="Testing321")
        response = self.client.get(reverse("edit_profile_page", kwargs={"user_id":1}), follow=True)

        self.assertContains(response, "<h1>YOU DO NOT HAVE PERMISSION<", status_code=404)


