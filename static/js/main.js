// JichangPlus 机场加 Client Utilities & Instant Search
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

  // Client-Side Article Search
  var searchInput = document.getElementById("site-search-input");
  var searchDropdown = document.getElementById("search-results");
  var searchIndex = null;

  if (searchInput && searchDropdown) {
    // Lazy load search index
    function loadSearchIndex() {
      if (!searchIndex) {
        fetch("/search-index.json")
          .then(function(res) { return res.json(); })
          .then(function(data) { searchIndex = data; })
          .catch(function(err) { console.error("Search index failed:", err); });
      }
    }

    searchInput.addEventListener("focus", loadSearchIndex);

    searchInput.addEventListener("input", function() {
      var query = searchInput.value.trim().toLowerCase();
      if (!query || !searchIndex) {
        searchDropdown.innerHTML = "";
        searchDropdown.classList.remove("active");
        return;
      }

      var matches = searchIndex.filter(function(item) {
        return (item.title && item.title.toLowerCase().indexOf(query) !== -1) ||
               (item.desc && item.desc.toLowerCase().indexOf(query) !== -1) ||
               (item.keywords && item.keywords.toLowerCase().indexOf(query) !== -1);
      }).slice(0, 8);

      if (matches.length === 0) {
        searchDropdown.innerHTML = "<div class='search-result-item' style='color:#64748b;'>未找到匹配文章</div>";
        searchDropdown.classList.add("active");
      } else {
        var html = matches.map(function(item) {
          return "<a href='" + item.url + "' class='search-result-item'>" +
                 "<div class='search-result-title'>" + item.title + "</div>" +
                 "<div class='search-result-desc'>" + (item.desc || "").substring(0, 48) + "...</div>" +
                 "</a>";
        }).join("");
        searchDropdown.innerHTML = html;
        searchDropdown.classList.add("active");
      }
    });

    // Close on outside click or Escape
    document.addEventListener("click", function(e) {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.classList.remove("active");
      }
    });

    document.addEventListener("keydown", function(e) {
      if (e.key === "Escape") {
        searchDropdown.classList.remove("active");
      }
    });
  }

  // Affiliate Click Tracking
  document.querySelectorAll("a[rel*='sponsored']").forEach(function(el) {
    el.addEventListener("click", function() {
      if (window._paq) {
        window._paq.push(["trackEvent", "Affiliate", "Click", el.getAttribute("href")]);
      }
    });
  });
});
