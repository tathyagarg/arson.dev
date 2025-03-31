const editor = document.querySelector('#editor-code');
const languageSelect = document.querySelector('#language');

languageSelect.addEventListener('change', () => {
  const language = languageSelect.value;
  editor.setAttribute('class', `language-${language}`);

  Prism.highlightElement(editor);
})

