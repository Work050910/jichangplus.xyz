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
  var isIndexLoading = false;
  var selectedIndex = -1;

  if (searchInput && searchDropdown) {
    function loadSearchIndex(callback) {
      if (searchIndex) {
        if (callback) callback();
        return;
      }
      if (isIndexLoading) return;
      isIndexLoading = true;
      fetch("/search-index.json")
        .then(function(res) {
          if (!res.ok) throw new Error("HTTP " + res.status);
          return res.json();
        })
        .then(function(data) {
          searchIndex = data;
          isIndexLoading = false;
          if (callback) callback();
          if (searchInput.value.trim()) {
            doSearch();
          }
        })
        .catch(function(err) {
          isIndexLoading = false;
          console.error("Search index failed:", err);
        });
    }

    // Preload index in background so search is instantaneous
    if (window.requestIdleCallback) {
      window.requestIdleCallback(function() { loadSearchIndex(); });
    } else {
      setTimeout(function() { loadSearchIndex(); }, 800);
    }

    function doSearch() {
      var rawQuery = searchInput.value.trim();
      if (!rawQuery) {
        searchDropdown.innerHTML = "";
        searchDropdown.classList.remove("active");
        selectedIndex = -1;
        return;
      }

      if (!searchIndex) {
        searchDropdown.innerHTML = "<div class='search-result-item' style='color:#64748b;'>正在加载搜索索引...</div>";
        searchDropdown.classList.add("active");
        loadSearchIndex();
        return;
      }

      var terms = rawQuery.toLowerCase().split(/\s+/).filter(Boolean);
      var matches = searchIndex.filter(function(item) {
        var text = ((item.title || "") + " " + (item.desc || "") + " " + (item.keywords || "")).toLowerCase();
        return terms.every(function(t) { return text.indexOf(t) !== -1; });
      }).slice(0, 8);

      selectedIndex = -1;
      if (matches.length === 0) {
        searchDropdown.innerHTML = "<div class='search-result-item' style='color:#64748b;'>未找到包含 “" + rawQuery + "” 的相关文章</div>";
        searchDropdown.classList.add("active");
      } else {
        var html = matches.map(function(item, idx) {
          return "<a href='" + item.url + "' class='search-result-item' data-index='" + idx + "'>" +
                 "<div class='search-result-title'>" + item.title + "</div>" +
                 "<div class='search-result-desc'>" + (item.desc || "").substring(0, 48) + "...</div>" +
                 "</a>";
        }).join("");
        searchDropdown.innerHTML = html;
        searchDropdown.classList.add("active");
      }
    }

    searchInput.addEventListener("focus", function() {
      loadSearchIndex();
      if (searchInput.value.trim()) {
        doSearch();
      }
    });

    searchInput.addEventListener("input", doSearch);

    // Keyboard navigation (ArrowDown, ArrowUp, Enter, Escape)
    searchInput.addEventListener("keydown", function(e) {
      var items = searchDropdown.querySelectorAll("a.search-result-item");
      if (!items.length) {
        if (e.key === "Escape") {
          searchDropdown.classList.remove("active");
        }
        return;
      }

      if (e.key === "ArrowDown") {
        e.preventDefault();
        selectedIndex++;
        if (selectedIndex >= items.length) selectedIndex = 0;
        updateSelection(items);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        selectedIndex--;
        if (selectedIndex < 0) selectedIndex = items.length - 1;
        updateSelection(items);
      } else if (e.key === "Enter") {
        if (selectedIndex >= 0 && selectedIndex < items.length) {
          e.preventDefault();
          items[selectedIndex].click();
        } else if (items.length > 0) {
          e.preventDefault();
          items[0].click();
        }
      } else if (e.key === "Escape") {
        searchDropdown.classList.remove("active");
        selectedIndex = -1;
      }
    });

    function updateSelection(items) {
      items.forEach(function(el, idx) {
        if (idx === selectedIndex) {
          el.classList.add("selected");
          el.scrollIntoView({ block: "nearest" });
        } else {
          el.classList.remove("selected");
        }
      });
    }

    // Close on outside click
    document.addEventListener("click", function(e) {
      if (!searchInput.contains(e.target) && !searchDropdown.contains(e.target)) {
        searchDropdown.classList.remove("active");
        selectedIndex = -1;
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

  // =========================================================================
  // Article Table of Contents (TOC) & Scrollspy with Intersection Observer
  // Requirements:
  // 1. Auto-generate IDs for H2 & H3 headings
  // 2. Generate/sync hierarchical sidebar TOC with smooth scrolling
  // 3. Scrollspy via Intersection Observer: highlight TOC & silent URL hash replaceState
  // 4. Initial positioning when loading page with URL #hash
  // =========================================================================
  var articleBody = document.querySelector(".article-body") || document.querySelector(".article-content-main") || document.querySelector("main");
  var sidebarNavList = document.querySelector(".sidebar-nav-list");
  var sidebarStickyBox = document.querySelector(".sidebar-sticky-box") || document.querySelector(".sidebar-toc-nav");

  if (articleBody) {
    // 1. Auto-generate IDs for all H2 and H3 elements
    var headings = articleBody.querySelectorAll("h2, h3");
    var usedIds = {};
    headings.forEach(function(h, idx) {
      if (!h.id || h.id.trim() === "") {
        var rawText = h.textContent.trim().toLowerCase();
        var cleanSlug = rawText
          .replace(/[^\w\u4e00-\u9fa5]+/g, "-")
          .replace(/^-+|-+$/g, "");
        var genId = cleanSlug ? ("h-" + cleanSlug) : ("section-" + (idx + 1));
        if (usedIds[genId]) {
          usedIds[genId]++;
          genId = genId + "-" + usedIds[genId];
        } else {
          usedIds[genId] = 1;
        }
        h.id = genId;
      } else {
        usedIds[h.id] = (usedIds[h.id] || 0) + 1;
      }
    });

    // 2. Generate TOC if sidebar container exists but nav list is missing or empty
    if (sidebarStickyBox && (!sidebarNavList || sidebarNavList.children.length === 0)) {
      if (!sidebarNavList) {
        var navContainer = document.querySelector(".sidebar-toc-nav");
        if (!navContainer) {
          navContainer = document.createElement("nav");
          navContainer.className = "sidebar-toc-nav";
          sidebarStickyBox.appendChild(navContainer);
        }
        sidebarNavList = document.createElement("ul");
        sidebarNavList.className = "sidebar-nav-list";
        navContainer.appendChild(sidebarNavList);
      }

      headings.forEach(function(h) {
        var li = document.createElement("li");
        var isH2 = h.tagName.toLowerCase() === "h2";
        li.className = "sidebar-nav-item " + (isH2 ? "toc-level-2" : "toc-level-3");

        var a = document.createElement("a");
        a.href = "#" + h.id;
        a.className = "sidebar-nav-link";
        a.setAttribute("data-target", h.id);
        a.title = h.textContent.trim();
        a.textContent = h.textContent.trim();

        li.appendChild(a);
        sidebarNavList.appendChild(li);
      });
    }

    // Targets to observe: all H2/H3 headings plus any explicit targets referenced by sidebar links (like #airport-card-xx)
    var targetElements = [];
    var targetIdMap = {};

    headings.forEach(function(h) {
      if (h.id && !targetIdMap[h.id]) {
        targetElements.push(h);
        targetIdMap[h.id] = h;
      }
    });

    document.querySelectorAll(".sidebar-nav-link").forEach(function(link) {
      var href = link.getAttribute("href");
      if (href && href.startsWith("#") && href.length > 1) {
        var tid = href.substring(1);
        if (!targetIdMap[tid]) {
          var el = document.getElementById(tid);
          if (el) {
            targetElements.push(el);
            targetIdMap[tid] = el;
          }
        }
      }
    });

    if (targetElements.length > 0) {
      var isClickScrolling = false;
      var clickScrollTimer = null;
      var activeId = null;

      // Function to highlight TOC link and silently update address bar hash
      function setActiveHeading(id, updateHash) {
        if (!id || activeId === id) return;
        activeId = id;

        var allLinks = document.querySelectorAll(".sidebar-nav-link");
        var activeLink = null;

        allLinks.forEach(function(link) {
          var href = link.getAttribute("href");
          var dataTarget = link.getAttribute("data-target");
          if (href === "#" + id || dataTarget === id) {
            link.classList.add("active");
            activeLink = link;
          } else {
            link.classList.remove("active");
          }
        });

        // Ensure active item stays visible in scrollable sidebar
        if (activeLink && sidebarStickyBox) {
          activeLink.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }

        // Silent hash update with history.replaceState (no page refresh, no new history stack entries)
        if (updateHash !== false && !isClickScrolling) {
          if (window.location.hash !== "#" + id) {
            if (window.history && window.history.replaceState) {
              window.history.replaceState(null, null, "#" + id);
            }
          }
        }
      }

      // Smooth scroll on TOC link click
      document.querySelectorAll(".sidebar-nav-link, .sidebar-toc-nav a").forEach(function(link) {
        link.addEventListener("click", function(e) {
          var href = link.getAttribute("href");
          if (href && href.startsWith("#") && href.length > 1) {
            var targetId = href.substring(1);
            var targetEl = document.getElementById(targetId);
            if (targetEl) {
              e.preventDefault();
              isClickScrolling = true;
              clearTimeout(clickScrollTimer);

              // Immediately activate clicked link
              setActiveHeading(targetId, true);

              // Smoothly scroll to target
              targetEl.scrollIntoView({ behavior: "smooth", block: "start" });

              clickScrollTimer = setTimeout(function() {
                isClickScrolling = false;
              }, 800);
            }
          }
        });
      });

      // 3. Scrollspy using Intersection Observer API
      if ("IntersectionObserver" in window) {
        var visibleTargets = new Set();

        var observer = new IntersectionObserver(function(entries) {
          if (isClickScrolling) return;

          entries.forEach(function(entry) {
            if (entry.isIntersecting) {
              visibleTargets.add(entry.target);
            } else {
              visibleTargets.delete(entry.target);
            }
          });

          if (visibleTargets.size > 0) {
            // Pick the target nearest to the top of viewport
            var sorted = Array.from(visibleTargets).sort(function(a, b) {
              return a.getBoundingClientRect().top - b.getBoundingClientRect().top;
            });
            setActiveHeading(sorted[0].id, true);
          } else {
            // Fallback: pick the last heading that has scrolled past the top threshold
            var scrollPos = (window.pageYOffset || document.documentElement.scrollTop) + 100;
            var current = null;
            for (var i = 0; i < targetElements.length; i++) {
              var t = targetElements[i];
              var rectTop = t.getBoundingClientRect().top + (window.pageYOffset || document.documentElement.scrollTop);
              if (rectTop <= scrollPos) {
                current = t;
              } else {
                break;
              }
            }
            if (current) {
              setActiveHeading(current.id, true);
            }
          }
        }, {
          rootMargin: "-80px 0px -65% 0px",
          threshold: 0
        });

        targetElements.forEach(function(el) {
          observer.observe(el);
        });
      }

      // 4. Initial positioning when page loads with a URL hash
      if (window.location.hash) {
        var initId = decodeURIComponent(window.location.hash.substring(1));
        var initEl = document.getElementById(initId);
        if (initEl) {
          setTimeout(function() {
            initEl.scrollIntoView({ behavior: "smooth", block: "start" });
            setActiveHeading(initId, false);
          }, 200);
        }
      }
    }
  }
});

