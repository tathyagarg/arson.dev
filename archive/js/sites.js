// hi
async function getSites() {
  const sites_resp = await fetch("/api/sites");
  const data = await sites_resp.json();

  const sites = data.sites;
  const sitesList = document.getElementById("site-list");
  sitesList.innerHTML = "";
  sites.forEach(async (site) => {
    const link = document.createElement("a");
    link.href = `/sites/${site.name}`;
    link.style = "display: block";
    link.target = "_blank";

    const div = document.createElement("div");
    const icon_resp = await fetch(`/sites/${site.name}/favicon.ico`);
    const icon = await icon_resp.blob();

    const image = document.createElement("img");
    image.src = URL.createObjectURL(icon);
    image.className = "site-icon";

    const name = document.createElement("h3");
    name.innerText = site.title;
    name.className = "site-name";

    const description = document.createElement("p");
    description.innerText = site.description;
    description.className = "site-description";

    const tags = document.createElement("div");
    tags.className = "site-tags";

    const domain = document.createElement("div");
    domain.className = "site-domain tag";
    domain.innerText = `Domain: ${site.domain}`;

    const source = document.createElement("div");
    source.className = "site-source tag";
    source.innerHTML = `<a href=${site.source}>Source</a>`

    tags.appendChild(domain);
    tags.appendChild(source);

    div.appendChild(image);
    div.appendChild(tags);
    div.appendChild(name);
    div.appendChild(description);

    link.appendChild(div);
    link.className = "site";
    sitesList.appendChild(link);
  });
}

getSites().then(()=>{});
