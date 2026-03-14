        document.addEventListener('DOMContentLoaded', () => {
            const tabLogin = document.getElementById('tab-login');
            const tabRegister = document.getElementById('tab-register');
            const formLogin = document.getElementById('form-login');
            const formRegister = document.getElementById('form-register');

            // Функция для переключения на Вход
            tabLogin.addEventListener('click', (e) => {
                e.preventDefault();
                tabLogin.classList.add('active');
                tabRegister.classList.remove('active');
                formLogin.classList.add('active-form');
                formRegister.classList.remove('active-form');
            });

            // Функция для переключения на Регистрацию
            tabRegister.addEventListener('click', (e) => {
                e.preventDefault();
                tabRegister.classList.add('active');
                tabLogin.classList.remove('active');
                formRegister.classList.add('active-form');
                formLogin.classList.remove('active-form');
            });
        });