var root = document.querySelector(":root");

function fetchTag(tag) {
  const tagElement = document.createElement('span');
  tagElement.classList.add('tag');
  tagElement.textContent = tag.name;
  tagElement.dataset.dark = tag.dark_color;
  tagElement.dataset.light = tag.light_color;
  tagElement.style.backgroundColor = localStorage.getItem('theme') === 'dark' ? tag.dark_color : tag.light_color;

  return Promise.resolve(tagElement);
}

function getArticles() {
  fetch('/api/recent')
    .then(response => response.json())
    .then(data => {
      const articles = data.articles;
      const articlesList = document.getElementById('articles');
      articlesList.innerHTML = ''; // Clear existing content

      articles.forEach(article => {
        const link = document.createElement('a');
        link.href = `/blog/${article.slug}`;
        link.classList.add('article');

        const div = document.createElement('div');
        const unformatted_date = new Date(article.created_at);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const date = unformatted_date.toLocaleDateString('en-US', options);

        const tagHolder = document.createElement('div');

        Promise.all(article.tags.map(fetchTag)).then(tagElements => {
          tagElements.forEach(tagElement => {console.log(tagElement); tagHolder.appendChild(tagElement)});

          div.innerHTML = `
            <h2>${article.title}</h2>
            <p id="summary"><i>${article.summary}</i></p>
            <p><small>${date}</small></p>
            Tags: ${tagHolder.innerHTML}
          `;

          const image = document.createElement('img');
          image.src = article.banner_url;
          image.alt = article.title;

          link.appendChild(div);
          link.appendChild(image);
          articlesList.appendChild(link);
        });
      });
    })
    .catch(error => console.error('Error fetching articles:', error));
}

getArticles();

