# Book JSON Skill

[English](README.md) · [繁體中文](README.zh-TW.md) · [简体中文](README.zh-CN.md) · [日本語](README.ja.md) · [한국어](README.ko.md)

英語の単語リスト、PDF、スキャン文書、写真から、自分用の単語帳 `book.json` を作成します。語義に使う言語を指定すると、AI が対象の語彙を抽出し、例文と訳文を補い、付属のテンプレートに従って結果を確認します。

これは、独立した Python 検証ツールを含む **AI エージェント用スキル**です。内容の生成や画像・PDF の読み取りには、スキルを使うエージェントの機能を利用します。検証ツールを単独で実行しても、語彙の抽出・翻訳・生成は行われません。

## 作成できるもの

- 英語、簡体字中国語、繁体字中国語、日本語、韓国語など、指定した言語による語義。
- **すべての語義グループ**に対応する英語の例文と指定言語の訳文。
- 任意の学習単元構成。`Lesson 2` や `Unit 1 / Lesson 2` は `word.unit` に保存し、単元分けのない単語帳ではこのフィールドを省略します。
- 文字列による連続した ID。同一単元内の重複項目は統合し、異なる単元の項目は別レコードとして保持します。
- 確認できない発音記号は空文字列にし、不足情報をファイル外で報告します。
- 新しい単語帳、または既存の単語帳を指定して語彙を追加した統合版。

出力は、本プロジェクトの [単語帳フォーマット仕様](skills/book-json/references/book_template.md) に対応するアプリケーション向けです。あらゆる単語学習ソフトで使える共通交換形式ではありません。読み込み先のアプリが対応する語義の言語は、このスキルで生成できる言語より少ない場合があります。

## インストール

このリポジトリをダウンロードして展開するか、クローンし、利用するツールに応じて以下の方法を選んでください。コピーするのは、入手したプロジェクト内の **`skills/book-json` フォルダー全体**です。通常は個人用にインストールし、特定のプロジェクトだけで使う場合は、そのプロジェクト内に配置します。

Windows の表は Windows 上で直接実行する場合のパスです。WSL 内でツールを実行する場合は、Windows のユーザーフォルダーではなく、WSL 内の Linux ユーザーのホームディレクトリを使ってください。

### Claude Code

#### Windows

