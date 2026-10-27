# 学習動画ライブラリ

会社PC・自宅PC・iPhoneで作った動画を、どこからでも見られるようにするサイトです。
GitHub Pages(無料)で公開します。

## ファイルの置き場所

```
videos/          ← mp4 を入れる
  安全教育/      ← フォルダを作るとカテゴリになる(任意)
    手順1_準備.mp4
motion/          ← Motion で作った HTML を入れる
  会社紹介.html          ← 1ファイルのもの
  冷凍サイクル/          ← 画像などが付いているものはフォルダごと
    index.html
youtube.json     ← YouTube(限定公開)の動画を載せたいときに書く
```

- ファイル名がそのままタイトルになります(`_` は空白に置き換わります)
- 追加して main に反映すると、1〜2分で一覧が自動で更新されます
- 一覧(videos.json)は自動で作られるので、自分で編集する必要はありません

## YouTube の動画を載せる場合

`youtube.json` を次のように書きます(最後の項目の後ろに `,` を付けないこと)。

```json
[
  { "title": "長い研修動画", "url": "https://youtu.be/xxxxxxxxxxx", "category": "研修" },
  { "title": "もう1本", "url": "https://www.youtube.com/watch?v=yyyyyyyyyyy" }
]
```

## 容量の目安

- サイト全体で 1GB まで、1ファイル 100MB まで
- ブラウザ(iPhone含む)からのアップロードは 1ファイル 25MB まで。大きいものは GitHub Desktop で
- 一度上げたファイルは消しても容量が戻らないので、差し替えはなるべく少なく
