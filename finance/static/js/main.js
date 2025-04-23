// Анимация загрузки
document.addEventListener('DOMContentLoaded', () => {
  // Плавное появление элементов
  const fadeElems = document.querySelectorAll('.fade-in');
  fadeElems.forEach(el => {
    el.style.opacity = '0';
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s ease';
      el.style.opacity = '1';
    }, 100);
  });

  // Подсветка активного пункта меню
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active');
    }
  });
});