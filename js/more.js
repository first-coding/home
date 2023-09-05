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


// 显示弹窗
const showBtn = document.getElementById('start-transfer');
const popup = document.querySelector('.popup');

showBtn.addEventListener('click', () => {
  popup.style.display = 'block';
});

// 关闭弹窗
const confirmBtn = document.getElementById('confirm');

confirmBtn.addEventListener('click', () => {
  popup.style.display = 'none'; 
})