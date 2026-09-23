// JichangPlus 机场加 Client Utilities
document.addEventListener("DOMContentLoaded", function() {
  // Mobile Nav Drawer Toggle
  var menuToggle = document.querySelector(".menu-toggle");
  var mainNav = document.querySelector(".main-nav");
  if (menuToggle && mainNav) {
    menuToggle.addEventListener("click", function() {
      var isExpanded = menuToggle.getAttribute("aria-expanded") === "true";
      menuToggle.setAttribute("aria-expanded", !isExpanded);
      mainNav.classList.toggle("is-open");
    });
  }

  // Coupon Copy Helper
  var copyButtons = document.querySelectorAll(".coupon-copy-btn");
  copyButtons.forEach(function(btn) {
    btn.addEventListener("click", function() {
      var coupon = btn.getAttribute("data-coupon");
      if (coupon && coupon !== "暂无优惠码") {
        if (navigator.clipboard) {
          navigator.clipboard.writeText(coupon).then(function() {
            var orig = btn.textContent;
            btn.textContent = "已复制!";
            setTimeout(function() { btn.textContent = orig; }, 2000);
          });
        }
      }
    });
  });

  // Track event stubs
  document.querySelectorAll("a[rel*="sponsored"]").forEach(function(el) {
    el.addEventListener("click", function() {
      if (window._paq) {
        window._paq.push(["trackEvent", "Affiliate", "Click", el.getAttribute("href")]);
      }
    });
  });
});
