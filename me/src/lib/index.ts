export const imageToAscii = async (src: string, width: number, height: number): Promise<string> => {
  const response = await fetch(src);
  const blob = await response.blob();
  const imageBitmap = await createImageBitmap(blob);

  const aspectRatio = imageBitmap.width / imageBitmap.height;
  const newHeight = Math.floor(width / aspectRatio);
  if (newHeight > height) {
    width = Math.floor(height * aspectRatio) * 2;
  } else {
    height = newHeight;
  }

  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d");
  if (!ctx) throw new Error("Could not get canvas context");

  ctx.drawImage(imageBitmap, 0, 0, width, height);
  const imageData = ctx.getImageData(0, 0, width, height);
  const pixels = imageData.data;

  const asciiChars = "$@B%8M#*ZO0QJUYXt/|({[?-+i!lI:`.     ";
  const asciiCharsLength = asciiChars.length;
  let asciiImage = "";

  for (let i = 0; i < pixels.length; i += 4) {
    const r = pixels[i];
    const g = pixels[i + 1];
    const b = pixels[i + 2];
    const brightness = (r + g + b) / 3;
    const charIndex = Math.floor((brightness / 255) * (asciiChars.length - 1));
    asciiImage += asciiChars[asciiCharsLength - charIndex - 1];
    if ((i / 4 + 1) % width === 0) {
      asciiImage += "\n";
    }
  }

  return asciiImage;
}
