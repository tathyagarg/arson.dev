const variables = [
  "crust",
  "mantle",
  "base",
  "surface0",
  "surface1",
  "surface2",
  "text",
  "blue",
  "sapphire",
];

export function updateTheme(theme: string) {
  for (let variable of variables) {
    document.documentElement.style.setProperty(
      `--${variable}`,
      `var(--${theme}-${variable})`,
    );
  }
}
