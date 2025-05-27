# ビデオアノテーションツール

このツールは、任意のビデオファイルに対してアクションアノテーションを行うためのPyQt5ベースのアプリケーションです。
3つのクラス（アクション、チーム、位置）を選択してアノテーションを作成し、JSONファイルとして保存できます。

## 特徴

- 任意のビデオファイル（mp4, avi, mkv）に対応
- 3段階のラベル選択（アクション → チーム → 位置）
- アノテーションの自動保存・読み込み
- フレーム単位での精密な操作
- キーボードショートカット対応

## 環境構築

### 必要な環境
- Python 3.8以上
- Windows, macOS, Linux対応

### venv環境の作成

以下の手順でPython仮想環境を作成し、必要なライブラリをインストールします：

```bash
# 仮想環境の作成
python -m venv annotation

# 仮想環境の有効化
# Windows の場合:
annotation\Scripts\activate
# macOS/Linux の場合:
source annotation/bin/activate

# pipのアップグレード
pip install --upgrade pip

# 必要なライブラリのインストール
pip install PyQt5
```

### 設定ファイルの準備

アプリケーションを実行する前に、以下の設定ファイルを準備してください：

1. `config/classes.txt` - 第1段階のラベル（アクション）
2. `config/second_classes.txt` - 第2段階のラベル（チーム）
3. `config/third_classes.txt` - 第3段階のラベル（位置）

各ファイルには、1行に1つずつラベルを記述してください。

例：
```
# config/classes.txt
PASS
DRIVE
HEADER
HAIGH PASS
...

# config/second_classes.txt (about key player's own half)
right
left

# config/third_classes.txt (about Location)
Left center midfield
...
0 (OUT)
Right center midfield
...
```

## 使用方法

### アプリケーションの起動

```bash
# 仮想環境を有効化
annotation\Scripts\activate  # Windows
# または
source annotation/bin/activate  # macOS/Linux

# アプリケーションの起動
cd interface
python main_window.py
```

### 基本操作

1. **ビデオファイルを開く**
   - 「Open video」ボタンをクリック
   - 対応形式：mp4, avi, mkv

2. **アノテーションの作成**
   - アノテーションしたい位置で`Enter`キーを押す
   - 3つのラベルを順番に選択：
     - 第1段階：アクション（例：Goal, Card）
     - 第2段階：チーム（例：Home, Away）
     - 第3段階：位置（例：Left, Center, Right）

3. **アノテーションの保存**
   - 「保存」ボタンをクリック
   - または`Ctrl+S`キーを押す
   - ビデオファイルと同じフォルダに`{ビデオ名}_annotations.json`として保存

4. **アノテーションの削除**
   - 右側のリストでアノテーションを選択
   - `Delete`キーまたは`Backspace`キーを押す

### キーボードショートカット

- `Space`: 再生/一時停止
- `←`: 1フレーム戻る
- `→`: 1フレーム進む
- `Enter`: アノテーション作成
- `Delete/Backspace`: 選択したアノテーションを削除
- `Ctrl+S`: アノテーションを保存
- `Esc`: 選択解除
- `A/F1`: 再生速度を1倍に設定
- `Z/F2`: 再生速度を2倍に設定
- `E/F3`: 再生速度を4倍に設定

## アノテーションファイル形式

アノテーションは以下のJSON形式で保存されます：

```json
{
  "annotations": [
    {
      "position": 15000,
      "action": "Goal",
      "team": "Home",
      "location": "Center"
    },
    {
      "position": 30000,
      "action": "Card",
      "team": "Away", 
      "location": "Left"
    }
  ]
}
```

- `position`: ミリ秒単位での動画内の位置
- `action`: 第1段階のラベル
- `team`: 第2段階のラベル
- `location`: 第3段階のラベル

## トラブルシューティング

### よくある問題

1. **ビデオが再生されない**
   - ビデオファイルの形式を確認してください
   - PyQt5がサポートするコーデックを使用してください

2. **アノテーションが保存されない**
   - ビデオファイルのフォルダに書き込み権限があることを確認してください
   - ファイルパスに日本語が含まれていないか確認してください

3. **設定ファイルが読み込まれない**
   - `config/`フォルダ内に必要なテキストファイルがあることを確認してください
   - ファイルの文字エンコーディングがUTF-8であることを確認してください

## ライセンス

Apache v2.0
詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 作者

このツールは、SoccerNetアノテーションツールをベースに、任意のビデオファイルに対応するよう改良されました。

元の作者：
* **Anthony Cioppa**, University of Liège (ULiège)
* **Adrien Deliège**, University of Liège (ULiège)
* **Silvio Giancola**, King Abdullah University of Science and Technology (KAUST)
* **Meisam J. Seikavandi**, Aalborg University (AAU)
* **Jacob V. Dueholm**, Aalborg University (AAU)

詳細は[AUTHORS](AUTHORS)ファイルを参照してください。
