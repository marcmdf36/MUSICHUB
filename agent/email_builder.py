from pathlib import Path

TEMPLATE_PATH = Path(__file__).parent.parent / "templates" / "email_template.html"

HEADER_IMAGE_URL = "https://raw.githubusercontent.com/marcmdf36/MUSICHUB/main/docs/header.jpg"

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
 
    songs_html = "".join(
        build_song_card(
            song=song,
            emoji=GENRE_EMOJIS.get(song.get("genre", ""), "🎵"),
            cover=song.get("album_cover") or None,
            url=song.get("spotify_url", "#"),
        )
        for song in songs
    )

    html = template.replace("{{header_image_url}}", HEADER_IMAGE_URL)
    html = template.replace("{{intro}}", intro)
    html = html.replace("{{songs_html}}", songs_html)
    html = html.replace("{{outro}}", outro)
 
    return html


def build_song_card(song: dict, emoji: str, cover: str | None, url: str) -> str:
    """
    Genera el bloque HTML de una tarjeta de canción para el email de MusicHub.
    Diseñado para encajar con el template musichub_template_v2.html.
    """

    cover_td = (
        f"<td width='90' style='vertical-align:top; padding:0;'>"
        f"<img src='{cover}' width='90' height='90' "
        f"style='display:block; border-radius:10px 0 0 10px; object-fit:cover;' "
        f"alt='Portada'/></td>"
        if cover else ""
    )

    album_year = " · ".join(filter(None, [song.get("album", ""), str(song.get("year", ""))]))
    reason    = song.get("reason", "")

    return f"""
        <tr>
          <td style="padding:10px 40px 0;">
            <table width="100%" cellpadding="0" cellspacing="0"
                   style="background-color:#f0e8fa;
                          border-radius:10px;
                          overflow:hidden;
                          border-left:3px solid #9b6ecf;">
              <tr>
                {cover_td}
                <td style="padding:14px 18px; vertical-align:top;">

                  <!-- Título + enlace -->
                  <p style="margin:0 0 3px; font-size:15px; line-height:1.4;">
                    <span style="font-size:16px;">{emoji}</span>
                    <a href="{url}"
                       style="color:#2e1a44;
                              text-decoration:none;
                              font-family:'Playfair Display', Georgia, serif;
                              font-weight:600;
                              letter-spacing:0.3px;">
                      {song['title']}
                    </a>
                  </p>

                  <!-- Artista · Álbum · Año -->
                  <p style="margin:0 0 8px;
                            font-size:12px;
                            color:#9b6ecf;
                            font-family:'Lato', Arial, sans-serif;
                            letter-spacing:0.5px;
                            text-transform:uppercase;
                            font-weight:400;">
                    {song['artist']}{(' · ' + album_year) if album_year else ''}
                  </p>

                  <!-- Motivo de la recomendación -->
                  {f'<p style="margin:0; font-size:13px; color:#4a3560; line-height:1.6; font-family:Lato, Arial, sans-serif; font-weight:300;">{reason}</p>' if reason else ''}

                </td>
              </tr>
            </table>
          </td>
        </tr>
        <tr><td style="height:6px;"></td></tr>
    """