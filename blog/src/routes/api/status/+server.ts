export const GET = async () => {
  return new Response(
    JSON.stringify({
      message: 'Hello, world!',
    }),
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
}
