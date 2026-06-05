const body = document.querySelector('body');

const hamburger = document.querySelector('.hamburger-menu');
const modalNav = document.querySelector('.modal-nav-overlay');

const langBtn = document.querySelector('.header-menu li:last-child')
const modalLang = document.querySelector('.modal-lang-overlay');

// TODO: Remove debug logs; add null checks before addEventListener
console.log(langBtn);
console.log(modalLang);

hamburger.addEventListener('click', () => {
  modalNav.classList.toggle('is-open');

  if (modalNav.classList.contains('is-open')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

langBtn.addEventListener('click', () => {
  modalLang.classList.toggle('is-open');
  langBtn.classList.toggle('is-open');

  if (modalLang.classList.contains('is-open')) {
    document.body.style.overflow = 'hidden';
  } else {
    document.body.style.overflow = '';
  }
});

