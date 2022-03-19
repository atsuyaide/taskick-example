# Taskick Example Application

ここではPNG画像を特定のフォルダに保存されたとき, その画像をPDFに変換し出力フォルダに保存するアプリケーションを作成します.

アプリケーションは以下のアルゴリズムで動作します.

1. `input`フォルダーにPNGファイルが保存されると, それを検知.
2. 保存されたファイルパスを変換スクリプトに渡し, PDFに変換.
3. 変換したPDFを`output`フォルダに保存.
4. inputフォルダを定期的に削除し, 綺麗な状態を保つ.

使い方・動作例は[Taskick](https://github.com/kappa000/taskick-example.git)を参照してください.

## Structures

このリポジトリは以下のフォルダ構成です.

```text
├── input           # ここにPNG画像が保存されるとアプリケーションを起動する
├── output          # 変換されたPDFはこのフォルダに保存される
├── jobconf.yaml    # 実効するスクリプトや起動スケジュールなどが設定可能
├── sandbox         # 好きに使ってください:)
└── src
    └── png2pdf.py  # PNGをPDFに変換するスクリプト
```

Taskickとそれぞれのファイルは以下の責任範囲を持ちます.

> 1. `input`フォルダーにPNGファイルが保存されると, それを検知. <- Taskick(`jobconf.yaml`で設定)
> 2. 保存されたファイルパスを変換スクリプトに渡し, PDFに変換. <- Taskick(`png2pdf.py`を起動)
> 3. 変換したPDFを`output`フォルダに保存. <- `png2pdf.py`
> 4. inputフォルダを定期的に削除し, 綺麗な状態を保つ. <- Taskick(`rm -f input/*.*`)

状況設定は以下のYAMLファイルで設定されています.

```yaml
wellcome_taskick: # Task name
  status: 1 # 0: inactive, 1: active
  commands:
    - echo
    - $(date) Welcome to Taskick!
  execution:
    event_type: null # If event_type is NULL, it is executed only at startup.

remove_input_folder:
  status: 1
  commands:
    - rm -f input/*.*
  execution:
    immediate: true # If true, it is executed at startup.
    event_type: time
    detail:
      when: "*/1 * * * *" # Crontab format: Run every 1 minute.

png2pdf:
  status: 1
  commands:
    - python
    - ./src/png2pdf.py
  execution:
    immediate: false
    event_type: file
    propagate: true # If true, events that occur at runtime (such as the path of an edited file) are passed to the running script.
    detail:
      path: ./input
      recursive: false
      handler: # Support all watchdog.handler.
        name: PatternMatchingEventHandler
        args: # This args is passed to the handler.
          patterns:
            - "*.png"
      when: # Supprt created, deleted, modified, closed, moved event.
        - created
```

実行間隔や起動基準などの変更は`jobconf.yaml`を編集するのみで可能です.

例えば,

- `input`フォルダを掃除する間隔を5分にしたい.

```yaml
when: "*/1 * * * *"
```

↓

```yaml
when: "*/5 * * * *"
```

- 変換する対象ファイルをPNGだけでなくJPEGも対応させたい.

```yaml
patterns:
  - "*.png"
```

↓

```yaml
patterns:
  - "*.png"
  - "*.jpeg"
