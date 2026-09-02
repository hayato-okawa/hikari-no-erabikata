# 灯りの選び方 - 運用リポジトリ

一人暮らし・新生活向け家電/ガジェット選びガイド。アフィリエイト収益型の静的サイト。
初期費用0円・スマホ一台での運用を前提に設計しています。

## 構成

```
index.html              トップページ(記事一覧)
about.html               サイト概要
privacy-policy.html      プライバシーポリシー(AdSense審査に必要)
style.css                共通スタイル
robots.txt / sitemap.xml SEO用ファイル
articles/                 公開済み記事
articles-queue/           公開待ちの記事キュー(連番ファイル名順に公開される)
templates/article-template.html  記事HTMLの雛形
scripts/publish_next.py  週1回、キューから1本取り出して公開するスクリプト
.github/workflows/weekly-publish.yml  上記スクリプトを毎週月曜21:00 JSTに自動実行
```

## Claude Codeアプリでのデプロイ手順(スマホのみで完結)

Claude Codeアプリ(またはClaude Code経由のリモート環境)で、以下をそのまま依頼してください。

### 1. GitHubへのログイン(初回のみ・スマホブラウザで完結)

```
gh auth login
```
表示される8桁のコードをスマホのブラウザで `github.com/login/device` に入力するだけで認証できます。GitHubアカウントを持っていない場合は、先にスマホブラウザで無料アカウントを作成してください。

### 2. リポジトリ作成・初回push

```
gh repo create hikari-no-erabikata --public --source=. --push
```

### 3. GitHub Pagesを有効化

```
gh api -X POST repos/{owner}/hikari-no-erabikata/pages -f "source[branch]=main" -f "source[path]=/"
```
数分後、`https://{owner}.github.io/hikari-no-erabikata/` で公開されます。

### 4. サイト内のURLを実際のドメインに置き換え

`index.html` / `articles/*.html` / `sitemap.xml` / `robots.txt` / `scripts/publish_next.py` 内の
`https://example.github.io` を実際の公開URLに一括置換してください(Claude Codeに「example.github.ioを実際のURLに置き換えてpushして」と依頼すればOKです)。

### 5. 週次自動公開の動作確認

GitHub Actionsは毎週月曜21:00 JSTに自動実行されますが、手動でも即テストできます。
```
gh workflow run weekly-publish.yml
```

## 収益化の申請(スマホブラウザで完結・唯一の人手作業)

以下は自動化できないため、スマホのブラウザから直接申請してください。サイトが実際に公開されてから申請します。

1. **Amazonアソシエイト** … スマホブラウザで [affiliate.amazon.co.jp](https://affiliate.amazon.co.jp) から登録。サイトURLの入力が必要です。
2. **楽天アフィリエイト** … [affiliate.rakuten.co.jp](https://affiliate.rakuten.co.jp) から登録。
3. **Google AdSense** … [adsense.google.com](https://adsense.google.com) から登録。審査には数日〜数週間かかり、ある程度の記事数(目安10本以上)とプライバシーポリシーの設置が求められます。

審査が通ったら、各サービスの発行するアフィリエイトタグ/広告コードを、`pick-box` 内の `<a class="buy">` リンクや記事内に反映してください(この差し込み作業もClaude Codeに依頼できます)。

## 記事を追加する(コンテンツの継続生成)

新しい記事は `articles-queue/` に連番のHTMLファイルとして追加します。形式:

```
title: 記事タイトル
tag: カテゴリ名
dek: 一覧に表示する要約文
slug: url-slug
---
<p>本文をHTMLで記述...</p>
<h2>見出し</h2>
<p>...</p>
```

キューに記事が溜まっている限り、週1本ずつ自動で公開され続けます。記事本体の執筆(このチャットやClaude Codeでのリサーチ・ドラフト作成)だけが継続的に必要な人手作業です。

## 法令・規約に関する注意

- アフィリエイト表示(景品表示法のステマ規制)として、記事下部に開示文を入れています。表現を変える場合も開示自体は必ず残してください。
- Amazon/楽天の商品リンクは、各プログラムの規約(画像の扱い、価格表示、リンク形式など)に沿って設置してください。
- 医療・健康・金融など高リスクな商品カテゴリは扱わない前提の設計です。扱う場合は各法令(薬機法・景表法等)の確認が別途必要です。
