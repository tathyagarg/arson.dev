
export const imageToAscii = async (
  src: string,
  width: number,
  height: number,
): Promise<string> => {
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
  imageBitmap.close();

  const pixels = ctx.getImageData(0, 0, width, height).data;

  const asciiChars = "$@B%8M#*ZO0QJUYXt/|({[?-+i!lI:`.    ";
  const asciiCharsLength = asciiChars.length;

  const brightnesses: number[] = [];

  // Calculate brightness of every pixel.
  for (let i = 0; i < pixels.length; i += 4) {
    const r = pixels[i];
    const g = pixels[i + 1];
    const b = pixels[i + 2];

    brightnesses.push((r + g + b) / 3);
  }

  // Find minimum and maximum brightness.
  const minBrightness = Math.min(...brightnesses);
  const maxBrightness = Math.max(...brightnesses);
  const brightnessRange = maxBrightness - minBrightness;

  let asciiImage = "";

  // Normalize brightness relative to the darkest pixel.
  for (let i = 0; i < brightnesses.length; i++) {
    const normalized = brightnessRange === 0
      ? 0
      : ((brightnesses[i] - minBrightness) / brightnessRange) * 255;

    const charIndex = Math.floor(
      (normalized / 255) * (asciiCharsLength - 1),
    );

    asciiImage += asciiChars[asciiCharsLength - 1 - charIndex];

    if ((i + 1) % width === 0) {
      asciiImage += "\n";
    }
  }

  return asciiImage;
};

