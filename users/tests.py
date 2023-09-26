from .models import User
from django.test import TestCase
from django.contrib.auth.hashers import check_password, make_password

# Create your tests here.

class LogInTest(TestCase):

    def test_signup_render_successful(self):
        response = self.client.get("/users/signup/")
        self.assertEqual(response.status_code, 200)
    
    def test_signup_succesful(self):
        # datos de registro
        test_user = "test_user"
        test_pass = "password123"

        # intento de registro
        response = self.client.post("/users/signup-verification/", {
            "htmluser": test_user,
            "htmlpass": test_pass
        })

        #verificación de éxito
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=test_user).exists())

        # Verificación de datos
        user = User.objects.get(username=test_user)
        self.assertEqual(user.username, test_user)
        self.assertTrue(check_password(test_pass, user.password))

    def test_signup_duplicate_user(self):
        
        dup_user = "dup_user"
        pass1 = "pass1"
        pass2 = "pass2"
        
        #intento con un usuario no repetido
        init_response = self.client.post("/users/signup-verification/", {
            "htmluser": dup_user,
            "htmlpass": pass1
        })

        #intento con un usuario con username y contraseña repetidos
        dup_response = self.client.post("/users/signup-verification/", {
            "htmluser": dup_user,
            "htmlpass": pass1
        })

        #intento con un usuario con username repetido y contraseña diferente
        dup_response_pass_2 = self.client.post("/users/signup-verification/", {
            "htmluser": dup_user,
            "htmlpass": pass2
        })

        #verififación de éxito

        #1. permite ingresar al primer usuario
        self.assertEqual(init_response.status_code, 302)

        #2. no permite ingresar al segundo usuario
        self.assertEqual(dup_response.status_code, 400)

        #3. no permite ingresar al tercer usuario
        self.assertEqual(dup_response_pass_2.status_code, 400)

    def test_hashed_passwords(self):    
        # Datos de registro
        req_user = "test_user"
        req_pass = "test_password"
        hashed_pass = make_password(req_pass)

        # Intento de registro
        response = self.client.post("/users/signup_verification", {
                "htmluser": req_user,
                "htmlpass": hashed_pass
            })
                
        if check_password(req_pass, hashed_pass):
            print("////////////////////////////////")
            print("hash hecho cámbiate de carrera igual.")

        else:
            print("////////////////////////////////")
            print("No hash cámbiate de carrera.")

class LoginTest(TestCase):

    def test_login_render_successful(self):
        response = self.client.get("/users/login/")
        self.assertEqual(response.status_code, 200)
    
    def test_login_successful(self):
        
        # datos de registro
        req_user = "test_user"
        req_pass = "test_password"

        # intento de registro
        signup_response = self.client.post("/users/signup-verification/", {
            "htmluser": req_user,
            "htmlpass": req_pass
        })
        
        # intento de inicio de sesión
        login_response = self.client.post("/users/login-verification/", {
            "htmluser": req_user,
            "htmlpass": req_pass
        })
        
        # Verificación de éxito (verificar que las credenciales coinciden con las que se encuentran en la base de datos)
        self.assertEqual(login_response.status_code, 302)
        self.assertTrue(User.objects.filter(username=req_user).exists())

        # Verificación de datos
        user = User.objects.get(username=req_user)
        self.assertEqual(user.username, req_user)
        self.assertTrue(check_password(req_pass, user.password))

    def test_login_incorrect_credentials(self):
        # Datos de inicio de sesión
        test_user = "test_user"
        test_pass = "test_password"

        # Intento de inicio de sesión sin previo registro
        no_credentials_response = self.client.post("/users/login_verification/", {
            "htmluser": test_user,
            "htmlpass": test_pass
        })
        
        # Verificación de rechazo (verificar que las credenciales no coinciden con las que se encuentran en la base de datos)
        self.assertFalse(User.objects.filter(username=test_user).exists())

class IndexTest(TestCase):

    def test_index_render_successful(self):
        response = self.client.get("/users/home/")
        self.assertEqual(response.status_code, 200)
