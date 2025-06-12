async function replace_embed_link(content) {
  const embeds = content.match(/!\[\[(.*?)\]\]/g) || [];
  for (const embed of embeds) {
    const noteName = embed.match(/\[\[(.*?)\]\]/)[1];
    const noteContent = await this.app.vault.adapter.read(`${noteName}.md`);
    content = content.replace(embed, noteContent);
  }
  return content;
};

module.exports = replace_embed_link