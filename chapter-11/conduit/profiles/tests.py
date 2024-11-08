# Create your tests here.
from profiles.models import Profile

User = get_user_model()


@pytest.mark.django_db  # Ensures that the test database is used
def test_create_user():
    user = User.objects.create_user(username="john", password="pass123")
    assert user.username == "john"
    assert user.is_active  # Check that the user is active by default


@pytest.mark.django_db
def test_check_password():
    user = User.objects.create_user(username="john", password="pass123")
    assert (
        user.check_password("pass123") is True
    )  # Test that the password is set correctly
