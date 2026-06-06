import Swiper from 'https://cdn.jsdelivr.net/npm/swiper@11/swiper.mjs';
import { Navigation } from 'https://cdn.jsdelivr.net/npm/swiper@11/modules/index.mjs';

const swiper = new Swiper('.swiper', {
    modules: [Navigation],
    navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
    },
    slidesPerView: 'auto',
    spaceBetween: '8',
});