const body = document.querySelector('body');

const hamburger = document.querySelector('.hamburger-menu');
const modalNav = document.querySelector('.modal-nav-overlay');

const langBtn = document.querySelector('.header-menu li:last-child')
const modalLang = document.querySelector('.modal-lang-overlay');

if (hamburger && modalNav) {
  hamburger.addEventListener('click', () => {
    modalNav.classList.toggle('is-open');

    if (modalNav.classList.contains('is-open')) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  });
}

if (langBtn && modalLang) {
  langBtn.addEventListener('click', () => {
    modalLang.classList.toggle('is-open');
    langBtn.classList.toggle('is-open');

    if (modalLang.classList.contains('is-open')) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  });
}
