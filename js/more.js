// 获取轮播图元素
const swiperEl = document.querySelector('.swiper');

// 初始化 Swiper
const swiper = new Swiper(swiperEl, {
  loop: true,
  autoplay: {
    delay: 1000,
    stopOnLastSlide: false,
    disableOnInteraction: false,
    autoplayDisableOnInteraction: false
  }
});

// 悬停控制自动轮播
swiperEl.addEventListener('mouseenter', () => {
  swiper.autoplay.stop();
});

swiperEl.addEventListener('mouseleave', () => {
  swiper.autoplay.start(); 
});

// 页面隐藏时暂停轮播
document.addEventListener('visibilitychange', e => {
  if (document.visibilityState === 'hidden') {
    swiper.autoplay.stop();
  } else {
    swiper.autoplay.start();
  }
});

// 获取按钮和弹窗元素
const btn = document.getElementById('start-transfer');
const popup = document.querySelector('.popup');

// 点击按钮显示弹窗
btn.addEventListener('click', () => {
  popup.style.display="block"
})


// 点击外部关闭弹窗 
document.body.addEventListener('click', (e) => {
  if(!e.target.closest('.popup')) {
    popup.style.display = 'none';
  }
})