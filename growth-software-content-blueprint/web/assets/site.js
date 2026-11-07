// Mobile nav toggle (hamburger). The only script on the site: no tracking, no ads.
document.addEventListener('click', function (e) {
  var t = e.target.closest('.nav-toggle');
  var header = document.querySelector('.site-header');
  if (t && header) {
    var open = header.classList.toggle('open');
    t.setAttribute('aria-expanded', open ? 'true' : 'false');
    return;
  }
  if (header && header.classList.contains('open') && e.target.closest('.nav-menu a')) header.classList.remove('open');
});
