        document.addEventListener('DOMContentLoaded', function() {
            const carousel = document.getElementById('events-carousel');
            const btnLeft = document.getElementById('btn-left');
            const btnRight = document.getElementById('btn-right');

            // На сколько пикселей прокручивать за одно нажатие 
            // (примерно ширина одной карточки + отступ)
            const scrollAmount = 380; 

            btnLeft.addEventListener('click', () => {
                carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
            });

            btnRight.addEventListener('click', () => {
                carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
            });
            const header = document.querySelector('.header');

            window.addEventListener('scroll', () => {
                // Если мы прокрутили страницу больше чем на 150 пикселей вниз
                if (window.scrollY > 150) {
                    header.classList.add('scrolled'); // Добавляем цвет и закругления
                } else {
                    header.classList.remove('scrolled'); // Делаем снова прозрачной
                }
            });
        });