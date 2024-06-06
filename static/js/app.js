let navbarMenuHTML = document.querySelector(".app-menu").innerHTML;
let moreMenuWidth = 150;
let scrollbarElement = "";

function windowResizeHover() {
  let windowSize = document.documentElement.clientWidth;
  // console.log("Window size: " + windowSize);

  if (windowSize >= 1025) {
    document.body.classList.remove("overflow-hidden");
    document.querySelector(".app-menu").classList.add("hidden");

    if (sessionStorage.getItem("data-layout") == "vertical") {
      document.documentElement.setAttribute("data-sidebar-size", "sm");
    }

    if (document.querySelector(".hamburger-icon")) {
      document.querySelector(".hamburger-icon").classList.add("open");
    }

    if (sessionStorage.getItem("data-layout") == "horizontal") {
      updateHorizontalMenus();
    }
  } else if (windowSize <= 1025 && windowSize >= 768) {
    document.body.classList.remove("overflow-hidden");
    document.querySelector(".app-menu").classList.add("hidden");

    if (sessionStorage.getItem("data-layout") == "vertical") {
      document.documentElement.setAttribute(
        "data-sidebar-size",
        sessionStorage.getItem("data-sidebar-size")
      );
    }

    if (sessionStorage.getItem("data-layout") == "horizontal") {
      updateHorizontalMenus();
    }

    if (document.querySelector(".hamburger-icon")) {
      document.querySelector(".hamburger-icon").classList.remove("open");
    }
  } else if (windowSize < 768) {
    if (sessionStorage.getItem("data-layout") != "horizontal") {
      document.documentElement.setAttribute("data-sidebar-size", "lg");
    }
    if (document.querySelector(".hamburger-icon")) {
      document.querySelector(".hamburger-icon").classList.add("open");
    }
  }
}

// two-column sidebar active js
function initActiveMenu() {
  var currentPath =
    location.pathname == "/" ? "" : location.pathname.substring(1);
  // navbar-nav
  var a = document
    .getElementById("navbar-nav")
    .querySelector('[href="/' + currentPath + '"]');
  if (a) {
    a.classList.add("active");
    var parentCollapseDiv = a.parentElement.parentElement.parentElement;
    if (parentCollapseDiv) {
      if (document.documentElement.getAttribute("data-layout") == "vertical")
        parentCollapseDiv.classList.remove("hidden");
      parentCollapseDiv.classList.add("active");
      parentCollapseDiv.previousElementSibling?.classList.add("active");
      parentCollapseDiv.previousElementSibling?.classList.add("show");
      if (document.documentElement.getAttribute("data-layout") == "vertical")
        parentCollapseDiv.previousElementSibling?.parentElement.parentElement.parentElement?.classList.remove(
          "hidden"
        );
      parentCollapseDiv.previousElementSibling?.parentElement.parentElement.parentElement?.previousElementSibling?.classList.add(
        "active"
      );
    }
  }

  initMenuItemScroll();
}

function isLoadBodyElement() {
  var windowSize = document.documentElement.clientWidth;
  var verticalOverlay = document.getElementById("sidebar-overlay");
  if (verticalOverlay) {
    verticalOverlay.addEventListener("click", function () {
      if (!verticalOverlay.classList.contains("hidden")) {
        if (windowSize <= 768) {
          document.querySelector(".app-menu").classList.add("hidden");
          document.body.classList.remove("overflow-hidden");
        } else {
          document.documentElement.getAttribute("data-sidebar-size") == "sm"
            ? document.documentElement.setAttribute("data-sidebar-size", "lg")
            : document.documentElement.setAttribute("data-sidebar-size", "sm");
        }
        verticalOverlay.classList.add("hidden");
      }
    });
  }
}

function windowLoadContent() {
  window.addEventListener("resize", windowResizeHover);

  document.addEventListener("scroll", function () {
    windowScroll();
  });

  window.addEventListener("load", function () {
    initActiveMenu();
    isLoadBodyElement();
  });
  if (document.getElementById("topnav-hamburger-icon")) {
    document
      .getElementById("topnav-hamburger-icon")
      .addEventListener("click", tonggleHamburgerMenu);
  }
}

