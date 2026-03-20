document.addEventListener('DOMContentLoaded', function() {
    // --- Код для карусели ---
    const carousel = document.getElementById('events-carousel');
    const btnLeft = document.getElementById('btn-left');
    const btnRight = document.getElementById('btn-right');

    const scrollAmount = 380;

    if (btnLeft && btnRight && carousel) {
        btnLeft.addEventListener('click', () => {
            carousel.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
        });

        btnRight.addEventListener('click', () => {
            carousel.scrollBy({ left: scrollAmount, behavior: 'smooth' });
        });
    }

    // --- Код для шапки ---
    const header = document.querySelector('.site-header');

    if (header) {
        const toggleHeader = () => {
            // Если проскроллили больше 50 пикселей вниз, добавляем класс
            if (window.scrollY > 120) {
                header.classList.add('site-header-solid');
            } else {
                // Если вернулись на самый верх, убираем класс
                header.classList.remove('site-header-solid');
            }
        };

        // Запускаем проверку при загрузке (если пользователь обновил страницу где-то посередине)
        toggleHeader();

        // Отслеживаем скролл
        window.addEventListener('scroll', toggleHeader);
    }
});