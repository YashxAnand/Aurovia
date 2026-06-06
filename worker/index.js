export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const key = url.pathname.slice(1); // Remove leading slash

    if (!key) {
      return new Response("Aurovia Assets Bucket - Please provide a file path.", { status: 400 });
    }

    if (request.method !== 'GET') {
      return new Response("Method not allowed", { status: 405 });
    }

    const object = await env.MY_BUCKET.get(key);

    if (object === null) {
      return new Response("Object Not Found", { status: 404 });
    }

    const headers = new Headers();
    object.writeHttpMetadata(headers);
    headers.set("etag", object.httpEtag);
    headers.set("Access-Control-Allow-Origin", "*");

    return new Response(object.body, {
      headers,
    });
  },
};
