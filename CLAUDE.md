# Topo dos Clips — padrão de cortes

Este repositório é usado para gerar cortes de lives/vídeos pelo celular.
O usuário manda um link (Twitch funciona; YouTube bloqueia download em servidor na nuvem —
nesse caso pedir para enviar o arquivo do vídeo pelo app) e pede N cortes de X a Y segundos.

## Padrão obrigatório de cada corte
- Vertical 9:16 (1080x1920), 30 fps, H.264 + AAC, áudio normalizado (loudnorm I=-14).
- **Título fixo no topo do vídeo** durante o corte inteiro: faixa branca com texto preto
  (Inter Black), curto e em maiúsculas, dizendo o assunto do momento.
  Ex.: "FAKE NEWS: O GOOGLE DIZ QUE ELE É GAY", e em momentos de raiva algo como "ELE DEU RAGE NA LIVE".
- Legenda palavra a palavra (máx. 3 palavras por vez), Inter Black branca com contorno preto,
  em maiúsculas. Na câmera cheia fica embaixo (y≈1560); no layout de jogo fica na divisa câmera/jogo (y≈770).
- Layouts:
  - Câmera em tela cheia → recorte central 9:16 no rosto.
  - Jogo/tela com câmera no canto → câmera em cima (1080x770) e jogo embaixo (1080x1150).
- **Conferir o layout ao longo do corte inteiro**, não só no meio: se no início/fim do trecho a
  live estiver em outra cena (ex.: painel/tela compartilhada), ajustar o início/fim ou o layout.
- Entregar os arquivos com SendUserFile e uma tabela: nº, tempo na live, título.

## Fluxo
1. `yt-dlp` baixa só o áudio → `ffmpeg` para wav 16 kHz mono.
2. `scripts/transcribe.py` (faster-whisper `small`, pt, word timestamps) → `transcript.jsonl`.
3. Ler a transcrição condensada, escolher os momentos, ajustar tempos com `scripts/show.py`.
4. `scripts/render.py` lê `vod/clips.txt` (`nº|início|fim|nome`) e `vod/titles.txt` (`nº|TÍTULO`)
   e corta direto do m3u8 da Twitch (ffmpeg precisa de `http_proxy=$HTTPS_PROXY`).
   Clipes 01–10 = câmera cheia, 11+ = jogo (ajustar a regra `game=` conforme o vídeo).
