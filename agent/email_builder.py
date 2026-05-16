from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "email_template.html"

GENRE_EMOJIS = {
    "rock": "🎸",
    "indie": "🌿",
    "electronic": "🔊",
    "house": "🏠",
    "classical": "🎻",
    "techno": "⚡",
    "jazz": "🎷",
    "hiphop": "🎤",
    "soul": "💜",
}


def build_email_html(songs: list[dict], intro: str, outro: str) -> str:
    """Construye el email HTML con datos reales de Spotify."""
    template = TEMPLATE_PATH.read_text(encoding="utf-8")

    songs_html = ""
    for i, song in enumerate(songs):
        emoji = GENRE_EMOJIS.get(song.get("genre", ""), "🎵")
        cover = song.get("album_cover", "")
        url = song.get("spotify_url", "#")

        songs_html += f"""
        <tr>
          <td style="padding:12px 40px;">
            <table width="100%" cellpadding="0" cellspacing="0" 
                   style="background-color:#f9f9fb; border-radius:10px; overflow:hidden;">
              <tr>
                {"<td width='80' style='vertical-align:top;'><img src='" + cover + "' width='80' height='80' style='display:block; border-radius:10px 0 0 10px;' alt='Album cover'/></td>" if cover else ""}
                <td style="padding:14px 18px; vertical-align:top;">
                  <p style="margin:0 0 4px; font-size:15px;">
                    {emoji} <a href="{url}" style="color:#1a1a2e; text-decoration:none; font-weight:bold;">{song['title']}</a>
                  </p>
                  <p style="margin:0 0 6px; font-size:13px; color:#666;">
                    {song['artist']} · {song.get('album', '')} · {song.get('year', '')}
                  </p>
                  <p style="margin:0; font-size:13px; color:#444; line-height:1.5;">
                    {song.get('reason', '')}
                  </p>
                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr><td style="height:8px;"></td></tr>
        """

    html = template.replace("{{intro}}", intro)
    html = html.replace("{{songs_html}}", songs_html)
    html = html.replace("{{outro}}", outro)

    return html