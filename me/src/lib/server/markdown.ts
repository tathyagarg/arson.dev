import { Marked } from "marked";
import hljs from "highlight.js/lib/common";

const marked = new Marked({
  highlight: undefined,
});

marked.use({
  renderer: {
    code({ text, lang }) {
      const language = lang?.split(/\s+/)[0];

      let highlighted = text;

      if (language && hljs.getLanguage(language)) {
        highlighted = hljs.highlight(text, {
          language,
        }).value;
      } else {
        highlighted = hljs.highlightAuto(text).value;
      }

      return `<pre><code class="hljs language-${language ?? "plaintext"}">${highlighted}</code></pre>`;
    },
  },
});

export function parseMarkdown(content: string) {
  return marked.parse(content);
}
