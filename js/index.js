var swiper = new Swiper('.swiper', {
  autoplay: {
    delay: 1000,
  },
  effect: 'fade',
});

const house = document.getElementById('listing')
house.addEventListener('click',()=>{
  window.location.href='html/more.html'
})