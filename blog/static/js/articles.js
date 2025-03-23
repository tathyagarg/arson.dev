function getArticles() {
  fetch('/api/recent')
    .then(response => response.json())
    .then(articles => {
      const articlesList = document.getElementById('articles');
      articles.forEach(article => {
        const div = document.createElement('div');
        const unformatted_date = new Date(article.created_at);
        const options = { year: 'numeric', month: 'long', day: 'numeric' };
        const date = unformatted_date.toLocaleDateString('en-US', options);

        div.innerHTML = `
          <h2>${article.title}</h2>
          <p>${date}</p>
        `;

        articlesList.appendChild(div);
      });
    });
}

getArticles();