| 使用範囲 | インストール先 | 完全なパスの例 |
| --- | --- | --- |
| 個人用（推奨） | `%USERPROFILE%\.claude\skills\book-json\` | `C:\Users\alice\.claude\skills\book-json\` |
| 特定のプロジェクト | `<プロジェクトのルート>\.claude\skills\book-json\` | `C:\Projects\my-study\.claude\skills\book-json\` |

個人用フォルダーをすぐに開くには、次の手順を使います。

1. **Win + E** でエクスプローラーを開き、**Ctrl + L** でアドレスバーを選択します。
2. `%USERPROFILE%` を貼り付けて Enter キーを押し、現在のユーザーフォルダーを開きます。
3. その中に `.claude` フォルダー、さらにその中に `skills` フォルダーを作成します。既にあるフォルダーはそのまま使います。
4. 入手したプロジェクト内の `skills/book-json` フォルダー全体を、この `skills` フォルダーにコピーします。
5. `%USERPROFILE%\.claude\skills\book-json\SKILL.md` が存在することを確認します。

`.claude\skills` が既に存在する場合は、エクスプローラーのアドレスバーに `%USERPROFILE%\.claude\skills` を貼り付けると直接開けます。これらの `%USERPROFILE%` を含むパスは、エクスプローラーのアドレスバー用です。

#### macOS

| 使用範囲 | インストール先 | 完全なパスの例 |
| --- | --- | --- |
| 個人用（推奨） | `~/.claude/skills/book-json/` | `/Users/alice/.claude/skills/book-json/` |
| 特定のプロジェクト | `<プロジェクトのルート>/.claude/skills/book-json/` | `/Users/alice/Projects/my-study/.claude/skills/book-json/` |

個人用フォルダーを初めて用意する場合は、「ターミナル」で次の 2 行を実行すると、必要なフォルダーを作成して Finder で開けます。

```sh
mkdir -p "$HOME/.claude/skills"
open "$HOME/.claude/skills"
```

入手したプロジェクト内の `skills/book-json` フォルダー全体を、開いた `skills` フォルダーにコピーし、`~/.claude/skills/book-json/SKILL.md` が存在することを確認します。

Finder では **Command + Shift + G** を押して `~/.claude/skills/` を入力すると直接開けます。フォルダーがまだない場合は、上記のターミナルコマンドで作成してください。macOS では `.claude` のように名前がドットで始まるフォルダーは通常非表示です。**Command + Shift + .** で表示・非表示を切り替えられます。

特定のプロジェクトにインストールする場合は、そのルートに `.claude/skills/` を作成し、同じ `book-json` フォルダーをコピーします。Claude Code での呼び出しは **`/book-json`** です。[Claude Code の公式スキルドキュメント](https://code.claude.com/docs/en/skills)も参照してください。

### Codex

#### Windows

| 使用範囲 | インストール先 | 完全なパスの例 |
| --- | --- | --- |
| 個人用（推奨） | `%USERPROFILE%\.agents\skills\book-json\` | `C:\Users\alice\.agents\skills\book-json\` |
| 特定のプロジェクト | `<プロジェクトのルート>\.agents\skills\book-json\` | `C:\Projects\my-study\.agents\skills\book-json\` |

個人用フォルダーをすぐに開くには、次の手順を使います。

1. **Win + E** でエクスプローラーを開き、**Ctrl + L** でアドレスバーを選択します。
2. `%USERPROFILE%` を貼り付けて Enter キーを押し、現在のユーザーフォルダーを開きます。
3. その中に `.agents` フォルダー、さらにその中に `skills` フォルダーを作成します。既にあるフォルダーはそのまま使います。
4. 入手したプロジェクト内の `skills/book-json` フォルダー全体を、この `skills` フォルダーにコピーします。
5. `%USERPROFILE%\.agents\skills\book-json\SKILL.md` が存在することを確認します。

`.agents\skills` が既に存在する場合は、エクスプローラーのアドレスバーに `%USERPROFILE%\.agents\skills` を貼り付けると直接開けます。これらの `%USERPROFILE%` を含むパスは、エクスプローラーのアドレスバー用です。

#### macOS

| 使用範囲 | インストール先 | 完全なパスの例 |
| --- | --- | --- |
| 個人用（推奨） | `~/.agents/skills/book-json/` | `/Users/alice/.agents/skills/book-json/` |
| 特定のプロジェクト | `<プロジェクトのルート>/.agents/skills/book-json/` | `/Users/alice/Projects/my-study/.agents/skills/book-json/` |

個人用フォルダーを初めて用意する場合は、「ターミナル」で次の 2 行を実行すると、必要なフォルダーを作成して Finder で開けます。

```sh
mkdir -p "$HOME/.agents/skills"
open "$HOME/.agents/skills"
```

入手したプロジェクト内の `skills/book-json` フォルダー全体を、開いた `skills` フォルダーにコピーし、`~/.agents/skills/book-json/SKILL.md` が存在することを確認します。

Finder では **Command + Shift + G** を押して `~/.agents/skills/` を入力すると直接開けます。フォルダーがまだない場合は、上記のターミナルコマンドで作成してください。macOS では `.agents` のように名前がドットで始まるフォルダーは通常非表示です。**Command + Shift + .** で表示・非表示を切り替えられます。

特定のプロジェクトにインストールする場合は、そのルートに `.agents/skills/` を作成し、同じ `book-json` フォルダーをコピーします。Codex CLI/IDE での呼び出しは **`$book-json`** です。[Codex の公式ローカルスキルドキュメント](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)も参照してください。

### その他のツール

- **`SKILL.md` に対応するツール**：そのツールの公式ドキュメントでインストール先と有効化・呼び出し方法を確認し、`skills/book-json` フォルダー全体をコピーしてください。すべてのツールに共通するインストール先や呼び出しコマンドはありません。
- **スキル機能がないツール**：ファイルを読める AI に `SKILL.md` と `assets/`、`references/`、`scripts/` をまとめて渡し、スキルの指示に従って `book.json` を生成するよう依頼できます。これは手動での利用方法であり、`/book-json` や `$book-json` がコマンドとして使えるようになるわけではありません。Python を実行できない場合は、自動検証を実施していないことを明示してください。

### インストール後の確認と動作条件

パス中の `alice` と `my-study` は例です。完全なパスの例を使う場合は実際のユーザー名とプロジェクトの場所に置き換えてください。`%USERPROFILE%` と `~` は現在のユーザーフォルダーを表すため、そのまま使えます。

コピー先の `book-json` の直下に `SKILL.md` がある構成にします。`book-json/book-json/SKILL.md` のようにフォルダーを二重にしないでください。`SKILL.md` だけをコピーすると、テンプレートと検証ツールが不足します。

動作条件：

- エージェントが入力ファイルを読み取り、結果を保存できること。写真やスキャン PDF には画像認識または OCR、テキスト PDF には文書読み取りツールが必要です。このリポジトリに OCR エンジンは含まれていません。
- 自動検証には **Python 3.10 以降**が必要です。検証ツールに**サードパーティーの依存パッケージはありません**。Python がない場合、エージェントは手動で確認できますが、自動検証を実施できなかったことを明示する必要があります。
- このプロジェクト専用の API キーは不要です。モデルへのアクセスやツールは、利用するエージェント側の設定に従います。

## 使い方

**Claude Code は `/book-json`、Codex CLI/IDE は `$book-json`** で呼び出します。その他のツールは、そのツールの有効化方法、または上記の手動での利用方法に従ってください。**語義の言語と、単語または元のファイルの両方**を指定してください。不足している項目があれば、スキルが確認します。「中国語」とだけ指定した場合は、簡体字か繁体字かを確認します。

以下の 3 つの例は Codex の呼び出し方法で記載しています。Claude Code では先頭行を `/book-json` に置き換えてください。その他のツールでは、そのツールの呼び出し方法に合わせてください。

### 単語を直接入力する

```text
$book-json
語義の言語：日本語。
単語：apple, borrow, look after。
難易度：A2。
book.json を生成してください。これらの単語に Unit や Lesson の区分はありません。
```

### PDF または写真から作成する

元のファイルを添付して、次のように依頼します。

```text
$book-json
語義の言語：日本語。
添付 PDF の 4～8 ページにある単語リストと、添付した 2 枚の写真の語彙を使ってください。
資料の Unit/Lesson 見出しを保持し、英語の例文と日本語訳を付けて book.json を作成してください。
```

ページ範囲、難易度、単元名、出力先ディレクトリは任意です。スキルは読む順序と抽出漏れを確認します。判読できない項目がある場合、完全な単語帳を渡すには、より鮮明な切り抜き画像やページが必要です。明確な単語リストのない一般的な文章では、どの単語を収集するか指定してください。

### 既存の単語帳に追加する

```text
$book-json
語義の言語：日本語。
添付した既存の book.json に、この写真の語彙を追加してください。
統合した結果を book.extended.json として保存してください。
```

既存の正しい内容は保持します。同一単元内で綴りが同じ項目は、語義を失わずに統合します。異なる単元の項目は別々に保持します。既存の単語帳の言語が指定言語と異なる場合は、処理方法を確認します。上書きを指定しない限り、新しいファイルに保存します。

## 出力形式

```json
[
  {
    "word": {
      "wordHead": "apple",
      "wordId": "1",
      "content": {
        "usphone": "",
        "ukphone": "",
        "trans": [
          {
            "tranCn": "りんご",
            "pos": "n",
            "sentence_example": "I eat an apple after lunch.\n昼食後にりんごを一つ食べます。"
          }
        ]
      }
    }
  }
]
```

`tranCn` は従来からのフィールド名で、**選択した言語での語義**を格納します。名前を変更したり、`language` メタデータを追加したりしないでください。例文フィールドは、JSON の解析後にちょうど 2 行になる必要があります。語義の言語が英語の場合、2 行目には例文と同じ意味の英文を別の表現で記述します。

**どの単語帳でも `unit` は省略できます。** 元の資料にある Lesson は `unit` に保存し、別の `lesson` フィールドは追加しません。元の語義と品詞は保持し、例文がない場合は AI が作成します。発音記号は確認できたものだけ記入します。句読点による語義の分割や単元ごとの重複統合については、[完全なフォーマット仕様](skills/book-json/references/book_template.md)を参照してください。

サンプル：[English](examples/book.en.json)、[繁體中文](examples/book.zh-Hant.json)、[简体中文](examples/book.zh-Hans.json)、[日本語](examples/book.ja.json)、[한국어](examples/book.ko.json)、[任意の Lesson/Unit 分け](examples/book.lessons.json)。

## 検証

リポジトリのルートディレクトリで実行します。

```sh
python skills/book-json/scripts/validate_book.py examples/book.ja.json
python skills/book-json/scripts/validate_book.py /path/to/book.json --json
```

環境に応じて、`python` を `python3` などの Python 3 起動コマンドに置き換えてください。複数のファイルパスを指定できます。終了コード `0` は全ファイルの合格、`1` は検証の失敗を示します。`--json` を付けると機械可読なレポートを出力します。検証ツールはファイルを読み取るだけで、変更しません。

フィールドと型の厳密なチェック、必須の例文、連続した ID、重複する項目・語義、未置換のプレースホルダー、発音記号を囲む記号、UTF-8 JSON、インポート上限の **100,000 レコード／30 MiB** などを確認します。[JSON Schema](skills/book-json/assets/book.schema.json) によるエディター内でのチェックも利用できます。

構造の検証だけでは、OCR の正確さ、抽出漏れ、指定言語の使用、翻訳の品質、例文が適切な語義を表しているかどうかは判断できません。これらはスキルの指示に従い、エージェントが別途確認します。

## プロジェクト構成

```text
skills/book-json/
  SKILL.md                         エージェントの手順と適用条件
  agents/openai.yaml               表示用メタデータ
  assets/book.template.json        生成用テンプレート
  assets/book.schema.json          JSON Schema
  references/book_template.md      完全なフォーマット仕様
  references/source-extraction.md  PDF・写真の読み取り手順
  references/extending-books.md    既存単語帳への追加・統合ルール
  scripts/validate_book.py         標準ライブラリのみの読み取り専用検証ツール
examples/                         オリジナルのサンプル単語帳
tests/                            自動検証テスト
.github/workflows/validate.yml    Linux／Windows CI
```

## 開発と公開

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

開発用の依存パッケージは、テストとメタデータ・Schema のチェックにのみ使います。検証ツールの実行には不要です。CI ではテストとサンプル単語帳の検証を実行します。

GitHub に公開する場合は、**このディレクトリを独立したリポジトリのルート**にしてください。Flutter プロジェクト、元の語彙データ、ローカル環境固有のパス、外部プロジェクトのファイルには依存しません。配布時にはスキルフォルダー全体を含めてください。形式を変更する場合は、仕様、Schema、検証ツール、サンプル、テストを合わせて更新し、5 言語の README の内容も揃えてください。

ローカル作業用の `inputs/` と `outputs/` は Git の追跡対象から除外されています。アップロードした資料は、選択した AI 製品とそのツールによって処理されます。検証ツール自体はネットワーク通信を行いません。非公開の元資料をリポジトリにコミットしないでください。

## ライセンス

[MIT](LICENSE)。付属のサンプルはオリジナルです。このライセンスは本プロジェクトに適用され、ユーザーが提供する第三者の書籍や写真などには適用されません。