function tonggleHamburgerMenu() {
  let windowSize = document.documentElement.clientWidth;
  let verticalOverlay = document.getElementById("sidebar-overlay");
  let hamburgerIcon = document.querySelector(".hamburger-icon");

  // console.log("Size: " + windowSize);
  // Toggle the open class
  hamburgerIcon.classList.toggle("open");

  // Toggle the visibility of the icons
  let chevronsLeft = hamburgerIcon.querySelector(
    '[data-lucide="chevrons-left"]'
  );
  let chevronsRight = hamburgerIcon.querySelector(
    '[data-lucide="chevrons-right"]'
  );

  chevronsLeft.classList.toggle("hidden");
  chevronsRight.classList.toggle("hidden");

  if (windowSize > 768) {
    document.querySelector(".hamburger-icon").classList.toggle("open");
  }

  //For collapse vertical menu
  if (document.documentElement.getAttribute("data-layout") === "vertical") {
    if (windowSize > 1025) {
      document.documentElement.getAttribute("data-sidebar-size") == "sm"
        ? document.documentElement.setAttribute("data-sidebar-size", "lg")
        : document.documentElement.setAttribute("data-sidebar-size", "sm");
    } else if (windowSize <= 1025 && windowSize >= 768) {
      document.documentElement.getAttribute("data-sidebar-size") ==
      sessionStorage.getItem("data-sidebar-size")
        ? document.documentElement.setAttribute(
            "data-sidebar-size",
            sessionStorage.getItem("data-sidebar-size") == "sm" ? "lg" : "sm"
          )
        : document.documentElement.setAttribute(
            "data-sidebar-size",
            sessionStorage.getItem("data-sidebar-size")
          );
    } else if (windowSize < 768) {
      // document.getElementById("sidebar-overlay").classList.remove("hidden")
      document.body.classList.add("overflow-hidden");
      if (verticalOverlay.classList.contains("hidden")) {
        verticalOverlay.classList.remove("hidden");
        document.querySelector(".app-menu").classList.remove("hidden");
      }
      document.documentElement.setAttribute("data-sidebar-size", "lg");
    }
    applyScrollbarLogic();
  } else {
    if (windowSize < 768) {
      // document.getElementById("sidebar-overlay").classList.remove("hidden")
      document.body.classList.add("overflow-hidden");
      if (verticalOverlay.classList.contains("hidden")) {
        verticalOverlay.classList.remove("hidden");
        document.querySelector(".app-menu").classList.remove("hidden");
      }
    }
  }
}

// Attach the event listener
if (document.getElementById("topnav-hamburger-icon")) {
  document.getElementById("topnav-hamburger-icon").addEventListener("click", tonggleHamburgerMenu);
}

function applyScrollbarLogic() {
  if (document.documentElement.getAttribute("data-layout") == "vertical") {
    if (document.documentElement.getAttribute("data-sidebar-size") != "sm") {
      scrollbarElement = new SimpleBar(document.getElementById("scrollbar"));
    } else {
      setTimeout(() => {
        document.querySelector(".app-menu").innerHTML = navbarMenuHTML;
      }, 500);
    }
  }
}

function initMenuItemScroll() {
  var sidebarMenu = document.getElementById("navbar-nav");
  if (sidebarMenu) {
    var currentPath =
      location.pathname == "/" ? "" : location.pathname.substring(1);
    var activeMenu = document
      .getElementById("navbar-nav")
      .querySelector('[href="/' + currentPath + '"]');
    const bodyHeight =
      window.innerHeight / 2 < 85 ? 85 : window.innerHeight / 2;
    var offsetTopRelativeToBody = 0;
    while (activeMenu) {
      offsetTopRelativeToBody += activeMenu.offsetTop;
      activeMenu = activeMenu.offsetParent;
    }

    if (offsetTopRelativeToBody > 300) {
      var verticalMenu = document.getElementsByClassName("app-menu")
        ? document.getElementsByClassName("app-menu")[0]
        : "";
      var scrollWrapper = verticalMenu.querySelector(
        ".simplebar-content-wrapper"
      );
      if (verticalMenu && scrollWrapper) {
        var scrollTop =
          offsetTopRelativeToBody == 330
            ? offsetTopRelativeToBody + 85
            : offsetTopRelativeToBody - bodyHeight;
        scrollWrapper.scrollTo({
          top: scrollTop,
          behavior: "smooth",
        });
      }
    }
  }
}

// Call the function when the page loads
applyScrollbarLogic();

function init() {
  windowLoadContent();
  initMenuItemScroll();
}

init();
//  Window scroll sticky class add
function windowScroll() {
  var navbar = document.getElementById("page-topbar");
  if (navbar) {
    if (
      document.body.scrollTop >= 50 ||
      document.documentElement.scrollTop >= 50
    ) {
      navbar.classList.add("is-sticky");
    } else {
      navbar.classList.remove("is-sticky");
    }
  }
}
console.log("Hello World");
