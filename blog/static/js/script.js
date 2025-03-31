const variables = [
  "crust", "mantle", "base",
  "surface0", "surface1", "surface2",
  "text", "blue", "sapphire"
]

function updateTheme(theme) {
  var root = document.querySelector(":root");
  for (let variable of variables) {
    root.style.setProperty(`--${variable}`, `var(--${theme}-${variable})`);
  }
}

let theme = localStorage.getItem("theme");
if (theme == null) {
  localStorage.setItem("theme", "dark");
}
updateTheme(localStorage.getItem("theme"));

getNavbar = new Promise((resolve, reject) => {
  fetch("/static/html/navbar.html")
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      resolve(data);
    });
});

getNavbar.then((data) => {
  document.getElementById("navbar").innerHTML = data;

  let theme = localStorage.getItem("theme");
  let themeToggleParent = document.getElementById("theme-switch");
  let themeToggle = themeToggleParent.querySelector("input");

  themeToggle.checked = theme === "light";

  themeToggle.addEventListener("change", (e) => {
    localStorage.setItem("theme", e.target.checked ? "light" : "dark");
    updateTheme(localStorage.getItem("theme"));
  });
});

getFooter = new Promise((resolve, reject) => {
  fetch("/static/html/footer.html")
    .then((response) => {
      return response.text();
    })
    .then((data) => {
      resolve(data);
    });
})

getFooter.then((data) => {
  document.getElementById("footer").innerHTML = data;
});
