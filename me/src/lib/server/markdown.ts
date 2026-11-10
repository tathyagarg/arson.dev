import { Marked } from "marked";
import hljs from "highlight.js";

const marked = new Marked();

marked.use({
  renderer: {
    code({ text, lang }) {
      const language = lang?.split(/\s+/)[0];

      console.log("Language:", language);
      console.log("LLVM recognized:", hljs.getLanguage(language ?? ""));

      const highlighted = language && hljs.getLanguage(language)
        ? hljs.highlight(text, { language }).value
        : hljs.highlightAuto(text).value;

      console.log("Highlighted output:", highlighted.slice(0, 500));

      return `<pre><code class="hljs language-${language ?? "plaintext"}">${highlighted}</code></pre>`;
    }
  },
});

export function parseMarkdown(content: string) {
  return marked.parse(content);
}
