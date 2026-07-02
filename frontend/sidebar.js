(function () {
  var activePage = document.body.getAttribute("data-page") || "Home";

  var style = document.createElement("style");
  style.textContent =
    "#sidebar-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.6);z-index:65;backdrop-filter:blur(4px)}#sidebar-overlay.active{display:block}@media(max-width:767px){#main-sidebar{position:fixed!important;left:0!important;top:0!important;height:100vh!important;z-index:70!important;transform:translateX(-100%);transition:transform .3s cubic-bezier(.4,0,.2,1);display:flex!important}#main-sidebar.active{transform:translateX(0)}#hamburger-btn{display:flex!important}}@media(min-width:768px){#hamburger-btn{display:none!important}#sidebar-overlay{display:none!important}}";
  document.head.appendChild(style);

  var hamburger = document.createElement("button");
  hamburger.id = "hamburger-btn";
  hamburger.className =
    "fixed top-4 left-3 z-[75] w-10 h-10 items-center justify-center bg-surface-container-high/80 backdrop-blur-md rounded-xl border border-outline-variant text-on-surface hover:bg-surface-container-highest transition-all hidden";
  hamburger.innerHTML =
    '<span class="material-symbols-outlined text-[24px]">menu</span>';

  var overlay = document.createElement("div");
  overlay.id = "sidebar-overlay";

  var sidebar = document.createElement("aside");
  sidebar.id = "main-sidebar";
  sidebar.className =
    "fixed left-0 top-0 h-full w-[240px] bg-surface-container-lowest flex-col border-r border-outline-variant z-[60] hidden md:flex";

  var navItems = [
    { page: "Home", icon: "home", label: "Home" },
    { page: "Explore", icon: "explore", label: "Explore" },
    { page: "Listening History", icon: "history", label: "History" },
    { page: "Catalog", icon: "library_music", label: "Catalog" },
    { page: "Graph View", icon: "hub", label: "Graph View" },
  ];

  var isActive = function (page) {
    return page === activePage;
  };

  var itemClass = function (page) {
    return isActive(page)
      ? "text-on-surface font-bold border-l-4 border-primary pl-4 py-3 flex items-center gap-md transition-all scale-[0.98] cursor-pointer"
      : "text-on-surface-variant font-medium pl-base py-3 flex items-center gap-md transition-colors hover:bg-surface-container-high hover:text-on-surface group cursor-pointer";
  };

  var iconClass = function (page) {
    return isActive(page)
      ? "material-symbols-outlined text-primary"
      : "material-symbols-outlined group-hover:text-primary transition-colors";
  };

  var iconFill = function (page) {
    return isActive(page) ? "font-variation-settings: 'FILL' 1" : "";
  };

  var navHtml = "";
  for (var i = 0; i < navItems.length; i++) {
    var item = navItems[i];
    navHtml +=
      '<a data-nav="' +
      item.page +
      '" onclick="navigateTo(\'' +
      item.page +
      '\')" class="' +
      itemClass(item.page) +
      '">';
    navHtml +=
      '<span class="' +
      iconClass(item.page) +
      '" data-icon="' +
      item.icon +
      '" style="' +
      iconFill(item.page) +
      '">' +
      item.icon +
      "</span>";
    navHtml +=
      '<span class="font-label-md text-label-md">' +
      item.label +
      "</span>";
    navHtml += "</a>";
  }

  sidebar.innerHTML =
    '<div class="p-lg">' +
    '<h1 class="font-bold text-[22px] leading-tight text-primary tracking-tight">Music<br>Recommendation</h1>' +
    '<p class="font-body-sm text-body-sm text-on-surface-variant mt-1">Premium Curator</p>' +
    "</div>" +
    '<nav class="flex-1 px-sm mt-md space-y-xs">' +
    navHtml +
    "</nav>" +
    '<div class="p-lg border-t border-outline-variant pt-lg">' +
    '<a onclick="logout()" class="flex items-center gap-md px-sm py-3 text-on-surface-variant hover:text-on-surface hover:bg-surface-container-high rounded-lg transition-all cursor-pointer mb-md">' +
    '<span class="material-symbols-outlined">logout</span>' +
    '<span class="font-label-md text-label-md">Logout</span>' +
    '</a>' +
    '<button class="w-full py-sm bg-primary-container text-on-primary-container font-bold rounded-full transition-transform active:scale-95">Upgrade to Pro</button>' +
    "</div>";

  document.body.insertBefore(sidebar, document.body.firstChild);
  document.body.insertBefore(overlay, document.body.firstChild);
  document.body.insertBefore(hamburger, document.body.firstChild);

  var hb = document.getElementById("hamburger-btn");
  var sb = document.getElementById("main-sidebar");
  var ov = document.getElementById("sidebar-overlay");
  if (hb && sb && ov) {
    hb.addEventListener("click", function (e) {
      e.stopPropagation();
      sb.classList.toggle("active");
      ov.classList.toggle("active");
      var icon = hb.querySelector(".material-symbols-outlined");
      icon.textContent = sb.classList.contains("active") ? "close" : "menu";
    });
    ov.addEventListener("click", function () {
      sb.classList.remove("active");
      ov.classList.remove("active");
      var icon = hb.querySelector(".material-symbols-outlined");
      if (icon) icon.textContent = "menu";
    });
    sb.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        sb.classList.remove("active");
        ov.classList.remove("active");
        var icon = hb.querySelector(".material-symbols-outlined");
        if (icon) icon.textContent = "menu";
      });
    });
  }

  function getUserId() {
    try {
      var hash = window.parent.location.hash;
      var match = hash.match(/user_id=([^&]+)/);
      if (match) return decodeURIComponent(match[1]);
    } catch (e) {}
    try {
      var params = new URLSearchParams(window.location.search);
      return params.get("user_id") || "";
    } catch (e) {}
    return "";
  }

  window.navigateTo = function (page) {
    var uid = getUserId();
    try {
      parent.navigate(page, uid ? { user_id: uid } : {});
    } catch (e) {
      var hash = "#" + encodeURIComponent(page);
      if (uid) hash += "&user_id=" + encodeURIComponent(uid);
      window.location.hash = hash;
    }
  };

  window.logout = function () {
    try {
      window.parent.location.hash = "#Login";
    } catch (e) {
      window.location.hash = "#Login";
    }
  };
})();
