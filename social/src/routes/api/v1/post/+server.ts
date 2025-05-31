export const POST = async ({ request, locals }) => {
  const formData = await request.formData();
  console.log('Form Data:', formData);

  return new Response(JSON.stringify({
    message: 'Form data received successfully',
  }), {
    headers: {
      'Content-Type': 'application/json'
    }
  });
}
