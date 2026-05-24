const hamburger = document.querySelector('.hamburger-menu');
const modal = document.querySelector('.modal-overlay');


hamburger.addEventListener('click', () => {
  modal.classList.toggle('is-open');
  console.log("hamburger clicked");
});