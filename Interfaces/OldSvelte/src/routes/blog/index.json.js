import posts from "./_posts.js";

const contents = JSON.stringify(
  posts.map((post) => {
    return {
      slug: post.slug,
      title: post.title,
      preview_content: post.preview_content,
      preview_image: post.preview_image,
    };
  })
);

export function get(req, res) {
  res.writeHead(200, {
    "Content-Type": "application/json",
  });

  res.end(contents);
}
