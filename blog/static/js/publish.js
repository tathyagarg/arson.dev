function handleBlogPost() {
  const slug = document.getElementById("slug").value;
  const title = document.getElementById("title").value;
  const content = document.getElementById("content").files[0];
  const tagsElem = document.getElementById("tags").options;
  const banner_url = document.getElementById("banner_url").value;
  const authorization = document.getElementById("auth").value;

  let tags = [];

  for (var i = 0; i < tagsElem.length; i++) {
    if (tagsElem[i].selected) {
      tags.push(tagsElem[i].value);
    }
  }

  const file = new FileReader();
  file.onload = function() {
    const new_content = file.result;
    fetch("/api/publish", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        slug: slug,
        title: title,
        content: new_content,
        tags: tags,
        banner_url: banner_url,
        authorization: authorization
      })
    })
      .then(response => response.json())
      .then(data => {
        console.log("Success:", data);
        window.location.href = "/";
      })
      .catch(error => {
        console.error("Error:", error);
      });
  };
  file.readAsText(content);
}
